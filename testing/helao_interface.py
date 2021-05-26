import os
import sys
import subprocess
import signal
import psutil
from importlib import import_module
import PySimpleGUI as gui

import time

helao_root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.join(helao_root, 'config'))
config = import_module(sys.argv[1]).config

items = config['launch']['server']+config['launch']['action']+config['launch']['orchestrator']+config['launch']['visualizer']

layout = [[gui.Text(text=item,k=item),
           gui.Button("open",enable_events=True,k=item+"-open"),
           gui.Button("close",button_color='green',disabled=True,enable_events=True,k=item+"-close"),
           gui.Button("refresh",disabled=True,enable_events=True,k=item+"-refresh")] for  item in items]
window = gui.Window('HELAO',layout)

servers = {}

while True:
    event, values = window.read(timeout=1000)
    ps = [p.pid for p in list(psutil.process_iter())]
    closed = []
    for server in servers.items():
        if not (server[1][1].pid in ps and server[1][0].pid in ps):
            print(f"server {server[0]} seems to have closed unexpectedly")
            closed.append(server[0])
            window[server[0]+"-open"].update(disabled = False)
            window[server[0]+"-close"].update(disabled = True)
            window[server[0]+"-refresh"].update(disabled = True)
    for c in closed:
        del servers[c]
    if event == gui.WIN_CLOSED:
        break
    elif event.split('-')[0] in config['launch']['server'] or event.split('-')[0] in config['launch']['action'] or event.split('-')[0] in config['launch']['orchestrator']:
        s = event.split('-')[0]
        api =  "server" if event.split('-')[0] in config['launch']['server'] else "action" if event.split('-')[0] in config['launch']['action'] else "orchestrators"
        if event.split('-')[1] == 'open':
            l = list(psutil.process_iter())
            cmd = ["python", f"{api}/{s}.py", sys.argv[1]]
            print(f"Starting {api}/{s}")
            p0 = subprocess.Popen(cmd, cwd=helao_root, shell=True)
            time.sleep(.1)
            p1,p2 = None, None
            for p in psutil.process_iter():
                if p not in l:
                    if p.name() == 'cmd.exe':
                        p1 = p
                    if p.name() == 'python.exe':
                        p2 = p
            if not (p1.pid == p0.pid and p2 != None):
                print(f"server {s} failed to start")
            else:
                servers.update({s:(p0,p2)})
                window[event].update(disabled = True)
                window[s+"-close"].update(disabled = False)
                window[s+"-refresh"].update(disabled = False)
        elif event.split('-')[1] == 'close':
            print(f"Killing {api}/{s}.py")
            l = list(psutil.process_iter())
            servers[s][0].terminate()
            servers[s][1].terminate()
            time.sleep(.1)
            terminated = [None,None]
            l2 = list(psutil.process_iter())
            for p in l:
                if p not in l2:
                    if p.name() == 'cmd.exe':
                        terminated[0] = servers[s][0].pid
                    if p.name() == 'python.exe':
                        terminated[1] = servers[s][1].pid
            if not terminated == [servers[s][0].pid,servers[s][1].pid]:
                print(f"server {s} failed to close")
            else: 
                del servers[s]
                window[s+"-open"].update(disabled = False)
                window[event].update(disabled = True)
                window[s+"-refresh"].update(disabled = True)
        elif event.split('-')[1] == 'refresh':
            print(f"Killing {api}/{s}.py")
            l = list(psutil.process_iter())
            servers[s][0].terminate()
            servers[s][1].terminate()
            time.sleep(.1)
            terminated = [None,None]
            l2 = list(psutil.process_iter())
            for p in l:
                if p not in l2:
                    if p.name() == 'cmd.exe':
                        terminated[0] = servers[s][0].pid
                    if p.name() == 'python.exe':
                        terminated[1] = servers[s][1].pid
            if not terminated == [servers[s][0].pid,servers[s][1].pid]:
                print(f"server {s} failed to close")
            else: 
                del servers[s]
                window[s+"-open"].update(disabled = False)
                window[event].update(disabled = True)
                window[s+"-refresh"].update(disabled = True)

                cmd = ["python", f"{api}/{s}.py", sys.argv[1]]
                print(f"Starting {api}/{s}")
                p0 = subprocess.Popen(cmd, cwd=helao_root, shell=True)
                time.sleep(.1)
                p1,p2 = None, None
                for p in psutil.process_iter():
                    if p not in l2:
                        if p.name() == 'cmd.exe':
                            p1 = p
                        if p.name() == 'python.exe':
                            p2 = p
                if not (p1.pid == p0.pid and p2 != None):
                    print(f"server {s} failed to start")
                else:
                    servers.update({s:(p0,p2)})
                    window[event].update(disabled = True)
                    window[s+"-close"].update(disabled = False)
                    window[s+"-refresh"].update(disabled = False)
