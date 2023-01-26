
import Optimization as mpc
import parameter as parameters
from parameter import load_params
import pickle
import os
import numpy as np
from datetime import datetime
import copy



options = {
    'Tariff'        :   {'Variable'          : False},   # [-] TRUE = 'variable' or FALSE = 'fix' -> Decides if Powerprice is variable or fix
#    'time_step'     :   {'time_variable'        : ''},
    'WeatherData':   {'TRY'                  : 'cold'       # [-] 'warm'    -> warmes TRY 2015
                                                            # [-] 'normal'  -> normales TRY 2015
                                                    },      # [-] 'cold' -> kaltes TRY 2015
    'Solve'         :   {'MIP_gap'             : 1,
                        'TimeLimit'            : 60,
                        'TimeLimitMax'         : 35491348,
                        'type'                 : 'gurobi',
                         },

    'PV'            :   {'PV_factor'           : 1.0,      # Rescale PV- Generation P_PV = n_Mod (default: 750) * 330 W * PV_factor
                         },

    'Initial'       : {'T_HP_VL_Init'           : 35 + 273.15 },


### Location of the Single Family House ###
    'Location'      :   {'lat'                  : 52.519*2*3.14/360,            # [°]   Latitude Berlin
                         'lon'                  : 13.408*2*3.14/360,            # [°]   Longitude Berlin
                         'roof_area'            : 35,                           # [m²]  Roof Area
                         'til'                  : 15 * 2 * 3.14 / 360,          # [°]   Dachneigung
                         'azi_1'                : 90 * (2 * 3.14) / (360),      # [°]   Orientation of roof sides (0: south, -: East, +: West)
                         'azi_2'                : -90 * (2 * 3.14) / (360)      # [°]   Orientation of roof sides (0: south, -: East, +: West)
                         },
}
#prediction_horizon = 72
start_time = 0
time_step = 1
total_runtime = 10           # Iterationsschritte
control_horizon = 10
params_opti = {
    'prediction_horizon'    : 10,
    'control_horizon'       : control_horizon,
    'time_step'             : time_step,
    'start_time'            : start_time,
    'total_runtime'         : total_runtime,
}

# Define paths and directories for results
path_file = str(os.path.dirname(os.path.realpath(__file__)))
#print(path_file)
dir_results = path_file + "/Results/" + str(datetime.now().strftime('%Y-%m-%d'))
if not os.path.exists(dir_results):
    os.makedirs(dir_results)


# Load Parameter
eco, devs, year = parameters.load_params(params_opti)

# save paramater settings of devices an economic assumptions to pickle file
devs_file = dir_results + '/devs.pkl'
eco_file = dir_results + '/eco.pkl'
pickle.dump(devs, open(devs_file, "wb"))
pickle.dump(eco, open(eco_file, "wb"))

# Save solving time of iterations
solving_time = {
    'solving_time':[]
}


# Define variables to be saved
save_optim_results = {
    'solving_time': [],
    'Mode 0': [],
    'Mode 1': [],
    'Mode 2': [],
    'Q_Sto': [],
    'Q_HP': [],
    'Q_Hou_Dem': [],
    'Q_Hou': [],
    'Q_Sto_Loss': [],
    'P_EL': [],
    'P_EL_HP': [],
    'P_EL_Dem': [],
    'P_PV_Grid': [],
    'P_PV': [],
    'COP_Carnot': [],
    'COP_HP': [],
    'T_Air_Input' : [],
    'T_Air': [],
    'T_Sto': [],
    'T_HP_VL': [],
    'T_HP_RL': [],
    'T_Hou_VL': [],
    'T_Hou_RL': [],
    'c_total': [],
    'c_grid' : [],
#    'c_revenue': [],
    'total_costs':  [],
    }

save_optim_results_opti = copy.deepcopy(save_optim_results)

# Time Settings
for iter in range(int(params_opti['total_runtime']/params_opti['control_horizon'])):
    print("======================== iteration = " +     str(iter) + " ========================")
    print('New start time is:', params_opti['start_time'])
    params_opti['start_time'] = params_opti['start_time'] + params_opti['control_horizon']
    end = (iter) * int(params_opti['control_horizon'] / params_opti['time_step'])
    time_series = parameters.load_time_series(params_opti, options)

    print('Optimization is running....')
    results_optim = mpc.run_MPC(params_opti, options, eco, time_series, devs, end)


    for res in save_optim_results_opti:
        for t in range(params_opti['prediction_horizon']):
            save_optim_results_opti[res].append(results_optim[res])

    # Set start time for next iteration



# Load Time Series for prediction horizon
#time_series = parameters.load_time_series(options)

#print(save_optim_results_opti['P_PV'])
#print(save_optim_results_opti['T_Air'])
#print(save_optim_results_opti['P_EL_Dem'])



#print(save_optim_results_opti['T_Sto')
# print("Q_Hou =")
#print(save_optim_results_opti['Q_Hou']) # -> Schaut gut aus

#print('P_PV =')
#print(save_optim_results_opti['P_PV']) # -> Schaut gut aus

#print('T_Air =')
#print(save_optim_results_opti['T_Air']) # Abfuck
#print('P_EL_Dem=')
#print(save_optim_results_opti['P_EL_Dem']) #-> Werte werden gelesen, aber falsch?
#print(save_optim_results_opti['T_Air_Input'])
#print(save_optim_results_opti['T_Sto'])
#print(save_optim_results_opti['T_Air'])
#print(save_optim_results_opti['P_EL'])
#print(save_optim_results_opti['Q_Hou'])