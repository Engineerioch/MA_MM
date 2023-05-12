import numpy as np
import pandas as pd
import csv

#from Optimization import T_Hou_delta_max


def load_params(options, params):

    # Set time parameter for year
    year = {
        'start_time_of_months': [0, 744, 1416, 2160, 2880, 3624, 4344, 5088, 5832, 6552, 7296, 8016],   # hours
        'length_of_months': [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]                            # days
    }


    # Set economic parameters
# todo Einheiten der Kosten Checken
    eco = {
        'costs'     : {
            #todo: Array für die Strompreise & Vergütungen erstellen -> für fixen Strompreis erledgit
            'c_payment'     : 0.06 / 1000,                   # [Euro/kWh] Feed in tariff (Einspeisevergütung)
            'c_comfort'     : 0.7,                             # [€/kWh]
        }
    }
    # Set component parameters

    devs = {
    # Set Heat Storage parameter
        'Sto'   : {
            'T_Sto_Ersatz' : 32 + 273.15,
            'T_Sto_min' : 18 + 273.15,                   # [K] Minimum temperature of storage
            'T_Sto_max' : 95 + 273.15,                  # [K] Maximum temperature of storage
            'T_Sto_Env' : 18 + 273.15,                  # [K] Environmental temperature of storage in basement or utility room
            'T_Sto_Init': 36 + 273.15,                  # [K] initial Storage Temperature for Optimization
            'U_Sto'     : 0.3,                          # [W/m²K] Heat Transfer Coefficient of Storage (Wärmeübergangkoeffizient des Speichers)
            'T_Kalt'    : 18 + 273.15,                  # [K] Coldest Temperature of Water in Storage as this is the constant Basement Temperature
            'h_d_ratio' : 2,                            # [-] Ratio of Heat/Diameter
            'S_Wall'    : 0.15,
            'T_Sto_Use' : 32 + 273.15
        },


        'TWW': {
            'T_TWW_Min': 40 + 273.15,  # [K] Minimum Temperature of TWW-Storage
            'T_TWW_Init': 60 + 273.15,  # [K] initial Storage Temperature for Optimization
            'U_TWW': 0.3,  # [W/m²K] Heat Transfer Coefficient of Storage (Wärmeübergangkoeffizient des Speichers)            # [K] Coldest Temperature of Water in Storage as this is the constant Basement Temperature
            'h_d_ratio': 2,  # [-] Ratio of Heat/Diameter
            'S_Wall': 0.15,
            'T_TWW_Max' : 65 + 273.15,
            'T_TWW_Soll' : 50 + 273.15
        },

    # Set Heat Pump parameter
        'HP'    : {
            'Q_HP_Max'      : 10000,                        # [W]   Maximum Heat Power of Heat Pump
            'T_HP_VL_1'     : 40 + 273.15,                  # [K]   Constant Flow Temperature from HP to Storage in Mode 1
            'T_HP_VL_2'     : 70 + 273.15,                  # [K]   Constant Flow Temperature from HP to Storage in Mode 2
            'T_HP_VL_3'     : 65 + 273.15,
            'm_flow_HP'     : 1230 / 3600,                   # [kg/h] Constant Heat flow of HP if HP is running -> Dividieren um kg/s zu bekommen)
            'eta_HP'        : 0.4,                          # [-]   Gütegrad HP
            'Q_HP_Min'      : 0,                            # [W]   Minimum Heat power of HP
            'T_Spreiz_HP'      : 7,                            # [K]   Maximum Change of Temperature between Vorlauf and Rücklauf

        },

    # Set PV parameters
        'PV'    : {
            'n_mod'         :   20,                         # [-]    Number of PV- Modules
            'eta_nom_PV'    : 0.97,                         # [-]    Nominal efficiency of PV inverter
            'P_PV_Min'      : 0,                            # [W]    Minimum Power of PV-System = 0 kW
            'P_PV_Module'   : 300,                          # [W]    Nominal Power of one PV-Module = 300
            'a_PV'          : [0.02409, 0.00561, 0.01228]
        },

    # Set Consumer parameters (House = Hou)
        'Hou'   : {
            'T_Hou_delta_max'   :    20 + 273.15,           # [K]    Maximum Difference between T_Hou_Vl and T_Hou_RL
            'm_flow_Hou'        :    1107 / 3600,           # [kg/s] Constant Mass flow from Storage to House
            'T_Hou_Gre'         : 273.15 + 15,               # [K] Heizgrenztemperatur (Mittelwert über den Tag)
            'T_Spreiz_Hou'      : 7 + 273.15,
            'T_Hou_VL_min'      : 35 + 273.15,

        },

        # Set natural Constant and other constants given by nature
        'Nature'    : {
            'c_w_water'         : 4.18 * 1000,              # [Ws/kgK] Spezifische Wärmekapazität von Wasser 1.163WH/kgK
            'Roh_water'         : 995,                      # [kg/m^3] konstante Dichte von Wasser irgendwo zwischen 30 und 40 Grad
            'T_Ref'             : 0,

        },
    }

    if options['Sto']['Size'] == 'Small':
        devs['Sto']['Volume'] = 0.3          # [m³] Small Storage has a capacity of 300l
    elif options['Sto']['Size'] == 'Medium':
        devs['Sto']['Volume'] = 0.5            # [m³] Medium Storage has a capacity of 500l
    elif options['Sto']['Size'] == 'Large':
        devs['Sto']['Volume'] = 0.7         # [m³] Large Storage has a capacity of 1000l
    else:
        print('Please set a supported Storage Size in EasyMPC -> options')

    if options['TWW']['Size'] == 'Medium':
        devs['TWW']['Volume'] = 0.3  # [m³] Medium TWW-Storage has a capacity of 300l
    elif options['TWW']['Size'] == 'Norm':
        devs['TWW']['Volume'] = 0.2  # [m³] Norm TWW-Storage has a capacity of 200l
    elif options['TWW']['Size'] == 'Large':
        devs['TWW']['Volume'] = 0.5  # [m³] Large TWW-Storage has a capacity of 500l
    else:
        print('Please set a supported TWW-Storage Size in EasyMPC -> options')

    return eco, devs, year



def load_time_series(params, options):
    time_step           = params['time_step']
    start_time          = params['start_time']
    prediction_horizon  = params['prediction_horizon']

    # Load inputs
    time_series         = {}


    # Einlesen des Strompreises [€/kWh]
    time_series['c_grid'] = []
    if options['Tariff']['Variable']:
        dC = pd.read_csv('input_data/Opti_Input/VarPowerPrice.csv', skiprows=0)
        time_series['c_grid'] = dC.iloc[:, 0]
    else:
        dC = pd.read_csv('input_data/Opti_Input/FixPowerPrice.csv', skiprows=0)
        time_series['c_grid'] = dC.iloc[:, 0]




    # This is the Input-Data if the Optimization is running with the Original TRY-Data
    if options['WeatherData']['Input_Data'] == 'TRY':

        # Electrical Load Data (Time steps = 1h)
        # [W] Simulierter Bedarf an elektrischer Energie
        time_series['P_EL_Dem']     = np.loadtxt('input_data/Opti_Input/ELHour.txt')

        # Heat Load Data (Time steps = 1h)
        # Simulierter Wärmebedarf für die jeweiligen TRY
        ## Erklärung: Zuerst wird die Datei durch pandas eingelesen
        #  danach wird die erste Spalte (time) gelöscht (iloc)
        #  dann wird die Summe der Zeilen gebildet (sum)
        time_series['Q_Hou_Dem'] = []
        if options['WeatherData']['TRY']    == 'cold':
            dQ = pd.read_csv('input_data/Opti_Input/Q_Dem/Q_Heat_Dem_cold.csv')
        elif options['WeatherData']['TRY']  == 'normal':
            dQ = pd.read_csv('input_data/Opti_Input/Q_Dem/Q_Heat_Dem_normal.csv')
        elif options['WeatherData']['TRY']  == 'warm':
            dQ = pd.read_csv('input_data/Opti_Input/Q_Dem/Q_Heat_Dem_warm.csv')
        else:
            print('Please tell which TRY you want to be simulated in parameter.py -> Options')
            #Anpassung des Q_Heat_Dem sodass der Array nur noch die Summe der Wärmebedarfe der Einzelräume beinhaltet
        dQ                          = dQ.iloc[: , 1:]
        time_series['Q_Hou_Dem']    = dQ.sum(axis=1)




        time_series['T_Air'] = []
            # Einlesen der Außentemperatur abhängig vom ausgewählten TRY
        if options['WeatherData']['TRY']    == "cold":
            dT = pd.read_csv('input_data/Opti_Input/Temperature_Berlin.csv', skiprows=0)
            time_series['T_Air'] = (dT.iloc[:, 3] + 273.15)
        elif options['WeatherData']['TRY']  == 'normal':
            dT = pd.read_csv('input_data/Opti_Input/Temperature_Berlin.csv', skiprows=0)
            time_series['T_Air'] = (dT.iloc[:, 1] + 273.15)
        elif options['WeatherData']['TRY']  == 'warm':
            dT = pd.read_csv('input_data/Opti_Input/Temperature_Berlin.csv', skiprows=0)
            time_series['T_Air'] = (dT.iloc[:, 2] +273.15)


            # Load of Sun Radiation Data
        dH = []
        if options['WeatherData']['TRY']    == 'cold':
            dH = pd.read_csv('input_data/Opti_Input/Global_Radiation_Berlin.csv', skiprows=0)
            time_series['HGloHor'] = dH.iloc[:, 3]
        elif options['WeatherData']['TRY']    == 'normal':
            dH = pd.read_csv('input_data/Opti_Input/Global_Radiation_Berlin.csv', skiprows=0)
            time_series['HGloHor'] = dH.iloc[:, 1]
        elif options['WeatherData']['TRY']    == 'warm':
            dH = pd.read_csv('input_data/Opti_Input/Global_Radiation_Berlin.csv', skiprows=0)
            time_series['HGloHor'] = dH.iloc[:, 2]


    ##        # Load PV-Data
        if options['WeatherData']['TRY']    == 'cold':
             P_PV_list = pd.read_csv('input_data/Opti_Input/P_PV/P_PV_TRY_cold.csv')
            #P_PV_list = pd.read_csv('input_data/Test/P_PV_TRY_cold.csv')
    #        P_PV_list = np.loadtxt('D:/lma-mma/MA_MM_Python/input_data/Test.csv.csv')
        elif options['WeatherData']['TRY']    == 'normal':
            P_PV_list = pd.read_csv('input_data/Opti_Input/P_PV/P_PV_TRY_normal.csv')
     #       P_PV_list = np.loadtxt('D:/lma-mma/MA_MM_Python/input_data/P_PV_TRY_normal_east.txt')
        elif options['WeatherData']['TRY']    == 'warm':
            P_PV_list = pd.read_csv('input_data/Opti_Input/P_PV/P_PV_TRY_warm.csv')
    #        P_PV_list = np.loadtxt('D:/lma-mma/MA_MM_Python/input_data/P_PV_TRY_warm.txt')
        P_PV_list = P_PV_list.values.tolist()
        time_series['P_PV'] = [item for sublist in P_PV_list for item in sublist]

            # Load Wind Speed Data
        dW = []
        if options['WeatherData']['TRY']    == 'cold':
            dW = pd.read_csv('input_data/Opti_Input/Wind_Speed_Berlin.csv', skiprows=0)
            time_series['Win_Speed'] = dW.iloc[:, 3]
        elif options['WeatherData']['TRY']    == 'normal':
            dW = pd.read_csv('input_data/Opti_Input/Wind_Speed_Berlin.csv', skiprows=0)
            time_series['Win_Speed'] = dW.iloc[:, 1]
        elif options['WeatherData']['TRY']    == 'warm':
            dW = pd.read_csv('input_data/Opti_Input/Wind_Speed_Berlin.csv', skiprows=0)
            time_series['Win_Speed'] = dW.iloc[:, 2]


        TWW     = pd.read_csv('input_data/Opti_Input/TWW_Opti.csv', skiprows=0) * 1000
        time_series["Q_TWW_Dem"] = TWW.iloc[:,0]


    elif options['WeatherData']['Input_Data'] == 'Cluster':
        if options['WeatherData']['TRY'] == 'cold':
#            with open("input_data/ClusteredYear/ALT_ClusteredYear_cold.csv", 'r') as file:
#                reader = csv.reader(file)
            File = pd.read_csv('D:/lma-mma/Repos/MA_MM/input_data/ClusteredYear/ClusteredYear_cold.csv', skiprows=0)
            time_series['T_Air']    = File.iloc[:, 0] + 273.15
            time_series['Q_Hou_Dem']= File.iloc[:,1]
            time_series['P_PV']     = File.iloc[:,2]
            time_series['P_EL_Dem'] = File.iloc[:,3]
            time_series['Q_TWW_Dem']= File.iloc[:,4] * 1000

        elif options['WeatherData']['TRY'] == 'normal':
            File = pd.read_csv('input_data/ClusteredYear/ClusteredYear_normal.csv')
            time_series['T_Air']    = File.iloc[:, 0] + 273.15
            time_series['Q_Hou_Dem']= File.iloc[:,1] / 4
            time_series['P_PV']     = File.iloc[:,2]
            time_series['P_EL_Dem'] = File.iloc[:,3]
            time_series['Q_TWW_Dem']= File.iloc[:,4] * 1000

        elif options['WeatherData']['TRY'] == 'warm':
            File = pd.read_csv('input_data/ClusteredYear/ClusteredYear_warm.csv')
            time_series['T_Air']    = File.iloc[:, 0] + 273.15
            time_series['Q_Hou_Dem']= File.iloc[:, 1]
            time_series['P_PV']     = File.iloc[:, 2]
            time_series['P_EL_Dem'] = File.iloc[:, 3]
            time_series['Q_TWW_Dem']= File.iloc[:, 4] * 1000


    elif options['WeatherData']['Input_Data'] == 'Clusterday':
        Tagesnummer = str(options['WeatherData']['DayNumber'])
        if options['WeatherData']['TRY'] == 'cold':
            File = pd.read_csv('D:/lma-mma/Repos/MA_MM/input_data/ClusteredDay/cold/DreiClusterTage_cold_' + Tagesnummer+ '.csv', skiprows=0)
            time_series['T_Air'] = File.iloc[:, 0] + 273.15
            time_series['Q_Hou_Dem'] = File.iloc[:, 1]
            time_series['P_PV'] = File.iloc[:, 2]
            time_series['P_EL_Dem'] = File.iloc[:, 3]
            time_series['Q_TWW_Dem'] = File.iloc[:, 4] * 1000

        elif options['WeatherData']['TRY'] == 'normal':
            File = pd.read_csv('input_data/ClusteredDay/Normal/DreiClusterTage_normal_' + Tagesnummer + '.csv', skiprows=0)
            time_series['T_Air'] = File.iloc[:, 0] + 273.15
            time_series['Q_Hou_Dem'] = File.iloc[:, 1]
            time_series['P_PV'] = File.iloc[:, 2]
            time_series['P_EL_Dem'] = File.iloc[:, 3]
            time_series['Q_TWW_Dem'] = File.iloc[:, 4] * 1000

        elif options['WeatherData']['TRY'] == 'warm':
            File = pd.read_csv('input_data/ClusteredDay/Warm/DreiClusterTage_warm_' + Tagesnummer + '.csv', skiprows=0)
            time_series['T_Air'] = File.iloc[:, 0] + 273.15
            time_series['Q_Hou_Dem'] = File.iloc[:, 1]
            time_series['P_PV'] = File.iloc[:, 2]
            time_series['P_EL_Dem'] = File.iloc[:, 3]
            time_series['Q_TWW_Dem'] = File.iloc[:, 4] * 1000
    else:
        print("Please tell which TRY should the Optimization be running for")

    if options['Sto']['Type'] == 'Seperated':
        if options['WeatherData']['TRY'] == 'cold':
            TWW = pd.read_csv('D:/lma-mma/Repos/MA_MM/input_data/ClusteredYear/ClusteredYear_cold.csv', skiprows=0)
        elif options['WeatherData']['TRY'] == 'normal':
            TWW = pd.read_csv('D:/lma-mma/Repos/MA_MM/input_data/ClusteredYear/ClusteredYear_normal.csv', skiprows=0)
        elif options['WeatherData']['TRY'] == 'warm':
            TWW = pd.read_csv('D:/lma-mma/Repos/MA_MM/input_data/ClusteredYear/ClusteredYear_warm.csv', skiprows=0)
        else:
            pass

        time_series["Q_TWW_Dem"] = TWW.iloc[:, 4] * 1000




    return time_series

