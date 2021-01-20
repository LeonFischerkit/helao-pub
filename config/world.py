config = dict()

# action library provides generator functions which produce action
# lists from input decision_id grouping
config["action_libraries"] = ["lisa_sdc_demo"]

# we define all the servers here so that the overview is a bit better
config["servers"] = dict(
    motor=dict(
        host="127.0.0.1",
        port=8001,
        group="server",
        fast="galil_motion",
        simulate=True, # choose between simulator(default) or real device
        params=dict(
            count_to_mm=dict(
                A=1.0/3154.787,
                B=1.0/6395.45,
                C=1.0/6395.45,
                D=1.0/6397.95,
                u=154.1133/985482.0
            ),
            galil_ip_str="192.168.200.23",
            def_speed_count_sec=10000,
            max_speed_count_sec=25000,
            ipstr="192.168.200.23",
            axis_id=dict(
                x="D",
                y="B",
                z="C",
                s="A",
                #t="E",
                #u="F"
                ),
            #axlett="ABCD", # not needed anymore
            timeout = 60 # timeout for axis stop in sec
        )
    ),
    io=dict(
        host="127.0.0.1",
        port=8002,
        group="server",
        fast="galil_io",
        simulate=True, # choose between simulator(default) or real device
        params=dict(
            galil_ip_str="192.168.200.23",
            def_speed_count_sec=10000,
            max_speed_count_sec=25000,
            ipstr="192.168.200.23",
            Ain_id=dict(
                AI1="1",
                AI2="2",
                AI3="3",
                AI4="4",
                AI5="5",
                AI6="6",
                AI7="7",
                AI8="8"
                ),
            Din_id=dict(
                DI1="1",
                DI2="2",
                DI3="3",
                DI4="4",
                DI5="5",
                DI6="6",
                DI7="7",
                DI8="8"
                ),
            Dout_id=dict(
                DO1="1",
                DO2="2",
                DO3="3",
                DO4="4",
                DO5="5",
                DO6="6",
                DO7="7",
                DO8="8"
                ),
        )
    ),
    potentiostat=dict(
        host="127.0.0.1",
        port=8003,
        group="server",
        fast="gamry_server",
        simulate=True, # choose between simulator(default) or real device
        params=dict(
            temp_dump=".\temp",
            path_to_gamrycom=r"C:\Program Files (x86)\Gamry Instruments\Framework\GamryCOM.exe"
        )
    ),
    data=dict(
        host="127.0.0.1",
        port=8004,
        group="server",
        fast="HTEdata_server",
        mode = "legacy", # lagcy; modelyst
        params = dict(
        )
    ),
    orchestrator=dict(
        host="127.0.0.1",
        port=8010,
        group="orchestrators",
        fast="async_orch",
        path="."
    ),
    potentiostat_vis=dict(
        host="127.0.0.1",
        port=5006,
        group="visualizer",
        bokeh="bokeh_test",
        params = dict(
            ws_host="potentiostat"
        )
    ),
#    motor_aligner=dict(
#        host="127.0.0.1",
#        port=5007,
#        group="action",
#        bokeh="bokeh_platealigner",
#        params = dict(
#            ws_host="motor",
#        )
#    )
)
