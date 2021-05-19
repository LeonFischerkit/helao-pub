config = dict()

# action library provides generator functions which produce action
# lists from input decision_id grouping
#config["action_libraries"] = ["lisa_sdc_demo"]
config["action_libraries"] = ["lisa_ANEC2"]
local_data_dump=r'C:\INST\RUNS2'

# we define all the servers here so that the overview is a bit better
config["servers"] = dict(
    ##########################################################################
    # Orchestrator
    ##########################################################################
    orchestrator=dict(
        host="127.0.0.1",
        port=8001,
        group="orchestrators",
        fast="async_orch",
        path=".",
        params=dict(
            local_data_dump=f'{local_data_dump}'
            )
    ),
    ##########################################################################
    # Instrument Servers
    ##########################################################################
    data=dict(
        host="127.0.0.1",
        port=8002,
        group="server",
        fast="HTEdata_server",
        mode = "legacy", # lagcy; modelyst
        params = dict(
        )
    ),
    motor=dict(
        host="127.0.0.1",
        port=8003,
        group="server",
        fast="galil_motion",
        simulate=False, # choose between simulator(default) or real device
        params=dict(
            Transfermatrix = [[1,0,0],[0,1,0],[0,0,1]], # default Transfermatrix for plate calibration
            M_instr = [[1,0,0,-76.525],[0,1,0,-50.875],[0,0,1,0],[0,0,0,1]], # instrument specific calibration
            count_to_mm=dict(
                A=1.0/15835.31275,#1.0/15690.3,
                B=1.0/6398.771436,#1.0/6395.45,
                C=1.0/6396.315722,#1.0/6395.45,
                D=1.0/3154.787,#1.0/3154.787,
            ),
            galil_ip_str="192.168.200.23",
            def_speed_count_sec=10000,
            max_speed_count_sec=25000,
            ipstr="192.168.200.23",
            axis_id=dict(
                x="C",
                y="B",
                z="A",
                Rz="D",
                #t="E",
                #u="F"
                ),
            axis_zero=dict(
                A=0.0, #z
                B=52.0, #y
                C=77.0, #x
                D=0.0, #Rz
                #t="E",
                #u="F"
                ),
            #axlett="ABCD", # not needed anymore
            timeout = 10*60, # timeout for axis stop in sec
            tbroadcast = 2, # frequency of websocket broadcast (only broadcasts if something changes but need to reduce the frequeny of that if necessary)
        )
    ),
    potentiostat=dict(
        host="127.0.0.1",
        port=8004,
        group="server",
        fast="gamry_server",
        simulate=False, # choose between simulator(default) or real device
        params=dict(
            #path_to_gamrycom=r"C:\Program Files (x86)\Gamry Instruments\Framework\GamryCOM.exe"
            #dev_family = 'Interface', # 'Interface' or 'Reference', not need anymore, we can autodetect this
            dev_id = 0, # (default 0) Gamry device number in Gamry Instrument Manager (i-1)
            local_data_dump=f'{local_data_dump}', # will use this if orch is not running
            #path_to_gamrycom=r"C:\Program Files (x86)\Gamry Instruments\Framework\GamryCOM.exe"
            #path_to_gamrycom=r"C:\Program Files (x86)\Gamry Instruments\Framework 6\GamryCOM.exe"
        )
    ),
    aligner=dict(
        host="127.0.0.1",
        port=8005,
        group="server",
        fast="alignment_server",
        params = dict(
            data_server = "data", # will use this to get PM_map temporaily, else need to parse it as JSON later
            motor_server = "motor", # will use this to get PM_map temporaily, else need to parse it as JSON later
            vis_server = "aligner_vis", # will use this to get PM_map temporaily, else need to parse it as JSON later
            cutoff = 6, # cutoff of digits for TransferMatrix calculation
        )
    ),
    nimax=dict(
        host="127.0.0.1",
        port=8006,
        group="server",
        fast="nidaqmx_server",
        params = dict(
            local_data_dump=f'{local_data_dump}', # will use this if orch is not running
            dev_CellCurrent_trigger = 'PFI1', #P1.1
            dev_CellVoltage_trigger = 'PFI1', #P1.1
            dev_CellCurrent = {
                '1':'PXI-6289/ai16',
                '2':'PXI-6289/ai17',
                '3':'PXI-6289/ai18',
                '4':'PXI-6289/ai19',
                '5':'PXI-6289/ai20',
                '6':'PXI-6289/ai21',
                '7':'PXI-6289/ai22',
                '8':'PXI-6289/ai23',
                '9':'PXI-6289/ai0'
                },
            dev_CellVoltage = {
                '1':'PXI-6284/ai16',
                '2':'PXI-6284/ai17',
                '3':'PXI-6284/ai18',
                '4':'PXI-6284/ai19',
                '5':'PXI-6284/ai20',
                '6':'PXI-6284/ai21',
                '7':'PXI-6284/ai22',
                '8':'PXI-6284/ai23',
                '9':'PXI-6284/ai0'
                },
            dev_ActiveCellsSelection = {
                '1':'PXI-6289/port0/line23', #P0.23
                '2':'PXI-6289/port0/line24', #P0.24
                '3':'PXI-6289/port0/line25', #P0.25
                '4':'PXI-6289/port0/line26', #P0.26
                '5':'PXI-6289/port0/line27', #P0.27
                '6':'PXI-6289/port0/line28', #P0.28
                '7':'PXI-6289/port0/line29', #P0.29
                '8':'PXI-6289/port0/line30', #P0.30
                '9':'PXI-6289/port0/line31'  #P0.31
                },
            dev_FSWBCDCmd = {
                '1':'PXI-6284/port0/line5', #P0.5
                '2':'PXI-6284/port0/line1', #P0.1
                '3':'PXI-6284/port0/line2', #P0.2
                '4':'PXI-6284/port0/line3'  #P0.3
                },
            dev_GasFlowValves = {
                '1':'PXI-6284/port1/line2', #P1.2
                '2':'PXI-6284/port1/line3', #P1.3
                '3':'PXI-6284/port1/line4', #P1.4
                '4':'PXI-6284/port1/line5', #P1.5
                '5':'PXI-6284/port1/line6', #P1.6
                '6':'PXI-6284/port1/line7', #P1.7
                '7':'PXI-6284/port2/line0', #P2.0
                '8':'PXI-6284/port2/line1', #P2.1
                '9':'PXI-6284/port2/line2'  #P2.2
                },
            dev_MasterCellSelect = {
                '1':'PXI-6284/port0/line23', #P0.23
                '2':'PXI-6284/port0/line24', #P0.24
                '3':'PXI-6284/port0/line25', #P0.25
                '4':'PXI-6284/port0/line26', #P0.26
                '5':'PXI-6284/port0/line27', #P0.27
                '6':'PXI-6284/port0/line28', #P0.28
                '7':'PXI-6284/port0/line29', #P0.29
                '8':'PXI-6284/port0/line30', #P0.30
                '9':'PXI-6284/port0/line31', #P0.31
                'X':'PXI-6284/port0/line22'  #P0.22, two electrode
                },
            dev_Pumps = {
                'PeriPump':'PXI-6284/port0/line4	', #P0.4
#                'MultiPeriPump':'PXI-6284/port0/line0' #P0.0
                'Direction':'PXI-6284/port0/line0' #P0.0
                },
            dev_FSW = {
                'Done':'PXI-6284/port2/line4',  #P2.4
                'Error':'PXI-6284/port2/line6'  #P2.6
                },
#             dev_RSHTTLhandshake = {
#                 'RSH1':'PXI-6284/port2/line5',  #P2.5
#                 'RSH2':'PXI-6284/port2/line7',  #P2.7
#                 'RSH3':'PXI-6284/port2/line3',  #P2.3
# #                'port':'PXI-6284/ctr0',
# #                'term':'/PXI-6284/PFI8' #P2.0
#                 }
        )
    ),
    PAL=dict(
        host="127.0.0.1",
        port=8007,
        group="server",
        fast="PAL_server",
        params = dict(
            user = 'RSHS',
            key = r'c:\helao\sshkeys\rshs_private3.ppk', # needs to be in new openssh file format
            host = 'hte-rshs-01.htejcap.caltech.edu',
            dev_NImax = { # TTL handshake via NImax
                'start':'PXI-6284/port2/line5',  #P2.5
                'continue':'PXI-6284/port2/line7',  #P2.7
                'done':'PXI-6284/port2/line3',  #P2.3
                }
        )
    ),
    ##########################################################################
    # Visualizers (bokeh servers)
    ##########################################################################
    exp_vis=dict(#simple dumb modular visualizer
        host="127.0.0.1",
        port=5001,
        group="visualizer",
        bokeh="bokeh_modular_visualizer",
        params = dict(
            doc_name = "ANEC2 visualizer",
            ws_nidaqmx="nimax",
            ws_potentiostat = 'potentiostat',
        )
    ),
    operator=dict(
        host="127.0.0.1",
        port=5002,
        group="operators",
        bokeh="async_operator",
        path=".",
        params = dict(
            doc_name = "ADSS Operator",
            orch = 'orchestrator',
            data_server = "data",
            servicemode=False,
        )
    ),
    aligner_vis=dict(
        host="127.0.0.1",
        port=5003,
        group="action",
        bokeh="bokeh_platealigner",
        params = dict(
            aligner_server="aligner", # aligner and aligner_vis should be in tandem
        )
    ),
    
)
