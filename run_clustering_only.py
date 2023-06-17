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
from plot_results_to_files import pp_figure

import tikzplotlib

from plot_results_to_files import latex_base
import clustering_medoid as clustering
from sklearn.metrics import r2_score
from rwth_colors import colors
plt.rcParams.update(pp_figure)


# Set the TRY-Type here
TRY = 'normal'
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



# Clustering Inputdata
#set the range of typedays you want to analyse here!
first = 1
last = 15
distance = 1

#Different weight-Factors
w_T = 1
w_Q = 1
w_PPV = 1
w_PEL = 1
Mip_Gap = 0.01
typedays = range(first,last,distance)



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
R_Square["R_Gesamt2"] = 0


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

#
    for m in range(len(z)):
        for n in range(len(z)):
            if map_days[n,m] > 0:
                clustered_T_Air = np.append(clustered_T_Air,clustered["T_Air_"+ str(i)][int(map_days[n,m] -1)])
                clustered_Q_Hou_Dem = np.append(clustered_Q_Hou_Dem,clustered["Q_Hou_Dem_"+ str(i)][int(map_days[n,m] -1)])
                clustered_P_PV = np.append(clustered_P_PV,clustered["P_PV_"+ str(i)][int(map_days[n,m] -1)])
                clustered_P_EL_Dem = np.append(clustered_P_EL_Dem,clustered["P_EL_Dem_"+ str(i)][int(map_days[n,m] -1)])
#
#
    diff_T_Air = np.abs(clustered_T_Air - raw_inputs["T_Air"])
    diff_Q_Hou_Dem = np.abs(clustered_Q_Hou_Dem - raw_inputs["Q_Hou_Dem"])
    diff_P_PV = np.abs(clustered_P_PV - raw_inputs["P_PV"])
    diff_P_EL_Dem = np.abs(clustered_P_EL_Dem - raw_inputs["P_EL_Dem"])
#
#
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
    R_Ges1 = (R_T_Air * w_T + R_Q_Hou_Dem * w_Q + R_P_PV * w_PPV + R_P_EL_Dem * w_PEL) / Sum_weights
#    R_Ges2 = (R_T_Air / 4) + (R_Q_Hou_Dem / 4) + (R_P_PV / 4) + (R_P_EL_Dem / 4)

    # Append to dictionary
    R_Square["R_T_Air"] = np.append(R_Square["R_T_Air"], R_T_Air)
    R_Square["R_Q_Hou_Dem"] = np.append(R_Square["R_Q_Hou_Dem"], R_Q_Hou_Dem)
    R_Square["R_P_PV"] = np.append(R_Square["R_P_PV"], R_P_PV)
    R_Square["R_P_EL_Dem"] = np.append(R_Square["R_P_EL_Dem"], R_P_EL_Dem)
    R_Square["R_Gesamt"] = np.append(R_Square["R_Gesamt"], R_Ges1)
#    R_Square["R_Gesamt2"] = np.append(R_Square["R_Gesamt2"], R_Ges2)

plt.xlabel('Anzahl der Typtage')
plt.ylabel('Abweichung von den TRY-Daten in %')
#plt.rcParams.update(latex_base)
plt.plot(typedays, diff["T_Air"][1:len(typedays)+1]/ abs_T_Air * 100, label="$T_\mathrm{Außen}$")
plt.plot(typedays, diff["Q_Hou_Dem"][1:len(typedays)+1]/abs_Q_Hou_Dem*100, label="$Q_\mathrm{Haus,Bed}$")
plt.plot(typedays, diff["P_PV"][1:len(typedays)+1]/abs_P_PV*100, label="$P_\mathrm{PV}$")
plt.plot(typedays, diff["P_EL_Dem"][1:len(typedays)+1]/abs_P_EL_Dem*100, label="$P_\mathrm{El,Bed}$")
#plt.style.use("D://lma-mma/Repos/MA_MM/ebc.paper.mplstyle")
plt.legend()
#Set saving location:
filename = "results/" + dataname
#plt.savefig(filename+".svg")
#plt.savefig(filename+".pdf")
#tikzplotlib.save(filename+'.tex')
plt.show()

plt.ylabel('Determinationskoeffizient R²')
plt.plot (typedays, R_Square["R_T_Air"][1:(len(typedays)+1)], label="$T_\mathrm{Außen}$", color=colors)
plt.plot (typedays, R_Square["R_Q_Hou_Dem"][1:(len(typedays)+1)], label="$R_{Q_\mathrm{Haus,Bed}}$")
plt.plot (typedays, R_Square["R_P_PV"][1:(len(typedays)+1)], label="$R_{P_\mathrm{PV}}$")
plt.plot (typedays, R_Square["R_P_EL_Dem"][1:(len(typedays)+1)], label="$R_{P_\mathrm{El,Bed}}$")
plt.plot (typedays, R_Square["R_Gesamt"][1:(len(typedays)+1)], label="$R_\mathrm{Gesamt,Gewichtet}$")
#plt.plot (typedays, R_Square["R_Gesamt2"][1:(len(typedays)+1)], label="R-Gesamt")

plt.rcParams.update(pp_figure)
#rc('font', **{'family':'san-serif','sans-serif':['Times']})
#rc('text', usetex = True)
#plt.rcParams
#plt.rcParams["font.family"] = "Helvetica"
#plt.rcParams["font.efficiency"] = 22

plt.legend()
#plt.savefig(filename+".pdf")
#plt.savefig(filename+".svg")
#tikzplotlib.save(filename+'.tex')
plt.show()

with open(filename+".pkl", 'wb') as f_in:
#   pickle.dump(clustered, f_in, pickle.HIGHEST_PROTOCOL)
#   pickle.dump(diff, f_in, pickle.HIGHEST_PROTOCOL)
#   pickle.dump(deviation_diff, f_in, pickle.HIGHEST_PROTOCOL)
   pickle.dump(R_Square, f_in, pickle.HIGHEST_PROTOCOL)


#c_grid = []
#for i in range(0,8760):
#    c_grid.append(clustered_c_grid[i])
#print(type(clustered_c_grid))
xp = np.arange(0.0, 8760, 1.0)
xnew = np.arange(0.0, 8760, 0.25)
#T = clustered_T_Air.tolist()

T_Air = np.interp(xnew, xp, clustered_T_Air) #Liste1)
Q_Hou= np.interp(xnew, xp, clustered_Q_Hou_Dem)
PPV= np.interp(xnew, xp, clustered_P_PV)
PEL= np.interp(xnew, xp, clustered_P_EL_Dem)
#print(len(c_grid))
#c =  np.interp(xnew, xp, c_grid)


# Create a timeline of one year and append DHW-Data according to the typedays
print(len(T_Air.tolist()))
print(clustered["T_Air_8"])
clustered_TWW = []
clustered_TWW1 = []
clustered_TWW2 = []
clustered_TWW3 = []
clustered_c_grid = []
for i in range(0,len(clustered_T_Air)):
    if i % 24 == 0:
        if round(clustered_T_Air[i], 2) == round(clustered["T_Air_8"][0][0], 2):
            with open("input_data/Medoid/TWW/"+TRY+"/outcome_1.csv", 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    first = float(row[0])
                    second = float(row[1])
                    third = float(row[2])
                    fourth = float(row[3])
                    clustered_TWW.append(first)
                    clustered_TWW1.append(second)
                    clustered_TWW2.append(third)
                    clustered_TWW3.append(fourth)

        elif clustered_T_Air[i] == clustered["T_Air_8"][1][0]:
            with open("input_data/Medoid/TWW/"+TRY+"/outcome_2.csv", 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    first = float(row[0])
                    second = float(row[1])
                    third = float(row[2])
                    fourth = float(row[3])
                    clustered_TWW.append(first)
                    clustered_TWW1.append(second)
                    clustered_TWW2.append(third)
                    clustered_TWW3.append(fourth)

        elif round(clustered_T_Air[i], 2) == round(clustered["T_Air_8"][2][0], 2):
            with open("input_data/Medoid/TWW/"+TRY+"/outcome_3.csv", 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    first = float(row[0])
                    second = float(row[1])
                    third = float(row[2])
                    fourth = float(row[3])
                    clustered_TWW.append(first)
                    clustered_TWW1.append(second)
                    clustered_TWW2.append(third)
                    clustered_TWW3.append(fourth)
                #print("True")
        elif clustered_T_Air[i] == clustered["T_Air_8"][3][0]:
            with open("input_data/Medoid/TWW/"+TRY+"/outcome_4.csv", 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    first = float(row[0])
                    second = float(row[1])
                    third = float(row[2])
                    fourth = float(row[3])
                    clustered_TWW.append(first)
                    clustered_TWW1.append(second)
                    clustered_TWW2.append(third)
                    clustered_TWW3.append(fourth)
        elif clustered_T_Air[i] == clustered["T_Air_8"][4][0]:
            with open("input_data/Medoid/TWW/"+TRY+"/outcome_5.csv", 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    first = float(row[0])
                    second = float(row[1])
                    third = float(row[2])
                    fourth = float(row[3])
                    clustered_TWW.append(first)
                    clustered_TWW1.append(second)
                    clustered_TWW2.append(third)
                    clustered_TWW3.append(fourth)

        elif clustered_T_Air[i] == clustered["T_Air_8"][5][0]:
            with open("input_data/Medoid/TWW/"+TRY+"/outcome_6.csv", 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    first = float(row[0])
                    second = float(row[1])
                    third = float(row[2])
                    fourth = float(row[3])
                    clustered_TWW.append(first)
                    clustered_TWW1.append(second)
                    clustered_TWW2.append(third)
                    clustered_TWW3.append(fourth)
        elif clustered_T_Air[i] == clustered["T_Air_8"][6][0]:
            with open("input_data/Medoid/TWW/"+TRY+"/outcome_7.csv", 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    first = float(row[0])
                    second = float(row[1])
                    third = float(row[2])
                    fourth = float(row[3])
                    clustered_TWW.append(first)
                    clustered_TWW1.append(second)
                    clustered_TWW2.append(third)
                    clustered_TWW3.append(fourth)
        elif clustered_T_Air[i] == clustered["T_Air_8"][7][0]:
            with open("input_data/Medoid/TWW/"+TRY+"/outcome_8.csv", 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    first = float(row[0])
                    second = float(row[1])
                    third = float(row[2])
                    fourth = float(row[3])
                    clustered_TWW.append(first)
                    clustered_TWW1.append(second)
                    clustered_TWW2.append(third)
                    clustered_TWW3.append(fourth)
        else:
            print('False')


print(T_Air.tolist())

#Save Clustered Year:
header = 'T_Air', 'Q_Hou', 'PPV', 'PEL', 'QTWW','Tp','Tmin','f',

#data = list(zip(T_Air, Q_Hou, PPV, PEL, clustered_TWW, clustered_TWW1, clustered_TWW2, clustered_TWW3))
#with open(f"input_data/ClusteredYear/ClusteredYear_"+TRY+".csv", "w", newline="") as f:
#    writer = csv.writer(f)
#    writer.writerow([g for g in header])
#    for values in data:
#        writer.writerow(values)

