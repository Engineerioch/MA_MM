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
#from EasyMPC import options
# Set the TRY-Type here
TRY = 'warm'
Tariff = 'Fix'

RG = []

# Import the Data according to the choosen TRY :
raw_inputs = {}
if TRY == 'cold':
    #options['WeatherData']['TRY'] == 'cold':
    raw_inputs["T_Air"] = np.loadtxt("input_data/Medoid/temperature_cold.csv")
    raw_inputs["P_PV"] = np.maximum(0, np.loadtxt("input_data/Medoid/P_PV_TRY_cold.csv"))
    raw_inputs["Q_Hou_Dem"] = np.maximum(0, np.loadtxt("input_data/Medoid/Q_Heat_Dem_cold.csv"))

elif TRY == 'normal':
    raw_inputs["T_Air"] = np.loadtxt("input_data/Medoid/temperature_normal.csv")
    raw_inputs["P_PV"] = np.maximum(0, np.loadtxt("input_data/Medoid/P_PV_TRY_normal.csv"))
    raw_inputs["Q_Hou_Dem"] = np.maximum(0, np.loadtxt("input_data/Medoid/Q_Heat_Dem_normal.csv"))

elif TRY == 'warm':
    raw_inputs["T_Air"] = np.loadtxt("input_data/Medoid/temperature_warm.csv")
    raw_inputs["P_PV"] = np.maximum(0, np.loadtxt("input_data/Medoid/P_PV_TRY_warm.csv"))
    raw_inputs["Q_Hou_Dem"] = np.maximum(0, np.loadtxt("input_data/Medoid/Q_Heat_Dem_warm.csv"))
else:
    print('Please select a TRY in EasyMPC -> Options')

# electricity demand
raw_inputs["P_EL_Dem"]          = np.maximum(0, np.loadtxt("input_data/Medoid/ELHour.txt"))


abs_T_Air = np.sum((raw_inputs["T_Air"]))
abs_Q_Hou_Dem = np.sum(raw_inputs["Q_Hou_Dem"])
abs_P_PV = np.sum(raw_inputs["P_PV"])
abs_P_EL_Dem = np.sum(raw_inputs["P_EL_Dem"])


data = [abs_T_Air, abs_Q_Hou_Dem, abs_P_PV, abs_P_EL_Dem]



#%% Clustering Inputdata
#set the range of typedays you want to analyse here!
first = 8
last = 9
distance = 1

#Different weight-Factors
w_T = 3
w_Q = 4
w_PPV = 2
w_PEL = 1
Mip_Gap = 0.01
typedays = range(first,last,distance)


clustered = {}
diff = {}
diff["T_Air"] = 0
diff["Q_Hou_Dem"] = 0
diff["P_PV"] = 0
diff["P_EL_Dem"] = 0

R_Square = {}
R_Square["R_T_Air"] = 0
R_Square["R_Q_Hou_Dem"] = 0
R_Square["R_P_PV"] = 0
R_Square["R_P_EL_Dem"] = 0
R_Square["R_Gesamt"] = 0



# clustering various inputs
for i in typedays:

    number_clusters = i
    inputs_clustering = np.array([raw_inputs["T_Air"],
                                raw_inputs["Q_Hou_Dem"],
                                raw_inputs["P_PV"],
                                raw_inputs["P_EL_Dem"],
                            ])

    (inputs, nc, z, inputsTransformed) = clustering.cluster(inputs_clustering,
                             number_clusters,
                             norm = 2,
                             mip_gap = Mip_Gap,
                             weights = [w_T,w_Q,w_PPV,w_PEL])

    # Set Names for Data nameing
    input = 'Alle_'
    Mip_String = str(Mip_Gap)+'_'+ TRY
    Mip = Mip_String.replace('.', '')
    weights = '_'+str(w_T)+str(w_Q)+str(w_PPV)+str(w_PEL)+'_'
    typdays = '_'+ str(number_clusters) + '_'
    dataname = "Cluster_"+input+str(first)+typdays+str(distance)+str(weights)+Mip



    # Determine time steps per day
    len_day = int(inputs_clustering.shape[1] / 365)


    print("clustering " + str(i) + " successful")
    clustered = {}


    clustered["T_Air_"+str(i)]      = inputs[0]
    clustered["Q_Hou_Dem_"+str(i)]  = inputs[1]
    clustered["P_PV_"+str(i)]       = inputs[2]
    clustered["P_EL_Dem_"+str(i)]   = inputs[3]
    clustered["weights"+str(i)]     = nc
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
    clustered_P_EL_Dem = []



    for m in range(len(z)):
        for n in range(len(z)):
            if map_days[n,m] > 0:
                clustered_T_Air = np.append(clustered_T_Air,clustered["T_Air_"+ str(i)][int(map_days[n,m] -1)])
                clustered_Q_Hou_Dem = np.append(clustered_Q_Hou_Dem,clustered["Q_Hou_Dem_"+ str(i)][int(map_days[n,m] -1)])
                clustered_P_PV = np.append(clustered_P_PV,clustered["P_PV_"+ str(i)][int(map_days[n,m] -1)])
                clustered_P_EL_Dem = np.append(clustered_P_EL_Dem,clustered["P_EL_Dem_"+ str(i)][int(map_days[n,m] -1)])


    diff_T_Air = np.abs(clustered_T_Air - raw_inputs["T_Air"])
    diff_Q_Hou_Dem = np.abs(clustered_Q_Hou_Dem - raw_inputs["Q_Hou_Dem"])
    diff_P_PV = np.abs(clustered_P_PV - raw_inputs["P_PV"])
    diff_P_EL_Dem = np.abs(clustered_P_EL_Dem - raw_inputs["P_EL_Dem"])


    diff["T_Air"] = np.append(diff["T_Air"], np.sum(diff_T_Air))
    diff["Q_Hou_Dem"] = np.append(diff["Q_Hou_Dem"], np.sum(diff_Q_Hou_Dem))
    diff["P_PV"] = np.append(diff["P_PV"], np.sum(diff_P_PV))
    diff["P_EL_Dem"] = np.append(diff["P_EL_Dem"], np.sum(diff_P_EL_Dem))


    deviation_diff = {}
    deviation_diff["T_Air"] = 0
    deviation_diff["Q_Hou_Dem"] = 0
    deviation_diff["P_PV"] = 0
    deviation_diff["P_EL_Dem"] = 0


    deviation_diff["T_Air"] = np.append(deviation_diff["T_Air"], diff["T_Air"][1:len(typedays)+1]/ abs_T_Air * 100)
    deviation_diff["Q_Hou_Dem"] = np.append(deviation_diff["Q_Hou_Dem"], diff["Q_Hou_Dem"][1:len(typedays)+1]/ abs_Q_Hou_Dem * 100)
    deviation_diff["P_PV"] = np.append(deviation_diff["P_PV"], diff["P_PV"][1:len(typedays)+1]/ abs_P_PV * 100)
    deviation_diff["P_EL_Dem"] = np.append(deviation_diff["P_EL_Dem"], diff["P_EL_Dem"][1:len(typedays)+1]/ abs_P_EL_Dem * 100)


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
plt.plot (typedays, diff["T_Air"][1:len(typedays)+1]/ abs_T_Air * 100, label="T_Air")
plt.plot (typedays, diff["Q_Hou_Dem"][1:len(typedays)+1]/abs_Q_Hou_Dem*100, label="Q_Hou_Dem")
plt.plot (typedays, diff["P_PV"][1:len(typedays)+1]/abs_P_PV*100, label="P_PV")
plt.plot (typedays, diff["P_EL_Dem"][1:len(typedays)+1]/abs_P_EL_Dem*100, label="P_EL_Dem")
plt.style.use("D://lma-mma/Repos/MA_MM/ebc.paper.mplstyle")

#plt.ylabel('Determinationskoeffizient R²')
#plt.plot (typedays, R_Square["R_T_Air"][1:(len(typedays)+1)], label="T_Air")
#plt.plot (typedays, R_Square["R_Q_Hou_Dem"][1:(len(typedays)+1)], label="Q_Hou_Dem")
#plt.plot (typedays, R_Square["R_P_PV"][1:(len(typedays)+1)], label="P_PV")
#plt.plot (typedays, R_Square["R_P_EL_Dem"][1:(len(typedays)+1)], label="P_EL_Dem")
#plt.plot (typedays, R_Square["R_Gesamt"][1:(len(typedays)+1)], label="R_Gesamt")


#plt.legend(loc='upper left')

#plt.rcParams.update(latex_base)
#rc('font', **{'family':'san-serif','sans-serif':['Times']})
#rc('text', usetex = True)
plt.rcParams
#plt.rcParams["font.family"] = "Helvetica"
#plt.rcParams["font.efficiency"] = 22

filename = "D://lma-mma/Repos/MA_MM/Cluster/"+dataname
#plt.savefig(filename+".png", dpi=600)
#plt.show()

#with open(filename+".pkl", 'wb') as f_in:
#   pickle.dump(clustered, f_in, pickle.HIGHEST_PROTOCOL)
#   pickle.dump(diff, f_in, pickle.HIGHEST_PROTOCOL)
#   pickle.dump(deviation_diff, f_in, pickle.HIGHEST_PROTOCOL)
#   pickle.dump(R_Square, f_in, pickle.HIGHEST_PROTOCOL)


clustered_TWW = []
for i in range(0,len(clustered_T_Air)):
    if i % 24 == 0:
        if round(clustered_T_Air[i], 2) == round(clustered["T_Air_8"][0][0], 2):
            with open("input_data/Medoid/TWW/outcome_1.csv", 'r') as file:
                reader = csv.reader(file)
                first = [float(row[0]) for row in reader]
                second = [float(row[1]) for row in reader]
                third = [float(row[2]) for row in reader]
                fourth = [float(row[3]) for row in reader]
        elif clustered_T_Air[i] == clustered["T_Air_8"][1][0]:
            with open("input_data/Medoid/TWW/outcome_2.csv", 'r') as file:
                reader = csv.reader(file)
                first = [float(row[0]) for row in reader]
                second = [float(row[1]) for row in reader]
                third = [float(row[2]) for row in reader]
                fourth = [float(row[3]) for row in reader]
        elif round(clustered_T_Air[i], 2) == round(clustered["T_Air_8"][2][0], 2):
            with open("input_data/Medoid/TWW/outcome_3.csv", 'r') as file:
                reader = csv.reader(file)
                first = [float(row[0]) for row in reader]
                second = [float(row[1]) for row in reader]
                third = [float(row[2]) for row in reader]
                fourth = [float(row[3]) for row in reader]
 #               print("True")
        elif clustered_T_Air[i] == clustered["T_Air_8"][3][0]:
            with open("input_data/Medoid/TWW/outcome_4.csv", 'r') as file:
                reader = csv.reader(file)
                first = [float(row[0]) for row in reader]
                second = [float(row[1]) for row in reader]
                third = [float(row[2]) for row in reader]
                fourth = [float(row[3]) for row in reader]
        elif clustered_T_Air[i] == clustered["T_Air_8"][4][0]:
            with open("input_data/Medoid/TWW/outcome_5.csv", 'r') as file:
                reader = csv.reader(file)
                first = [float(row[0]) for row in reader]
                second = [float(row[1]) for row in reader]
                third = [float(row[2]) for row in reader]
                fourth = [float(row[3]) for row in reader]
        elif clustered_T_Air[i] == clustered["T_Air_8"][5][0]:
            with open("input_data/Medoid/TWW/outcome_6.csv", 'r') as file:
                reader = csv.reader(file)
                first = [float(row[0]) for row in reader]
                second = [float(row[1]) for row in reader]
                third = [float(row[2]) for row in reader]
                fourth = [float(row[3]) for row in reader]
        elif clustered_T_Air[i] == clustered["T_Air_8"][6][0]:
            with open("input_data/Medoid/TWW/outcome_7.csv", 'r') as file:
                reader = csv.reader(file)
                first = [float(row[0]) for row in reader]
                second = [float(row[1]) for row in reader]
                third = [float(row[2]) for row in reader]
                fourth = [float(row[3]) for row in reader]
        elif clustered_T_Air[i] == clustered["T_Air_8"][7][0]:
            with open("input_data/Medoid/TWW/outcome_8.csv", 'r') as file:
                reader = csv.reader(file)
                first = [float(row[0]) for row in reader]
                second = [float(row[1]) for row in reader]
                third = [float(row[2]) for row in reader]
                fourth = [float(row[3]) for row in reader]
 #       elif clustered_T_Air[i] == clustered["T_Air_12"][8][0]:
 #           with open("input_data/Medoid/TWW/outcome_9.csv", 'r') as file:
 #               reader = csv.reader(file)
 #               first = [float(row[0]) for row in reader]
 #               second = [float(row[1]) for row in reader]
 #               third = [float(row[2]) for row in reader]
 #               fourth = [float(row[3]) for row in reader]
 #       elif clustered_T_Air[i] == clustered["T_Air_12"][9][0]:
 #           with open("input_data/Medoid/TWW/outcome_10.csv", 'r') as file:
 #               reader = csv.reader(file)
 #               first = [float(row[0]) for row in reader]
 #               second = [float(row[1]) for row in reader]
 #               third = [float(row[2]) for row in reader]
 #               fourth = [float(row[3]) for row in reader]
 #       elif clustered_T_Air[i] == clustered["T_Air_12"][10][0]:
 #           with open("input_data/Medoid/TWW/outcome_11.csv", 'r') as file:
 #               reader = csv.reader(file)
 #               first = [float(row[0]) for row in reader]
 #               second = [float(row[1]) for row in reader]
  #              third = [float(row[2]) for row in reader]
  #              fourth = [float(row[3]) for row in reader]
  #      elif clustered_T_Air[i] == clustered["T_Air_12"][11][0]:
  #          with open("input_data/Medoid/TWW/outcome_12.csv", 'r') as file:
  #              reader = csv.reader(file)
  #              first = [float(row[0]) for row in reader]
  #              second = [float(row[1]) for row in reader]
  #              third = [float(row[2]) for row in reader]
  #              fourth = [float(row[3]) for row in reader]

        for j in range(len(first)):
            clustered_TWW.append(first[j])
    else:
        pass

data = list(zip(clustered_T_Air, clustered_Q_Hou_Dem, clustered_P_PV, clustered_P_EL_Dem, clustered_TWW))
with open(f"ClusteredYear_warm.csv", "w", newline="") as f:
    writer = csv.writer(f)
    for values in zip(clustered_T_Air, clustered_Q_Hou_Dem, clustered_P_PV, clustered_P_EL_Dem, clustered_TWW):
        writer.writerow(values)



