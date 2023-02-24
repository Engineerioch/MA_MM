
import EasyModell as mpc
import parameter as parameters
from parameter import load_params
import pickle
import os
import csv
from datetime import datetime
import copy
import matplotlib.pyplot as plt


options = {
    'Tariff'        :   {'Variable'          : False},   # [-] TRUE = 'variable' or FALSE = 'fix' -> Decides if Powerprice is variable or fix
#    'time_step'     :   {'time_variable'        : ''},
    'WeatherData':   {'TRY'                  : 'cold'       # [-] 'warm'    -> warmes TRY 2015
                                                            # [-] 'normal'  -> normales TRY 2015
                                                    },      # [-] 'cold' -> kaltes TRY 2015
    'Solve'         :   {'MIP_gap'             : 0.01,
                        'TimeLimit'            : 60,
                        'TimeLimitMax'         : 35491348,
                        'type'                 : 'gurobi',
                         },

    'PV'            :   {'PV_factor'           : 1.0,      # Rescale PV- Generation P_PV = n_Mod (default: 750) * 330 W * PV_factor
                         },


    'Sto'           : {'Size'                   : 'Small',   # Define Storage size: Small = 300l, Medium = 500l, Large = 1000l
                        'Type'                  : 'Puffer',  # Define what type of storage one has (Puffer, Kombi, Seperated)
                       },
    'TWW'           : {
                        'Size'                  : 'Norm',   # Define the Size of the TWW-Storage Size
    },

### Location of the Single Family House ###
    'Location'      :   {'lat'                  : 52.519*2*3.14/360,            # [°]   Latitude Berlin
                         'lon'                  : 13.408*2*3.14/360,            # [°]   Longitude Berlin
                         'roof_area'            : 35,                           # [m²]  Roof Area
                         'til'                  : 15 * 2 * 3.14 / 360,          # [°]   Dachneigung
                         'azi_1'                : 90 * (2 * 3.14) / (360),      # [°]   Orientation of roof sides (0: south, -: East, +: West)
                         'azi_2'                : -90 * (2 * 3.14) / (360)      # [°]   Orientation of roof sides (0: south, -: East, +: West)
                         },
}

start_time = 24*15                  # start time in hours
time_step = 0.5                   # step size in hours
total_runtime = 48            # Iterationsschritte       -> Sollte durch 24 teilbar sein
control_horizon = 2             #
prediction_horizon = 8

params_opti = {
    'prediction_horizon'    : prediction_horizon,
    'control_horizon'       : control_horizon,
    'time_step'             : time_step,
    'start_time'            : start_time,
    'total_runtime'         : total_runtime,
}
if control_horizon >= params_opti['prediction_horizon']:
    print('Control Horizon has to be smaller than the prediction horizon')

end = 0
# Define paths and directories for results
path_file = str(os.path.dirname(os.path.realpath(__file__)))
#print(path_file)
dir_results = path_file + "/Results/" + str(datetime.now().strftime('%Y-%m-%d'))
if not os.path.exists(dir_results):
    os.makedirs(dir_results)


# Load Parameter
eco, devs, year = parameters.load_params(options, params_opti)

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
#    'solving_time': [],
    'Mode'              : [],
    'Q_HP'              : [],
    'Q_Penalty': [],
    'Q_Hou': [],
    'Q_Hou_Dem': [],
    'Q_Sto_Power_max': [],
    'T_TWW': [],
    'Q_TWW_Max': [],
    'Q_TWW_Dem': [],

    'T_Sto': [],
    'Q_Sto_Loss'        : [],
    'Q_Sto_Energy'      : [],

    'COP_Carnot': [],
    'COP_HP':[],
    'T_Air': [],
    'T_Mean': [],
    'c_el_power': [],
    'c_heat_power': [],
    'total_costs_ch': [],
    'P_EL'              : [],
    'P_EL_Dem'          : [],
    'P_EL_HP'           : [],
    'P_PV'              : [],
    'd_Temp_HP': [],
    'd_Temp_Hou': [],
    'c_grid': [],

    'c_penalty': [],
    'c_revenue': [],
    'c_cost': [],
    'c_el_cost_ch': [],
    'total_costs_ph':[],

    'P_HP_1'            : [],
    'P_HP_2'            : [],


    'T_HP_VL'           : [],

    'HP_off'            : [],
    'HP_mode1'          : [],
    'HP_mode2'          : [],
    'HP_TWW'            : [],
    'COP_1'             : [],
    'COP_2'             : [],
##    'c_grid': [],


    'Q_TWW_Loss'        : [],
    }

save_results = copy.deepcopy(save_optim_results)

# Time Settings
for iter in range(int(params_opti['total_runtime']/params_opti['control_horizon'])):

    time_series = parameters.load_time_series(params_opti, options)
    print("======================== iteration = " +     str(iter) + " ========================")
    print('New start time is:', params_opti['start_time'])
    if iter == 0:
        T_Sto_Init = devs['Sto']['T_Sto_Init']
        T_TWW_Init = devs['TWW']['T_TWW_Init']
    else:
        T_Sto_Init = save_results['T_Sto'][iter-1][end]
        T_TWW_Init = save_results['T_TWW'][iter-1][end]


    results_optim = mpc.runeasyModell(params_opti, options, eco, time_series, devs, iter, T_Sto_Init, T_TWW_Init)
    print('Optimization is running....')



    params_opti['start_time'] = params_opti['start_time'] + params_opti['control_horizon']
    end = int(params_opti['control_horizon'] * (1/ time_step)) - 1



    for res in save_results:
       # for t in range(params_opti['prediction_horizon']):

            save_results[res].append(results_optim[res])


show = 'Save_Results'

if show == 'HP':
    print('Mode')
    print(save_results['Mode'])
    print('Q_HP')
    print(save_results['Q_HP'])
    print('T_HP_VL')
    print(save_results['T_HP_VL'])
    print('T_HP_RL')
    print(save_results['T_HP_RL'])
    print('T_Sto')
    print(save_results['T_Sto'])
    print('T_Air')
    print(save_results['T_Air'])
elif show == 'Sto':
    print('T_Sto')
    print(save_results['T_Sto'])
    print('Q_Sto_Energy')
    print(save_results['Q_Sto_Energy'])
    print('Q_Sto_Power')
    print(save_results['Q_Sto_Power'])
    print('Q_Sto_Power_Max')
    print(save_results['Q_Sto_Power_Max'])
elif show == 'Power':
    print('P_EL')
    print(save_results['P_EL'])
    print('P_PV')
    print(save_results['P_PV'])
    print('P_EL_HP')
    print(save_results['P_EL_HP'])
elif show == 'costs':
#    print('c_grid')
#    print(save_optim_results_opti['c_grid'])
    print('c_power')
    print(save_results['c_power'])
    print('c_revenue')
    print(save_results['c_revenue'])
    print('c_penalty')
    print(save_results['c_penalty'])
    print('total_costs')
    print(save_results['total_costs'])
elif show == 'Hou':
    print('Q_Hou')
    print(save_results['Q_Hou'])
    print('T_Hou_VL')
    print(save_results['T_Hou_VL'])
    print('T_Hou_RL')
    print(save_results['T_Hou_RL'])
    print('Q_Penalty')
    print(save_results['Q_Penalty'])
elif show == 'Heat':
    print('Q_HP')
    print(save_results['Q_HP'])
    print('Q_Penalty')
    print(save_results['Q_Penalty'])
    print('Q_Sto_Power')
    print(save_results['Q_Sto_Power'])
    print('Q_Hou')
    print(save_results['Q_Hou'])
    print('Q_Hou_Dem')
    print(save_results['Q_Hou_Dem'])
    print('T_Mean')
    print(save_results['T_Mean'])
    print('T_Sto')
    print(save_results['T_Sto'])
elif show == 'all':

    zh




elif show== 'Save_Results':

    time_to_save = [0]
    ende = int(start_time + params_opti['total_runtime'])
    for i in range(start_time, ende + 1):
        for j in range(0, int(1 / time_step)):
            time_to_save.append(i + (j * time_step))

    with open('D:/lma-mma/Repos/MA_MM/Results/Real_Results/results.csv', 'w', newline='') as csvfile:

        # Create a CSV writer object
        writer = csv.writer(csvfile)

        # Write the headers to the first row
        writer.writerow(time_to_save)
        for key, values in save_results.items():
            row = [key] + sum(values, [])
            writer.writerow(row)
#    writer.close()

    dir_results = 'D:/lma-mma/Repos/MA_MM/Results'
    options_file = dir_results + '/options.txt'
    all_options = [options, params_opti]
    all_options_names = ['options', 'params_opti']
    pickle.dump(all_options, open(options_file, "wb"))
    with open(options_file, "w") as file:
        for key in all_options:
            file.write(all_options_names[all_options.index(key)])
            file.write('\n')
            for x in key:
                file.write(str(x) + "=")
                file.write(str(key[x]))
                file.write('\n')
            file.write('\n')
        file.close()

    devs_file = dir_results + '/devs.txt'
    all_devs = [devs, eco]
    all_devs_names = ['devs', 'eco']
    pickle.dump(all_devs, open(devs_file, "wb"))
    with open(devs_file, "w") as file_devs:
       for key in all_devs:
           file_devs.write(all_devs_names[all_devs.index(key)])
           file_devs.write('\n')
           for x in key:
               file_devs.write(str(x) + "=")
               file_devs.write(str(key[x]))
               file_devs.write('\n')
           file_devs.write('\n')
       file_devs.close()





else:
    print(save_results['T_Air'])
#    print(save_results['T_Mean'])
