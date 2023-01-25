import numpy as np
import pandas as pd

#from Optimization import T_Hou_delta_max


def load_params(params):

    # Set time parameter for year
    year = {
        'start_time_of_months': [0, 744, 1416, 2160, 2880, 3624, 4344, 5088, 5832, 6552, 7296, 8016],   # hours
        'length_of_months': [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]                            # days
    }


    # Set economic parameters
# todo Einheiten der Kosten Checken
    eco = {
        'costs'     : {
            #todo: Array für die Strompreise erstellen
            'c_grid_var_t'  : 1,                      # [Euro/kWh] Electricity Price if option with variable el price (Variabler Stropreis)
            'c_grid_dem'    : 0.35,                   # [Euro/kWh] Electricity Price if option 'fix' el price (Fester Strompreis)
            'c_payment'     : 0.06,                   # [Euro/kWh] Feed in tariff (Einspeisevergütung)
            'c_comfort'     : 1000,
        }
    }
    # Set component parameters

    devs = {
    # Set Heat Storage parameter
        'Sto'   : {
            'T_Sto_min' : 18 + 273.15,                   # [K] Minimum temperature of storage
            'T_Sto_max' : 95 + 273.15,                  # [K] Maximum temperature of storage
            'T_Sto_Env' : 18 + 273.15,                  # [K] Environmental temperature of storage in basement or utility room
            'T_Sto_Init': 70 + 273.15,                  # [K] initial Storage Temperature for Optimization
            'Volume'    : 0.3,                          # [m³] Volume of thermal Storage Set in Dymola
            'U_Sto'     : 30,                           # [W/m²K] Heat Transfer Coefficient of Storage (Wärmeübergangkoeffizient des Speichers)
            'T_Kalt'    : 18 + 273.15,                  # [K] Coldest Temperature of Water in Storage as this is the constant Basement Temperature
            #todo richtiger Wert für A_Sto
            'A_Sto'     : 2,                            # [m²] Surface of Heat Storage

        },

    # Set Heat Pump parameter
        'HP'    : {
            'Q_HP_Max'      : 10000,                        # [W]    Maximum Heat Power of Heat Pump
            'T_HP_VL_1'     : 35 + 273.15,                  # [K]    Constant Flow Temperature from HP to Storage in Mode 1
            'T_HP_VL_2'     : 70 + 273.15,                  # [K]    Constant Flow Temperature from HP to Storage in Mode 2
            'T_HP_VL_3'     : 20 + 273.15,
            'm_flow_HP'     : 80 / 3600,                    # [kg/s] Constant Heat flow of HP if HP is running
            'eta_HP'        : 0.4,                          # [-]    Gütegrad HP
            'Q_HP_Min'      : 0                             # [W]    Minimum Heat power of HP
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
            # TODO: vernünftiger Wert für m_flow_Hou
            'm_flow_Hou'        :     100 / 3600,           # [kg/s] Constant Mass flow from Storage to House

        },

        # Set natural Constant and other constants given by nature
        'Nature'    : {
            'c_w_water'         : 4180,                     # [Ws/kgK] Spezifische Wärmekapazität von Wasser 1.163WH/kgK
            'Roh_water'         : 995,                      # [kg/m^3] konstante Dichte von Wasser irgendwo zwischen 30 und 40 Grad


        },
    }


    return eco, devs, year



def load_time_series(params, options):
    global dQ
    time_step           = params['time_step']
    start_time          = params['start_time']
    prediction_horizon  = params['prediction_horizon']

        # Load inputs
    time_series         = {}

        # Electrical Load Data (Time steps = 1h)
# [W] Simulierter Bedarf an elektrischer Energie
    time_series['P_EL_Dem']     = np.loadtxt('D:/lma-mma/Repos/MA_MM/input_data/ELHour.txt') * 1000



        # Heat Load Data (Time steps = 1h)
# Simulierter Wärmebedarf für die jeweiligen TRY
        ## Erklärung: Zuerst wird die Datei durch pandas eingelesen
        #  danach wird die erste Spalte (time) gelöscht (iloc)
        #  dann wird die Summe der Zeilen gebildet (sum)
    time_series['Q_Hou_Dem'] = []
    if options['WeatherData']['TRY']    == 'cold':
        dQ = pd.read_csv("D:/lma-mma/Repos/MA_MM/input_data/Q_Dem/Q_Heat_Dem_cold.csv")
    elif options['WeatherData']['TRY']  == 'normal':
        dQ = pd.read_csv("D:/lma-mma/MA_MM_Python/input_data/Q_Dem/Q_Heat_Dem_normal.csv")
    elif options['WeatherData']['TRY']  == 'warm':
        dQ = pd.read_csv("D:/lma-mma/MA_MM_Python/input_data/Q_Dem/Q_Heat_Dem_warm.csv")
    else:
        print('Please tell which TRY you want to be simulated in parameter.py -> Options')
        #Anpassung des Q_Heat_Dem sodass der Array nur noch die Summe der Wärmebedarfe der Einzelräume beinhaltet
    dQ                          = dQ.iloc[: , 1:]
    time_series['Q_Hou_Dem']    = dQ.sum(axis=1)

# Einlesen des Strompreises
    time_series['c_grid'] = []
    if options['Tariff']['Variable']:
        dC = pd.read_csv('input_data/VariablePowerPrice.csv', skiprows=0)
        time_series['c_grid'] = dC.iloc[:, 0]
    else:
        dC = pd.read_csv('input_data/FixPowerPrice.csv', skiprows=0)
        time_series['c_grid'] = dC.iloc[:,0]


    time_series['T_Air'] = []
        # Einlesen der Außentemperatur abhängig vom ausgewählten TRY
    if options['WeatherData']['TRY']    == "cold":
        dT = pd.read_csv('input_data/Temperature_Berlin.csv', skiprows=0)
 #       time_series['T_Air'] = dT.iloc[:, 3]
        time_series['T_Air'] = dT.iloc[:, 3]
    elif options['WeatherData']['TRY']  == 'normal':
        dT = pd.read_csv('input_data/Temperature_Berlin.csv', skiprows=0)
        time_series['T_Air'] = dT.iloc[:, 1]
    elif options['WeatherData']['TRY']  == 'warm':
        dT = pd.read_csv('input_data/Temperature_Berlin.csv', skiprows=0)
        time_series['T_Air'] = dT.iloc[:, 2]

#    time_series['T_Air'] = dT.sum(axis=1)
#    time_series['T_Air'] = [item for sublist in dT for item in sublist]

        # Load of Sun Radiation Data
    dH = []
    if options['WeatherData']['TRY']    == 'cold':
        dH = pd.read_csv('input_data/Global_Radiation_Berlin.csv', skiprows=0)
        time_series['HGloHor'] = dH.iloc[:, 3]
    elif options['WeatherData']['TRY']    == 'normal':
        dH = pd.read_csv('input_data/Global_Radiation_Berlin.csv', skiprows=0)
        time_series['HGloHor'] = dH.iloc[:, 1]
    elif options['WeatherData']['TRY']    == 'warm':
        dH = pd.read_csv('input_data/Global_Radiation_Berlin.csv', skiprows=0)
        time_series['HGloHor'] = dH.iloc[:, 2]


##        # Load PV-Data
    if options['WeatherData']['TRY']    == 'cold':
        P_PV_list = pd.read_csv('input_data/P_PV_TRY_cold.csv')
#        P_PV_list = np.loadtxt('D:/lma-mma/MA_MM_Python/input_data/P_PV_TRY_cold.csv')
    elif options['WeatherData']['TRY']    == 'normal':
        P_PV_list = pd.read_csv('input_data/P_PV_TRY_normal.csv')
 #       P_PV_list = np.loadtxt('D:/lma-mma/MA_MM_Python/input_data/P_PV_TRY_normal_east.txt')
    elif options['WeatherData']['TRY']    == 'warm':
        P_PV_list = pd.read_csv('input_data/P_PV_TRY_warm.csv')
#        P_PV_list = np.loadtxt('D:/lma-mma/MA_MM_Python/input_data/P_PV_TRY_warm.txt')
    P_PV_list = P_PV_list.values.tolist()
    time_series['P_PV'] = [item for sublist in P_PV_list for item in sublist]

#    P_PV = np.loadtxt('input_data/P_PV_TRY_cold.csv', delimiter=';')
#    time_series['P_PV'] = np.zeros([prediction_horizon + 1])
#    for t in range(prediction_horizon + 1):
#        time_series['P_PV'] = P_PV[t]


        # Load Wind Speed Data
    dW = []
    if options['WeatherData']['TRY']    == 'cold':
        dW = pd.read_csv('input_data/Wind_Speed_Berlin.csv', skiprows=0)
        time_series['Win_Speed'] = dW.iloc[:, 3]
    elif options['WeatherData']['TRY']    == 'normal':
        dW = pd.read_csv('input_data/Wind_Speed_Berlin.csv', skiprows=0)
        time_series['Win_Speed'] = dW.iloc[:, 1]
    elif options['WeatherData']['TRY']    == 'warm':
        dW = pd.read_csv('input_data/Wind_Speed_Berlin.csv', skiprows=0)
        time_series['Win_Speed'] = dW.iloc[:, 2]

        # Costs of Power supply by the grid if option is fix or variable
        #Todo Varialber Strompreis Daten hinterlegen
 #       if options['Tariff']['Variable']:
#       time_series['c_grid_var']




        # PV Data
#    if options['time_step']:
                #Entweder es werden die Daten der PV-Erzeugung Stundengenau abgebildet, oder viertelstundengenau
                # Stundengenau: time_step = 0.25 (h)
                # Stundengenau_ time_step = 1 (h)
                # Startzeit immer bei 0

    return time_series

