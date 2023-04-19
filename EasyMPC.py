
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


    'Solve'         :   {'MIP_gap'             : 0.03,
                        'TimeLimit'            : 30,
                        'TimeLimitMax'         : 120,
                        'type'                 : 'gurobi',
                         },

    'PV'            :   {'PV_factor'           : 1.0,      # Rescale PV- Generation P_PV = n_Mod (default: 750) * 330 W * PV_factor
                         },

    'Tariff'        :   {'Variable'          : False},   # [-] TRUE = 'variable' or FALSE = 'fix' -> Decides if Powerprice is variable or fix


    'WeatherData':   {'TRY'                  : 'cold',       # [-] 'warm'    -> warmes TRY 2015
                                                            # [-] 'normal'  -> normales TRY 2015
                                                            # [-] 'cold' -> kaltes TRY 2015
                        'Input_Data' : 'TRY',               # Which Input-Data should be used: TRY = Data from original TRY
                                                            # Cluster = Clustered Data
                                                            # Clusterday = 3 same Clusterdays in a row
                        'DayNumber' : 5
                        },
    'Sto'           : {'Size'                   : 'Small',   # Define Storage size: Small = 300l, Medium = 500l, Large = 1000l
                        'Type'                  : 'Seperated',  # Define what type of storage one has (Puffer, Kombi, Seperated)
                       },

    'TWW'           : {
                        'Size'                  : 'Norm',   # Define the Size of the TWW-Storage Size
                        },
    }

start_time = 0                    # start time in hours
time_step = 0.25                     # step size in hours
total_runtime = 744                  # Iterationsschritte -> Sollte durch 24 teilbar sein
control_horizon = 4
prediction_horizon = 24

if options['WeatherData']['Input_Data'] == 'Clusterday':
    total_runtime = 48
else:
    pass

params_opti = {
    'prediction_horizon'    : prediction_horizon,
    'control_horizon'       : control_horizon,
    'time_step'             : time_step,
    'start_time'            : start_time,
    'total_runtime'         : total_runtime,
    'safe_start_time'       : start_time,           # only for saving
}

if control_horizon >= params_opti['prediction_horizon']:
    print('Control Horizon has to be smaller than the prediction horizon')

end = 0
# Define paths and directories for results
path_file = str(os.path.dirname(os.path.realpath(__file__)))
#print(path_file)



# Load Parameter
eco, devs, year = parameters.load_params(options, params_opti)

# save paramater settings of devices an economic assumptions to pickle file
##devs_file = dir_results + '/devs.pkl'
##eco_file = dir_results + '/eco.pkl'
##pickle.dump(devs, open(devs_file, "wb"))
##pickle.dump(eco, open(eco_file, "wb"))

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
  #  'Q_TWW_Max': [],
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
    'Q_TWW_Loss'        : [],
    'Q_Penalty_TWW'     : [],
    'TWW_Penalty'       : [],
    }

save_results = copy.deepcopy(save_optim_results)


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
        save_results[res].append(results_optim[res])


show = 'Save_Results'

if show == 'HP':
    print('Mode')


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
        #writer.close()

    # Create a file which saves only the Modes and one which only saves the Input-Data
    if options["WeatherData"]["Input_Data"] == "TRY":
        Input_type = '_TRY'
        if options['WeatherData']['TRY'] == 'cold':
            TRY_name = '_cold'
        elif options['WeatherData']['TRY'] == 'normal':
            TRY_name = '_normal'
        elif options['WeatherData']['TRY'] == 'warm':
            TRY_name = '_warm'
    elif options["WeatherData"]["Input_Data"] == "Cluster":
        Input_type = '_Cluster'
        if options['WeatherData']['TRY'] == 'cold':
            TRY_name = '_cold'
        elif options['WeatherData']['TRY'] == 'normal':
            TRY_name = '_normal'
        elif options['WeatherData']['TRY'] == 'warm':
            TRY_name = '_warm'
    else:
        Input_type = '_Clusterday_' + str(options["WeatherData"]["DayNumber"])
        if options['WeatherData']['TRY'] == 'cold':
            TRY_name = '_cold'
        elif options['WeatherData']['TRY'] == 'normal':
            TRY_name = '_normal'
        elif options['WeatherData']['TRY'] == 'warm':
            TRY_name = '_warm'

    if options['Sto']['Type'] == 'Puffer':
        Sto_name = '_Puffer'
    else:
        Sto_name = '_TWW'

    if options['Tariff']['Variable']:
        PowerPrice = '_Var'
    else:
        PowerPrice = '_Fix'

    if options['Sto']['Size'] == 'Small':
        Sto_type = '_Small'
    elif options['Sto']['Size'] == 'Medium':
        Sto_type = '_Medium'
    elif options['Sto']['Size'] == 'Large':
        Sto_type = '_Large'

    if options['TWW']['Size'] == 'Norm':
        TWW_type = '_Norm'
    elif options['TWW']['Size'] == 'Medium':
        TWW_type = '_Medium'
    elif options['TWW']['Size'] == 'Large':
        TWW_type = '_Large'

    timestep = str(time_step)
    ts = timestep.replace('.', '')

    # Define and Path to save the files
    if options['Sto']['Type'] == 'Puffer':
        CSVnames = str(start_time) + '_' + ts + '_' + str(total_runtime) + '_' + str(
            control_horizon) + '_' + str(prediction_horizon) + Input_type + TRY_name + PowerPrice + Sto_name + Sto_type + '.csv'
        TXTnames = str(start_time) + '_' + ts + '_' + str(total_runtime) + '_' + str(
            control_horizon) + '_' + str(prediction_horizon) + Input_type + TRY_name + PowerPrice + Sto_name + Sto_type + '.txt'
        if options['WeatherData']['Input_Data'] == 'Clusterday':
            Ordner = 'Results/Optimierung/Puffer/Clusterday/'
        else:
            Ordner = 'Results/Optimierung/Puffer/'

    else:
        CSVnames = str(start_time) + '_' + ts + '_' + str(total_runtime) + '_' + str(
            control_horizon) + '_' + str(prediction_horizon) + Input_type + TRY_name + PowerPrice + Sto_name + Sto_type + TWW_type + '.csv'
        TXTnames = str(start_time) + '_' + ts + '_' + str(total_runtime) + '_' + str(
            control_horizon) + '_' + str(prediction_horizon) + Input_type + TRY_name + PowerPrice + Sto_name + Sto_type + TWW_type + '.txt'
        Ordner = 'Results/Optimierung/TWW/'
        if options['WeatherData']['Input_Data'] == 'Clusterday':
            Ordner = 'Results/Optimierung/TWW/Clusterday/'
        else:
            Ordner = 'Results/Optimierung/TWW/'

    Modefile = (Ordner +'Modes_' + CSVnames)
    Datafile = (Ordner + 'Data_' + CSVnames)
    Inputfile = (Ordner + 'Input_' + CSVnames)
    Optionsfile = (Ordner + 'Options_' + TXTnames)
    Devsfile = (Ordner + 'Devs_' + TXTnames)
    Mode0_File = (Ordner + 'Mode0_' + CSVnames)
    Mode1_File = (Ordner + 'Mode1_' + CSVnames)
    Mode2_File = (Ordner + 'Mode2_' + CSVnames)
    Mode3_File = (Ordner + 'Mode3_' + CSVnames)
    dir_results = Ordner
    if not os.path.exists(dir_results):
        os.makedirs(dir_results)

    # Define which Data should be saved in which file and safe them directly
    # Create lists of Data
    T_Air = [val for sublist in save_results["T_Air"] for val in sublist]
    Q_Hou = [val for sublist in save_results["Q_Hou_Dem"] for val in sublist]
    P_PV = [val for sublist in save_results["P_PV"] for val in sublist]
    P_EL_Dem = [val for sublist in save_results["P_EL_Dem"] for val in sublist]
    T_Sto = [val for sublist in save_results["T_Sto"] for val in sublist]
    c_grid = [val for sublist in save_results["c_grid"] for val in sublist]
    COP_1 =[val for sublist in save_results["COP_1"] for val in sublist]
    COP_2 = [val for sublist in save_results["COP_2"] for val in sublist]
    Q_HP = [val for sublist in save_results["Q_HP"] for val in sublist]
    Q_Penalty = [val for sublist in save_results["Q_Penalty"] for val in sublist]
    T_Mean = [val for sublist in save_results["T_Mean"] for val in sublist]
    Modus = [val for sublist in save_results["Mode"] for val in sublist]
    HP_off = [val for sublist in save_results["HP_off"] for val in sublist]
    HP_1 = [val for sublist in save_results["HP_mode1"] for val in sublist]
    HP_2 = [val for sublist in save_results["HP_mode2"] for val in sublist]
    c_grid = [val for sublist in save_results["c_grid"] for val in sublist]
    if options['Sto']['Type'] == 'Seperated':
        T_TWW = [val for sublist in save_results["T_TWW"] for val in sublist]
        Q_TWW = [val for sublist in save_results["Q_TWW_Dem"] for val in sublist]
        HP_3  = [val for sublist in save_results["HP_TWW"] for val in sublist]
    else:
        pass
    # Create zip lists of data
    if options['Sto']['Type'] == 'Puffer':
        Data = list(zip(T_Air, Q_Hou, P_PV, P_EL_Dem, T_Mean, c_grid, T_Sto, COP_1, COP_2, Q_Penalty))
        Input = list(zip(T_Air, Q_Hou, P_PV, P_EL_Dem, T_Mean, c_grid))
    else:
        Data = list(zip(T_Air, Q_Hou, P_PV, P_EL_Dem, T_Mean, c_grid, Q_TWW, T_Sto, T_TWW, COP_1, COP_2, Q_HP,  Q_Penalty))
        Input = list(zip(T_Air, Q_Hou, P_PV, P_EL_Dem, T_Mean, c_grid, Q_TWW))

    with open(Modefile, "w", newline="") as m:
        writer = csv.writer(m)
        for val in Modus:
            writer.writerow([val])

    with open(Datafile, "w", newline="") as D:
        writer = csv.writer(D)
        for values in Data:
            writer.writerow(values)

    with open(Inputfile, "w", newline="") as I:
        writer = csv.writer(I)
        for values in Input:
            writer.writerow(values)

    dir_results = Ordner
    if not os.path.exists(dir_results):
        os.makedirs(dir_results)

    dir_results = Ordner
    options_file = Optionsfile
    all_options = [options, params_opti]
    all_options_names = ['options', 'params_opti']
    pickle.dump(all_options, open(options_file, "wb"))
    with open(options_file, "w") as file:
        for key in all_options:
            file.write(all_options_names[all_options.index(key)])
            file.write(all_options_names[all_options.index(key)])
            file.write('\n')
            for x in key:
                file.write(str(x) + "=")
                file.write(str(key[x]))
                file.write('\n')
            file.write('\n')
        file.close()

    devs_file = Devsfile
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


    with open(Mode0_File, "w", newline="") as m:
        writer = csv.writer(m)
        for val in HP_off:
            writer.writerow([val])

    with open(Mode1_File, "w", newline="") as m:
        writer = csv.writer(m)
        for val in HP_1:
            writer.writerow([val])

    with open(Mode2_File, "w", newline="") as m:
        writer = csv.writer(m)
        for val in HP_2:
            writer.writerow([val])

    if options['Sto']['Type'] == 'Seperated':
        with open(Mode3_File, "w", newline="") as m:
            writer = csv.writer(m)
            for val in HP_3:
                writer.writerow([val])
    else:
        pass

else:
    print(save_results['T_Air'])
#    print(save_results['T_Mean'])

