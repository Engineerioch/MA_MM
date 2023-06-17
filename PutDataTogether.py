import pickle
import csv

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tikzplotlib
from plot_results_to_files import pp_figure

######## In this file, the results from the Typedays are put together to create a clustered year
# First the data is red in
# Therefore you should define the first two variables of the data you want to use
TRY = 'normal'
Strompreis = 'Fix'
Ordner = 'Results/Optimierung/TWW/Clusterday/'
Dataname= Ordner + 'Data_0_025_48_4_24_Clusterday_'
Modesname= Ordner + 'Modes_0_025_48_4_24_Clusterday_'
# Change the last part of the following line, if the storage sizes are not Small and Norm
filename_rest = '_' + TRY + '_' + Strompreis +'_TWW_Small_Norm.csv'
#
#
#
Savename = '_0_025_8760_4_24_Clusteryear' + filename_rest


# Create Lists of the data from the file for each variable and typeday

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
HP_0 = List_0.iloc[:,6].tolist()
Pen_0 = List_0.iloc[:,7].tolist()

Data_Modes_1 = pd.read_csv(Modesname + "1" + filename_rest, header=None)
Modes_1 = Data_Modes_1.values.tolist()
List_1 = pd.read_csv(Dataname + "1" + filename_rest, header=None)
T_1 = List_1.iloc[:,0].tolist()
Q_1 = List_1.iloc[:,1].tolist()
PV_1 = List_1.iloc[:,2].tolist()
PEL_1 = List_1.iloc[:,3].tolist()
TM_1 = List_1.iloc[:,4].tolist()
Cel_1 = List_1.iloc[:,5].tolist()
HP_1 = List_1.iloc[:,6].tolist()
Pen_1 = List_1.iloc[:,7].tolist()

Data_Modes_2 = pd.read_csv(Modesname + "2" + filename_rest, header=None)
Modes_2 = Data_Modes_2.values.tolist()
List_2 = pd.read_csv(Dataname + "2" + filename_rest, header=None)
T_2 = List_2.iloc[:,0].tolist()
Q_2 = List_2.iloc[:,1].tolist()
PV_2 = List_2.iloc[:,2].tolist()
PEL_2 = List_2.iloc[:,3].tolist()
TM_2 = List_2.iloc[:,4].tolist()
Cel_2 = List_2.iloc[:,5].tolist()
HP_2 = List_2.iloc[:,6].tolist()
Pen_2 = List_2.iloc[:,7].tolist()

Data_Modes_3 = pd.read_csv(Modesname + "3" + filename_rest, header=None)
Modes_3 = Data_Modes_3.values.tolist()
List_3 = pd.read_csv(Dataname + "3" + filename_rest, header=None)
T_3 = List_3.iloc[:,0].tolist()
Q_3 = List_3.iloc[:,1].tolist()
PV_3 = List_3.iloc[:,2].tolist()
PEL_3 = List_3.iloc[:,3].tolist()
TM_3 = List_3.iloc[:,4].tolist()
Cel_3 = List_3.iloc[:,5].tolist()
HP_3 = List_3.iloc[:,6].tolist()
Pen_3 = List_3.iloc[:,7].tolist()

Data_Modes_4 = pd.read_csv(Modesname + "4" + filename_rest, header=None)
Modes_4 = Data_Modes_4.values.tolist()
List_4 = pd.read_csv(Dataname + "4" + filename_rest, header=None)
T_4 = List_4.iloc[:,0].tolist()
Q_4 = List_4.iloc[:,1].tolist()
PV_4 = List_4.iloc[:,2].tolist()
PEL_4 = List_4.iloc[:,3].tolist()#
TM_4 = List_4.iloc[:,4].tolist()
Cel_4 = List_4.iloc[:,5].tolist()
HP_4 = List_4.iloc[:,6].tolist()
Pen_4 = List_4.iloc[:,7].tolist()

Data_Modes_5 = pd.read_csv(Modesname + "5" + filename_rest, header=None)
Modes_5 = Data_Modes_5.values.tolist()
List_5 = pd.read_csv(Dataname + "5" + filename_rest, header=None)
T_5 = List_5.iloc[:,0].tolist()
Q_5 = List_5.iloc[:,1].tolist()
PV_5 = List_5.iloc[:,2].tolist()
PEL_5 = List_5.iloc[:,3].tolist()
TM_5 = List_5.iloc[:,4].tolist()
Cel_5 = List_5.iloc[:,5].tolist()
HP_5 = List_5.iloc[:,6].tolist()
Pen_5 = List_5.iloc[:,7].tolist()

Data_Modes_6 = pd.read_csv(Modesname + "6" + filename_rest, header=None)
Modes_6 = Data_Modes_6.values.tolist()
List_6 = pd.read_csv(Dataname + "6" + filename_rest, header=None)
T_6 = List_6.iloc[:,0].tolist()
Q_6 = List_6.iloc[:,1].tolist()
PV_6 = List_6.iloc[:,2].tolist()
PEL_6 = List_6.iloc[:,3].tolist()
TM_6 = List_6.iloc[:,4].tolist()
Cel_6 = List_6.iloc[:,5].tolist()
HP_6 = List_6.iloc[:,6].tolist()
Pen_6 = List_6.iloc[:,7].tolist()

Data_Modes_7 = pd.read_csv(Modesname + "7" + filename_rest, header=None)
Modes_7 = Data_Modes_7.values.tolist()
List_7 = pd.read_csv(Dataname + "7" + filename_rest, header=None)
T_7 = List_7.iloc[:,0].tolist()
Q_7 = List_7.iloc[:,1].tolist()
PV_7 = List_7.iloc[:,2].tolist()
PEL_7 = List_7.iloc[:,3].tolist()
TM_7 = List_7.iloc[:,4].tolist()
Cel_7 = List_7.iloc[:,5].tolist()
HP_7 = List_7.iloc[:,6].tolist()
Pen_7 = List_7.iloc[:,7].tolist()

#
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

T_Reihe = []
Q_Reihe = []
PV_Reihe = []
PEL_Reihe = []
QTWW_Reihe = []
Cel_Reihe = []
Modes_Zeitreihe = []
TM_Reihe = []
HP_Reihe = []
Pen_Reihe = []
Days_Reihe = []

# If the first temperature of a day is equel to the first temperature of a typeday, then the data of the second optimized day are appended to the list

for i in range(0, len(T_Year)):
    if i % 96 == 0:
        if (round(T_Year[i],2)) == round(T_0[0], 2):
            for j in range(96, 192):
                T_Reihe.append(T_0[j])
                Modes_Zeitreihe.append(Modes_0[j])
                Q_Reihe.append(Q_0[j] )
                PV_Reihe.append(PV_0[j])
                PEL_Reihe.append(PEL_0[j])
                Cel_Reihe.append(Cel_0[j])
                TM_Reihe.append(TM_0[j])
                HP_Reihe.append(HP_0[j])
                Pen_Reihe.append(Pen_0[j])

                if Ordner == 'Results/Optimierung/TWW/Clusterday/':
                    QTWW_Reihe.append(Q_TWW_0[j])
                else:
                    pass
            Days_Reihe.append([1])
        elif (round(T_Year[i],1)) == round(T_1[0], 1):
            for j in range(96, 192):
                T_Reihe.append(T_1[j])
                Modes_Zeitreihe.append(Modes_1[j])
                Q_Reihe.append(Q_1[j])
                PV_Reihe.append(PV_1[j])
                PEL_Reihe.append(PEL_1[j])
                Cel_Reihe.append(Cel_1[j])
                TM_Reihe.append(TM_1[j])
                HP_Reihe.append(HP_1[j])
                Pen_Reihe.append(Pen_1[j])
                if Ordner == 'Results/Optimierung/TWW/Clusterday/':
                    QTWW_Reihe.append(Q_TWW_1[j])
                else:
                    pass
            Days_Reihe.append([2])


        elif (round(T_Year[i],1)) == round(T_2[0], 1):
            for j in range(96, 192):
                T_Reihe.append(T_2[j])
                Modes_Zeitreihe.append(Modes_2[j])
                Q_Reihe.append(Q_2[j] )
                PV_Reihe.append(PV_2[j] )
                PEL_Reihe.append(PEL_2[j] )
                Cel_Reihe.append(Cel_2[j])
                TM_Reihe.append(TM_2[j])
                HP_Reihe.append(HP_2[j])
                Pen_Reihe.append(Pen_2[j])
                if Ordner == 'Results/Optimierung/TWW/Clusterday/':
                    QTWW_Reihe.append(Q_TWW_2[j])
                else:
                    pass
            Days_Reihe.append([3])

#
        elif (round(T_Year[i],1)) == round(T_3[96], 1):
            for j in range(96, 192):
                T_Reihe.append(T_3[j])
                Modes_Zeitreihe.append(Modes_3[j])
                Q_Reihe.append(Q_3[j] )
                PV_Reihe.append(PV_3[j] )
                PEL_Reihe.append(PEL_3[j] )
                Cel_Reihe.append(Cel_3[j])
                TM_Reihe.append(TM_3[j])
                HP_Reihe.append(HP_3[j])
                Pen_Reihe.append(Pen_3[j])
                if Ordner == 'Results/Optimierung/TWW/Clusterday/':
                    QTWW_Reihe.append(Q_TWW_3[j])
                else:
                    pass
            Days_Reihe.append([4])

#
        elif (round(T_Year[i],2)) == round(T_4[0], 2):
            for j in range(96, 192):
                T_Reihe.append(T_4[j])
                Modes_Zeitreihe.append(Modes_4[j])
                Q_Reihe.append(Q_4[j] )
                PV_Reihe.append(PV_4[j] )
                PEL_Reihe.append(PEL_4[j])
                Cel_Reihe.append(Cel_4[j])
                TM_Reihe.append(TM_4[j])
                HP_Reihe.append(HP_4[j])
                Pen_Reihe.append(Pen_4[j])
                if Ordner == 'Results/Optimierung/TWW/Clusterday/':
                    QTWW_Reihe.append(Q_TWW_4[j])
                else:
                    pass
            Days_Reihe.append([5])
        elif (round(T_Year[i],1)) == round(T_5[0], 1):
            for j in range(96, 192):
                T_Reihe.append(T_5[j])
                Modes_Zeitreihe.append(Modes_5[j])
                Q_Reihe.append(Q_5[j] )
                PV_Reihe.append(PV_5[j] )
                PEL_Reihe.append(PEL_5[j] )
                Cel_Reihe.append(Cel_5[j])
                TM_Reihe.append(TM_5[j])
                HP_Reihe.append(HP_5[j])
                Pen_Reihe.append(Pen_5[j])

                if Ordner == 'Results/Optimierung/TWW/Clusterday/':
                    QTWW_Reihe.append(Q_TWW_5[j])
                else:
                    pass
            Days_Reihe.append([6])
        elif (round(T_Year[i], 0)) == round(T_6[0],0):
            for j in range(96, 192):
                T_Reihe.append(T_6[j])
                Modes_Zeitreihe.append(Modes_6[j])
                Q_Reihe.append(Q_6[j] )
                PV_Reihe.append(PV_6[j] )
                PEL_Reihe.append(PEL_6[j] )
                Cel_Reihe.append(Cel_6[j])
                TM_Reihe.append(TM_6[j])
                HP_Reihe.append(HP_6[j])
                Pen_Reihe.append(Pen_6[j])

                if Ordner == 'Results/Optimierung/TWW/Clusterday/':
                    QTWW_Reihe.append(Q_TWW_6[j])
                else:
                    pass
            Days_Reihe.append([7])

        elif (round(T_Year[i],1)) == round(T_7[0], 1):
            for j in range(96, 192):
                T_Reihe.append(T_7[j])
                Modes_Zeitreihe.append(Modes_7[j])
                Q_Reihe.append(Q_7[j] )
                PV_Reihe.append(PV_7[j] )
                PEL_Reihe.append(PEL_7[j] )
                Cel_Reihe.append(Cel_7[j])
                TM_Reihe.append(TM_7[j])
                HP_Reihe.append(HP_7[j])
                Pen_Reihe.append(Pen_7[j])

                if Ordner == 'Results/Optimierung/TWW/Clusterday/':
                    QTWW_Reihe.append(Q_TWW_7[j])
                else:
                    pass
            Days_Reihe.append([8])
        else:
            print(i)
            pass
else:
    pass

# Create zipped lists to save the lists
if Ordner == 'Results/Optimierung/TWW/Clusterday/':
    Data = list(zip(T_Reihe, Q_Reihe, PV_Reihe, PEL_Reihe, TM_Reihe, Cel_Reihe, QTWW_Reihe))
    Save_path = 'Results/Optimierung/TWW/'
else:
    Data = list(zip(T_Reihe, Q_Reihe, PV_Reihe, PEL_Reihe, TM_Reihe, Cel_Reihe))
    Save_path = 'Results/Optimierung/Puffer/'
Modes = list(Modes_Zeitreihe)
Days = list(Days_Reihe)

# Save the new lists of data in Data and Modesfile

Datafile = Save_path + 'Data' + Savename
Modesfile = Save_path + 'Modes' + Savename


with open(Datafile, "w", newline="") as I:
    writer = csv.writer(I)
    for values in Data:
        writer.writerow(values)
#
with open(Modesfile, "w", newline="") as I:
    writer = csv.writer(I)
    for values in Modes:
        writer.writerow(values)


plt.rcParams.update(pp_figure)


