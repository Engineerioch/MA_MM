import pickle
import csv

import numpy as np
import pandas as pd





#Data_0_025_48_4_24_Clusterday_0_normal_Var_TWW_Medium_Norm
TRY = 'normal'
Strompreis = 'Fix'
Ordner = 'Results/Optimierung/TWW/Clusterday/'
Dataname= Ordner + 'Data_0_025_48_4_24_Clusterday_'
Modesname= Ordner + 'Modes_0_025_48_4_24_Clusterday_'
filename_rest = '_' + TRY + '_' + Strompreis +'_TWW_Small_Norm.csv'
#
#
Savename = '_0_025_8760_4_24_Clusteryear' + filename_rest


Year = pd.read_csv(f"input_data/ClusteredYear/ClusteredYear_"+TRY+".csv", skiprows=0)
T_Year0 = Year.iloc[:,0] + 273.15
T_Year = T_Year0.tolist()
Data_Modes_0 = pd.read_csv(Modesname + "0" + filename_rest, header=None)
Modes_0 = Data_Modes_0.values.tolist()
List_0 = pd.read_csv(Dataname + "0" + filename_rest, header=None)
T_0 = List_0.iloc[:,0].tolist()
Q_0 = List_0.iloc[:,1].tolist()
PV_0 = List_0.iloc[:,2].tolist()
PEL_0 = List_0.iloc[:,3].tolist()
TM_0 = List_0.iloc[:,4].tolist()
Cel_0 = List_0.iloc[:,5].tolist()

Data_Modes_1 = pd.read_csv(Modesname + "1" + filename_rest, header=None)
Modes_1 = Data_Modes_1.values.tolist()
List_1 = pd.read_csv(Dataname + "1" + filename_rest, header=None)
T_1 = List_1.iloc[:,0].tolist()
Q_1 = List_1.iloc[:,1].tolist()
PV_1 = List_1.iloc[:,2].tolist()
PEL_1 = List_1.iloc[:,3].tolist()
TM_1 = List_1.iloc[:,4].tolist()
Cel_1 = List_1.iloc[:,5].tolist()

Data_Modes_2 = pd.read_csv(Modesname + "2" + filename_rest, header=None)
Modes_2 = Data_Modes_2.values.tolist()
List_2 = pd.read_csv(Dataname + "2" + filename_rest, header=None)
T_2 = List_2.iloc[:,0].tolist()
Q_2 = List_2.iloc[:,1].tolist()
PV_2 = List_2.iloc[:,2].tolist()
PEL_2 = List_2.iloc[:,3].tolist()
TM_2 = List_2.iloc[:,4].tolist()
Cel_2 = List_2.iloc[:,5].tolist()

Data_Modes_3 = pd.read_csv(Modesname + "3" + filename_rest, header=None)
Modes_3 = Data_Modes_3.values.tolist()
List_3 = pd.read_csv(Dataname + "3" + filename_rest, header=None)
T_3 = List_3.iloc[:,0].tolist()
Q_3 = List_3.iloc[:,1].tolist()
PV_3 = List_3.iloc[:,2].tolist()
PEL_3 = List_3.iloc[:,3].tolist()
TM_3 = List_3.iloc[:,4].tolist()
Cel_3 = List_3.iloc[:,5].tolist()

Data_Modes_4 = pd.read_csv(Modesname + "4" + filename_rest, header=None)
Modes_4 = Data_Modes_4.values.tolist()
List_4 = pd.read_csv(Dataname + "4" + filename_rest, header=None)
T_4 = List_4.iloc[:,0].tolist()
Q_4 = List_4.iloc[:,1].tolist()
PV_4 = List_4.iloc[:,2].tolist()
PEL_4 = List_4.iloc[:,3].tolist()#
TM_4 = List_4.iloc[:,4].tolist()
Cel_4 = List_4.iloc[:,5].tolist()

Data_Modes_5 = pd.read_csv(Modesname + "5" + filename_rest, header=None)
Modes_5 = Data_Modes_5.values.tolist()
List_5 = pd.read_csv(Dataname + "5" + filename_rest, header=None)
T_5 = List_5.iloc[:,0].tolist()
Q_5 = List_5.iloc[:,1].tolist()
PV_5 = List_5.iloc[:,2].tolist()
PEL_5 = List_5.iloc[:,3].tolist()
TM_5 = List_5.iloc[:,4].tolist()
Cel_5 = List_5.iloc[:,5].tolist()

Data_Modes_6 = pd.read_csv(Modesname + "6" + filename_rest, header=None)
Modes_6 = Data_Modes_6.values.tolist()
List_6 = pd.read_csv(Dataname + "6" + filename_rest, header=None)
T_6 = List_6.iloc[:,0].tolist()
Q_6 = List_6.iloc[:,1].tolist()
PV_6 = List_6.iloc[:,2].tolist()
PEL_6 = List_6.iloc[:,3].tolist()
TM_6 = List_6.iloc[:,4].tolist()
Cel_6 = List_6.iloc[:,5].tolist()

Data_Modes_7 = pd.read_csv(Modesname + "7" + filename_rest, header=None)
Modes_7 = Data_Modes_7.values.tolist()
List_7 = pd.read_csv(Dataname + "7" + filename_rest, header=None)
T_7 = List_7.iloc[:,0].tolist()
Q_7 = List_7.iloc[:,1].tolist()
PV_7 = List_7.iloc[:,2].tolist()
PEL_7 = List_7.iloc[:,3].tolist()
TM_7 = List_7.iloc[:,4].tolist()
Cel_7 = List_7.iloc[:,5].tolist()

#print(Cel_7)
if Ordner == 'Results/Optimierung/TWW/Clusterday/':
    Q_TWW_0 = List_0.iloc[:,6].tolist()
    Q_TWW_1 = List_1.iloc[:,6].tolist()
    Q_TWW_2 = List_2.iloc[:,6].tolist()
    Q_TWW_3 = List_3.iloc[:,6].tolist()
    Q_TWW_4 = List_4.iloc[:,6].tolist()
    Q_TWW_5 = List_5.iloc[:,6].tolist()
    Q_TWW_6 = List_6.iloc[:,6].tolist()
    Q_TWW_7 = List_7.iloc[:,6].tolist()

else:
    pass


#
#
#

T_Reihe = []
Q_Reihe = []
PV_Reihe = []
PEL_Reihe = []
QTWW_Reihe = []
Cel_Reihe = []
Modes_Zeitreihe = []
TM_Reihe = []

for i in range(0, len(T_Year)):
    if i % 96 == 0:
        if (round(T_Year[i],2)) == round(T_0[0], 2):
            for j in range(96, 192):
                T_Reihe.append(T_0[j])
                Modes_Zeitreihe.append(Modes_0[j])
                Q_Reihe.append(Q_0[j] * 4)
                PV_Reihe.append(PV_0[j] * 4)
                PEL_Reihe.append(PEL_0[j] * 4)
                Cel_Reihe.append(Cel_0[j])
                TM_Reihe.append(TM_0[j])
                if Ordner == 'Results/Optimierung/TWW/Clusterday/':
                    QTWW_Reihe.append(Q_TWW_0[j])
                else:
                    pass
        elif (round(T_Year[i],1)) == round(T_1[0], 1):
            for j in range(96, 192):
                T_Reihe.append(T_1[j])
                Modes_Zeitreihe.append(Modes_1[j])
                Q_Reihe.append(Q_1[j]*4)
                PV_Reihe.append(PV_1[j] * 4)
                PEL_Reihe.append(PEL_1[j] * 4)
                Cel_Reihe.append(Cel_1[j])
                TM_Reihe.append(TM_1[j])
                if Ordner == 'Results/Optimierung/TWW/Clusterday/':
                    QTWW_Reihe.append(Q_TWW_1[j])
                else:
                    pass


        elif (round(T_Year[i],1)) == round(T_2[0], 1):
            for j in range(96, 192):
                T_Reihe.append(T_2[j])
                Modes_Zeitreihe.append(Modes_2[j])
                Q_Reihe.append(Q_2[j] * 4 )
                PV_Reihe.append(PV_2[j] * 4)
                PEL_Reihe.append(PEL_2[j] * 4)
                Cel_Reihe.append(Cel_2[j])
                TM_Reihe.append(TM_2[j])
                if Ordner == 'Results/Optimierung/TWW/Clusterday/':
                    QTWW_Reihe.append(Q_TWW_2[j])
                else:
                    pass

#
        elif (round(T_Year[i],1)) == round(T_3[96], 1):
            for j in range(96, 192):
                T_Reihe.append(T_3[j])
                Modes_Zeitreihe.append(Modes_3[j])
                Q_Reihe.append(Q_3[j] * 4)
                PV_Reihe.append(PV_3[j] * 4)
                PEL_Reihe.append(PEL_3[j] * 4)
                Cel_Reihe.append(Cel_3[j])
                TM_Reihe.append(TM_3[j])
                if Ordner == 'Results/Optimierung/TWW/Clusterday/':
                    QTWW_Reihe.append(Q_TWW_3[j])
                else:
                    pass

#
        elif (round(T_Year[i],2)) == round(T_4[0], 2):
            for j in range(96, 192):
                T_Reihe.append(T_4[j])
                Modes_Zeitreihe.append(Modes_4[j])
                Q_Reihe.append(Q_4[j] * 4)
                PV_Reihe.append(PV_4[j] * 4)
                PEL_Reihe.append(PEL_4[j] * 4)
                Cel_Reihe.append(Cel_4[j])
                TM_Reihe.append(TM_4[j])
                if Ordner == 'Results/Optimierung/TWW/Clusterday/':
                    QTWW_Reihe.append(Q_TWW_4[j])
                else:
                    pass
        elif (round(T_Year[i],1)) == round(T_5[0], 1):
            for j in range(96, 192):
                T_Reihe.append(T_5[j])
                Modes_Zeitreihe.append(Modes_5[j])
                Q_Reihe.append(Q_5[j] * 4)
                PV_Reihe.append(PV_5[j] * 4)
                PEL_Reihe.append(PEL_5[j] * 4)
                Cel_Reihe.append(Cel_5[j])
                TM_Reihe.append(TM_5[j])
                if Ordner == 'Results/Optimierung/TWW/Clusterday/':
                    QTWW_Reihe.append(Q_TWW_5[j])
                else:
                    pass

        elif (round(T_Year[i], 0)) == round(T_6[0],0):
            for j in range(96, 192):
                T_Reihe.append(T_6[j])
                Modes_Zeitreihe.append(Modes_6[j])
                Q_Reihe.append(Q_6[j] * 4)
                PV_Reihe.append(PV_6[j] * 4)
                PEL_Reihe.append(PEL_6[j] * 4)
                Cel_Reihe.append(Cel_6[j])
                TM_Reihe.append(TM_6[j])
                if Ordner == 'Results/Optimierung/TWW/Clusterday/':
                    QTWW_Reihe.append(Q_TWW_6[j])
                else:
                    pass

        elif (round(T_Year[i],1)) == round(T_7[0], 1):
            for j in range(96, 192):
                T_Reihe.append(T_7[j])
                Modes_Zeitreihe.append(Modes_7[j])
                Q_Reihe.append(Q_7[j] * 4)
                PV_Reihe.append(PV_7[j] * 4)
                PEL_Reihe.append(PEL_7[j] * 4)
                Cel_Reihe.append(Cel_7[j])
                TM_Reihe.append(TM_7[j])
                if Ordner == 'Results/Optimierung/TWW/Clusterday/':
                    QTWW_Reihe.append(Q_TWW_7[j])
                else:
                    pass

        else:
            print(i)
            pass
else:
    pass
#print(List_3)
if Ordner == 'Results/Optimierung/TWW/Clusterday/':
    Data = list(zip(T_Reihe, Q_Reihe, PV_Reihe, PEL_Reihe, TM_Reihe, Cel_Reihe, QTWW_Reihe))
    Save_path = 'Results/Optimierung/TWW/'
else:
    Data = list(zip(T_Reihe, Q_Reihe, PV_Reihe, PEL_Reihe, TM_Reihe, Cel_Reihe))
    Save_path = 'Results/Optimierung/Puffer/'
Modes = list(Modes_Zeitreihe)

#print(T_Reihe)
#print(max(Q_Reihe))
#print(len(T_Reihe))
#print(len(Q_Reihe))


Datafile = Save_path + 'Data' + Savename
Modesfile = Save_path + 'Modes' + Savename


with open(Datafile, "w", newline="") as I:
    writer = csv.writer(I)
    for values in Data:
        writer.writerow(values)

with open(Modesfile, "w", newline="") as I:
    writer = csv.writer(I)
    for values in Modes:
        writer.writerow(values)

#print((T_Reihe))

#T_Cluster = Year.iloc[:,0]
#with open('file_1.csv', 'r') as f:
#    first_value_file_1 = next(f).split(',')[0]
#
## Create a new csv file
#with open('new_file.csv', mode='w', newline='') as new_file:
#
#    # Loop through the 8 files
#    for i in range(1, 9):
#
#        # Read the first value of the current file
#        with open(f'file_{i}.csv', 'r') as f:
#            first_value_current_file = next(f).split(',')[0]
#
#        # Check if the first value of the current file matches the first value of file_1
#        if first_value_file_1 == first_value_current_file:
#
#            # Append the current file to the new csv file
#            with open(f'file_{i}.csv', 'r') as f:
#                next(f) # Skip the first line (we already checked it)
#                for line in f:
#                    new_file.write(line)
#
#print(T_Cluster)