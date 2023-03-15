#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: she
"""


# import python packages
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
import pickle as pickle

import clustering_medoid as clustering
from sklearn.metrics import r2_score


raw_inputs = {}

TRY = 'cold'
Tariff = 'Fix'

#%% Read inputs for each specific TRY

RG = []

# Import the Data according to the choosen TRY in EasyMPC -> options:

if TRY == 'cold':
    #options['WeatherData']['TRY'] == 'cold':
    raw_inputs["T_Air"] = np.loadtxt("input_data/Medoid/temperature_cold.csv")
    raw_inputs["P_PV"] = np.maximum(0, np.loadtxt("input_data/Medoid/P_PV_TRY_cold.csv"))
    raw_inputs["Q_Hou_Dem"] = np.maximum(0, np.loadtxt("input_data/Medoid/Q_Heat_Dem_cold.csv"))
    raw_inputs['Wind_Speed'] = np.maximum(0, np.loadtxt("input_data/Medoid/Wind_Speed_cold.csv"))
    raw_inputs['Rad_Glo'] = np.maximum(0, np.loadtxt("input_data/Medoid/Global_Radiation_cold.csv"))

elif TRY == 'normal':
    raw_inputs["T_Air"] = np.loadtxt("input_data/Medoid/temperature_normal.csv")
    raw_inputs["P_PV"] = np.maximum(0, np.loadtxt("input_data/Medoid/P_PV_TRY_normal.csv"))
    raw_inputs["Q_Hou_Dem"] = np.maximum(0, np.loadtxt("input_data/Medoid/Q_Heat_Dem_normal.csv"))
    raw_inputs['Wind_Speed'] = np.maximum(0, np.loadtxt("input_data/Medoid/Wind_Speed_normal.csv"))
    raw_inputs['Rad_Glo'] = np.maximum(0, np.loadtxt("input_data/Medoid/Global_Radiation_normal.csv"))

elif TRY == 'warm':
    raw_inputs["T_Air"] = np.loadtxt("input_data/Temperature/temperature_warm.csv")
    raw_inputs["P_PV"] = np.maximum(0, np.loadtxt("input_data/clustering_day_comparison.csv"))
    raw_inputs["Q_Hou_Dem"] = np.maximum(0, np.loadtxt("input_data/Medoid/Q_Heat_Dem_warm.csv"))
    raw_inputs['Wind_Speed'] = np.maximum(0, np.loadtxt("input_data/Medoid/Wind_Speed_warm.csv"))
    raw_inputs['Rad_Glo'] = np.maximum(0, np.loadtxt("input_data/Medoid/Global_Radiation_warm.csv"))
else:
    print('Please select a TRY in EasyMPC -> Options')


#if Tariff == 'Fix':
    #options['Tariff']['Variable'] == True:
    raw_inputs["c_grid"]            = np.loadtxt("input_data/Medoid/FixPowerPrice.csv")
#else:
 #   raw_inputs["c_grid"]            = np.loadtxt("input_data/VariablePowerPrice.csv")

# electricity demand
raw_inputs["P_EL_Dem"]          = np.maximum(0, np.loadtxt("input_data/ELHour.txt"))


#     raw_inputs["Q_TWW_Dem"] = np.maximum(0, np.loadtxt("input_data/Q_TWW_Dem.csv"))

abs_T_Air = np.sum((raw_inputs["T_Air"]))
abs_Q_Hou_Dem = np.sum(raw_inputs["Q_Hou_Dem"])
abs_P_PV = np.sum(raw_inputs["P_PV"])
#abs_Wind_Speed = np.sum(raw_inputs["Wind_Speed"])
abs_P_EL_Dem = np.sum(raw_inputs["P_EL_Dem"])
#abs_Rad_Glo = np.sum(raw_inputs["Rad_Glo"])
#abs_c_grid = np.sum(raw_inputs["c_grid"])
#abs_Q_TWW_Dem = np.sum(raw_inputs["Q_TWW_Dem"])

data = [abs_T_Air, abs_Q_Hou_Dem, abs_P_PV, abs_P_EL_Dem]


#s = pd.Series(data, index=range(len(data)))
#s.plot(kind="bar", rot=0)
#plt.plot()
#plt.show()
#%% Clustering Inputdata
#set the range of typedays you want to analyse here!
first = 5
last = 16
distance = 1

#Different weight-Factors
w_T = 1
w_Q = 1
w_PPV = 1
w_PEL = 4
Mip_Gap = 0.005



typedays = range(first,last,distance)


clustered = {}
diff = {}
diff["T_Air"] = 0
diff["Q_Hou_Dem"] = 0
diff["P_PV"] = 0
#diff["Wind_Speed"] = 0
diff["P_EL_Dem"] = 0
#diff["Rad_Glo"] = 0
#diff["c_grid"] = 0
#diff["Q_TWW_Dem"] = 0

R_Square = {}
R_Square["R_T_Air"] = 0
R_Square["R_Q_Hou_Dem"] = 0
R_Square["R_P_PV"] = 0
R_Square["R_P_EL_Dem"] = 0
R_Square["R_Gesamt"] = 0



#%% clustering various inputs
for i in typedays:

    number_clusters = i
    inputs_clustering = np.array([raw_inputs["T_Air"],
                                raw_inputs["Q_Hou_Dem"],
                                raw_inputs["P_PV"],
 #                               raw_inputs["Wind_Speed"],
                                raw_inputs["P_EL_Dem"],
 #                               raw_inputs["Rad_Glo"],
                            #    raw_inputs["c_grid"],
                            #    raw_inputs["Q_TWW_Dem"],
                            ])

    (inputs, nc, z, inputsTransformed) = clustering.cluster(inputs_clustering,
                             number_clusters,
                             norm = 2,
                             mip_gap = Mip_Gap,
                             weights = [w_T,w_Q,w_PPV,w_PEL])

    # Set Names for Data nameing
    input = 'Alle_'
    Mip_String = str(Mip_Gap)
    Mip = Mip_String.replace('.', '')
    weights = '_'+str(w_T)+str(w_Q)+str(w_PPV)+str(w_PEL)+'_'
    typdays = '_'+ str(number_clusters) + '_'
    dataname = "Cluster_"+input+str(first)+typdays+str(distance)+str(weights)+Mip



    # Determine time steps per day
    len_day = int(inputs_clustering.shape[1] / 365)


    print("clustering " + str(i) + " successful")
    clustered = {}


    clustered["T_Air_"+str(i)]       = inputs[0]
    clustered["Q_Hou_Dem_"+str(i)] = inputs[1]
    clustered["P_PV_"+str(i)]       = inputs[2]
#    clustered["Wind_Speed_"+str(i)] = inputs[3]
    clustered["P_EL_Dem_"+str(i)] = inputs[3]
#    clustered["Rad_Glo_"+str(i)] = inputs[5]
    #    clustered["c_grid_"+str(i)] = inputs[6]
    # clustered["Q_TWW_Dem_"+str(i)] = inputs[7]


    clustered["weights"+str(i)]            = nc
    clustered["mapping_"+ str(i)]   = z

    # adjust z for gap-related valuation errors
    for m in range(len(z)):
        for n in range(len(z)):
            if z[n,m] < 1:
                z[n,m] = 0

    # build matrix map_days indicating which day of the year is assigned to which typeday
    map_days = np.zeros([len(z),len(z)])
    times_cluster = np.sum(z, axis=1)
    j=1
    for t in range(len(times_cluster)):
        if times_cluster[t] > 0:
            map_days[t,:] = z[t,:]*j
            j = j+1

    clustered_T_Air = []
    clustered_Q_Hou_Dem = []
    clustered_P_PV =[]
#    clustered_Wind_Speed = []
    clustered_P_EL_Dem = []
#    clustered_Rad_Glo = []
    # clustered_c_grid = []
    # clustered_Q_TWW_Dem = []




    for m in range(len(z)):
        for n in range(len(z)):
            if map_days[n,m] > 0:
                clustered_T_Air = np.append(clustered_T_Air,clustered["T_Air_"+ str(i)][int(map_days[n,m] -1)])
                clustered_Q_Hou_Dem = np.append(clustered_Q_Hou_Dem,clustered["Q_Hou_Dem_"+ str(i)][int(map_days[n,m] -1)])
                clustered_P_PV = np.append(clustered_P_PV,clustered["P_PV_"+ str(i)][int(map_days[n,m] -1)])
#                clustered_Wind_Speed = np.append(clustered_Wind_Speed,clustered["Wind_Speed_"+ str(i)][int(map_days[n,m] -1)])
                clustered_P_EL_Dem = np.append(clustered_P_EL_Dem,clustered["P_EL_Dem_"+ str(i)][int(map_days[n,m] -1)])
#                clustered_Rad_Glo = np.append(clustered_Rad_Glo,clustered["Rad_Glo_"+ str(i)][int(map_days[n,m] -1)])
             #   clustered_c_grid = np.append(clustered_c_grid,clustered["c_grid_"+ str(i)][int(map_days[n,m] -1)])
             #   clustered_Q_TWW_Dem = np.append(clustered_Q_TWW_Dem,clustered["Q_TWW_Dem_"+ str(i)][int(map_days[n,m] -1)])


    diff_T_Air = np.abs(clustered_T_Air - raw_inputs["T_Air"])
    diff_Q_Hou_Dem = np.abs(clustered_Q_Hou_Dem - raw_inputs["Q_Hou_Dem"])
    diff_P_PV = np.abs(clustered_P_PV - raw_inputs["P_PV"])
#    diff_Wind_Speed = np.abs(clustered_Wind_Speed - raw_inputs["Wind_Speed"])
    diff_P_EL_Dem = np.abs(clustered_P_EL_Dem - raw_inputs["P_EL_Dem"])
#    diff_Rad_Glo = np.abs(clustered_Rad_Glo - raw_inputs["Rad_Glo"])
    # diff_c_grid = np.abs(clustered_c_grid - raw_inputs["c_grid"])
    # diff_Q_TWW_Dem = np.abs(clustered_Q_TWW_Dem - raw_inputs["Q_TWW_Dem"])


    diff["T_Air"] = np.append(diff["T_Air"], np.sum(diff_T_Air))
    diff["Q_Hou_Dem"] = np.append(diff["Q_Hou_Dem"], np.sum(diff_Q_Hou_Dem))
    diff["P_PV"] = np.append(diff["P_PV"], np.sum(diff_P_PV))
#    diff["Wind_Speed"] = np.append(diff["Wind_Speed"], np.sum(diff_Wind_Speed))
    diff["P_EL_Dem"] = np.append(diff["P_EL_Dem"], np.sum(diff_P_EL_Dem))
#    diff["Rad_Glo"] = np.append(diff["Rad_Glo"], np.sum(diff_Rad_Glo))
#    diff["c_grid"] = np.append(diff["c_grid"], np.sum(diff_c_grid))
#    diff["Q_TWW_Dem"] = np.append(diff["Q_TWW_Dem"], np.sum(diff_Q_TWW_Dem))


    deviation_diff = {}
    deviation_diff["T_Air"] = 0
    deviation_diff["Q_Hou_Dem"] = 0
    deviation_diff["P_PV"] = 0
#    deviation_diff["Wind_Speed"] = 0
    deviation_diff["P_EL_Dem"] = 0
#    deviation_diff["Rad_Glo"] = 0


    deviation_diff["T_Air"] = np.append(deviation_diff["T_Air"], diff["T_Air"][1:len(typedays)+1]/ abs_T_Air * 100)
    deviation_diff["Q_Hou_Dem"] = np.append(deviation_diff["Q_Hou_Dem"], diff["Q_Hou_Dem"][1:len(typedays)+1]/ abs_Q_Hou_Dem * 100)
    deviation_diff["P_PV"] = np.append(deviation_diff["P_PV"], diff["P_PV"][1:len(typedays)+1]/ abs_P_PV * 100)
#    deviation_diff["Wind_Speed"] = np.append(deviation_diff["Wind_Speed"], diff["Wind_Speed"][1:len(typedays)+1]/ abs_Wind_Speed * 100)
    deviation_diff["P_EL_Dem"] = np.append(deviation_diff["P_EL_Dem"], diff["P_EL_Dem"][1:len(typedays)+1]/ abs_P_EL_Dem * 100)
#    deviation_diff["Rad_Glo"] = np.append(deviation_diff["Rad_Glo"], diff["Rad_Glo"][1:len(typedays)+1]/ abs_Rad_Glo * 100)


#Calculation of R²-Value
    R_T_Air = r2_score(raw_inputs["T_Air"], clustered_T_Air)
    R_Q_Hou_Dem = r2_score(raw_inputs["Q_Hou_Dem"], clustered_Q_Hou_Dem)
    R_P_PV = r2_score(raw_inputs["P_PV"], clustered_P_PV)
    R_P_EL_Dem = r2_score(raw_inputs["P_EL_Dem"], clustered_P_EL_Dem)

    ##Summe der Gewichtungsfaktoren
    Sum_weights = w_T + w_Q + w_PPV + w_PEL
    R_Ges = (R_T_Air * w_T + R_Q_Hou_Dem * w_Q + R_P_PV * w_PPV + R_P_EL_Dem * w_PEL) / Sum_weights

    # Append to dictionary

    R_Square["R_T_Air"] = np.append(R_Square["R_T_Air"], R_T_Air)
    R_Square["R_Q_Hou_Dem"] = np.append(R_Square["R_Q_Hou_Dem"], R_Q_Hou_Dem)
    R_Square["R_P_PV"] = np.append(R_Square["R_P_PV"], R_P_PV)
    R_Square["R_P_EL_Dem"] = np.append(R_Square["R_P_EL_Dem"], R_P_EL_Dem)
    R_Square["R_Gesamt"] = np.append(R_Square["R_Gesamt"], R_Ges)


plt.xlabel('Number of typedays')
plt.ylabel('Total-Deviation from TRY-Data in %')
#plt.ylabel('Determinationskoeffizient R²')
plt.plot (typedays, diff["T_Air"][1:len(typedays)+1]/ abs_T_Air * 100, label="T_Air")
plt.plot (typedays, diff["Q_Hou_Dem"][1:len(typedays)+1]/abs_Q_Hou_Dem*100, label="Q_Hou_Dem")
plt.plot (typedays, diff["P_PV"][1:len(typedays)+1]/abs_P_PV*100, label="P_PV")
plt.plot (typedays, diff["P_EL_Dem"][1:len(typedays)+1]/abs_P_EL_Dem*100, label="P_EL_Dem")
#plt.plot (typedays, diff["Q_TWW_Dem"][1:len(typedays)+1]/abs_Q_TWW_Dem*100, label="Q_TWW_Dem")

#plt.plot (typedays, R_Square["R_T_Air"][1:(len(typedays)+1)], label="T_Air")
#plt.plot (typedays, R_Square["R_Q_Hou_Dem"][1:(len(typedays)+1)], label="Q_Hou_Dem")
#plt.plot (typedays, R_Square["R_P_PV"][1:(len(typedays)+1)], label="P_PV")
#plt.plot (typedays, R_Square["R_P_EL_Dem"][1:(len(typedays)+1)], label="P_EL_Dem")
#plt.plot (typedays, R_Square["R_Gesamt"][1:(len(typedays)+1)], label="R_Gesamt")


plt.legend(loc='lower right')

filename = "D://lma-mma/Repos/MA_MM/Cluster/"+dataname
plt.savefig(filename+".png", dpi=600)
plt.show()
print(R_Square["R_Gesamt"])

with open(filename+".pkl", 'wb') as f_in:
#with open(filename, 'w', newline='') as file:
#    writer = csv.writer(file)
#    #for row in clustered['T_Air']:
#    writer.writerow(clustered)


    pickle.dump(clustered, f_in, pickle.HIGHEST_PROTOCOL)
    pickle.dump(diff, f_in, pickle.HIGHEST_PROTOCOL)
    pickle.dump(deviation_diff, f_in, pickle.HIGHEST_PROTOCOL)
    pickle.dump(R_Square, f_in, pickle.HIGHEST_PROTOCOL)

#with open('D:/lma-mma/Repos/MA_MM/Results/Real_Results/results.csv', 'w', newline='') as csvfile:

    # Create a CSV writer object
 #   writer = csv.writer(csvfile)

    # Write the headers to the first row
 #   writer.writerow(time_to_save)
 #   for key, values in save_results.items():
 #       row = [key] + sum(values, [])
 #       writer.writerow(row)


