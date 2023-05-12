import pickle
import csv

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tikzplotlib

#Data_0_025_48_4_24_Clusterday_0_normal_Var_TWW_Medium_Norm
TRY = 'warm'
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
HP_Reihe = []
Pen_Reihe = []
Days_Reihe = []

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
            #print(i)
            #print(T_6[0])
            #print(T_Year[i])
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
#print(List_3)
if Ordner == 'Results/Optimierung/TWW/Clusterday/':
    Data = list(zip(T_Reihe, Q_Reihe, PV_Reihe, PEL_Reihe, TM_Reihe, Cel_Reihe, QTWW_Reihe))
    Save_path = 'Results/Optimierung/TWW/'
else:
    Data = list(zip(T_Reihe, Q_Reihe, PV_Reihe, PEL_Reihe, TM_Reihe, Cel_Reihe))
    Save_path = 'Results/Optimierung/Puffer/'
Modes = list(Modes_Zeitreihe)
Days = list(Days_Reihe)
#print(T_Reihe)
#print(max(Q_Reihe))
print(len(T_Reihe))
#print(len(Q_Reihe))


Datafile = Save_path + 'Data' + Savename
Modesfile = Save_path + 'Modes' + Savename
Daysfile = Save_path + 'Days' + Savename


with open(Datafile, "w", newline="") as I:
    writer = csv.writer(I)
    for values in Data:
        writer.writerow(values)
#
with open(Modesfile, "w", newline="") as I:
    writer = csv.writer(I)
    for values in Modes:
        writer.writerow(values)

#with open(Daysfile, "w", newline="") as I:
#    writer = csv.writer(I)
#    for values in Days:
#        writer.writerow(values)

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
from plot_results_to_files import latex_base
plt.rcParams.update(latex_base)

#print(Days)
count = {}
for sublist in Days:
    for num in sublist:
        if num in count:
            count[num] += 1
        else:
            count[num] = 1

#print(count)


#x = range(1, 9)
#keys = sorted(count.keys())
#values = [count[key] for key in keys]
#
#plt.bar(keys, values, width=0.5)
#plt.xlabel('Nummer des Typtages')
#plt.ylabel('Häufigkeit des Typtages')
Safeordner = 'D://lma-mma/Repos/MA_MM/Datensicherung/Plots/'
#plt.savefig(Safeordner + 'HaeufigkeitClustertage_' + TRY + '.svg')
#plt.savefig(Safeordner + 'HaeufigkeitClustertage_' + TRY + '.pdf')
#tikzplotlib.save(Safeordner + 'HaeufigkeitClustertage_' + TRY + '.tex')
#plt.show()
#print(values)
#Januar = range(1,32)
#x = list(range(1, len(Days)+1))
#y = [d[0] for d in Days]
#
#plt.plot(x[0:31], y[0:31], drawstyle='steps', label= 'Januar')
##plt.plot(x[0:30], y[31:61], drawstyle='steps', label= 'Februar')
#plt.plot(x[0:30], y[91:121], drawstyle='steps', label= 'April')
#plt.plot(x[0:31], y[182:213], drawstyle='steps', label= 'Juli')
#plt.plot(x[0:30], y[273:303], drawstyle='steps', label= 'Oktober')
##plt.plot(x[0:31], y[334:366], drawstyle='steps', label= 'Oktober')
##plt.plot(x[0:31], y[121:152], drawstyle='steps', label='Mai')
#
#plt.ylim([0.7, 8.3])
#plt.xlim([0.3, 31.7])
##plt.yticks(np.arange(0.5, 9, step=1))
#plt.legend()
#plt.xlabel('Tag im Monat')
#plt.ylabel('Typtag')
#plt.legend(loc='center left', bbox_to_anchor=(1, 0.82))
#plt.savefig(Safeordner + 'Clustertage4Monatsverlauf_' + TRY + '.svg')
#plt.savefig(Safeordner + 'Clustertage4Monatsverlauf_' + TRY + '.pdf')
#tikzplotlib.save(Safeordner + 'Clustertage4Monatsverlauf_' + TRY + '.tex')
##plt.title('Data Plot')
#plt.show()
#
#
#
#
#x = range(1, 9)
#keys = sorted(count.keys())
#values = [count[key] for key in keys]
#warm = [16, 42, 36, 32, 47, 65, 63, 64]
#kalt= [61, 34, 34, 19, 77, 62, 53, 25]
#normal = [36, 51, 67, 16, 72, 46, 41, 36]
## Define the x values
#x = np.arange(1,len(warm)+1)
#
## Set the width of the bars
#width = 0.25
#
## Create the figure and axes objects
#fig, ax = plt.subplots()
## Plot the data
#ax.bar(x - width, warm, width=width, label='warm')
#ax.bar(x, normal, width=width, label='normal')
#ax.bar(x + width, kalt, width=width, label='kalt')
#ax.set_ylim(0,95)
## Set the axis labels and legend
#ax.set_xlabel('Nummer des Typtages')
#ax.set_ylabel('Häufigkeit des Typtages im Jahr')
#ax.legend(loc ='upper left')
## Show the plot
#plt.savefig(Safeordner + 'HaeufigkeitClustertage_Alle_TRY.svg')
#plt.savefig(Safeordner + 'HaeufigkeitClustertage_Alle_TRY.pdf')
#tikzplotlib.save(Safeordner + 'HaeufigkeitClustertage_Alle_TRY.tex')
#plt.show()
T_0_neu = [x - 273.15 for x in T_0[:96]]
T_1_neu = [x - 273.15 for x in T_1[:96]]
T_2_neu = [x - 273.15 for x in T_2[:96]]
T_3_neu = [x - 273.15 for x in T_3[:96]]
T_4_neu = [x - 273.15 for x in T_4[:96]]
T_5_neu = [x - 273.15 for x in T_5[:96]]
T_6_neu = [x - 273.15 for x in T_6[:96]]
T_7_neu = [x - 273.15 for x in T_7[:96]]
#
fig, ax = plt.subplots()
x2 = np.arange(len(T_0))
ax.plot(x2[0:96]/4, T_0_neu, label='kalter Wintertag') #1
ax.plot(x2[0:96]/4, T_2_neu, label='Wintertag') #3
ax.plot(x2[0:96]/4, T_1_neu, label='Regentag') #2
ax.plot(x2[0:96]/4, T_3_neu, label='Frühlingstag') #4
ax.plot(x2[0:96]/4, T_6_neu, label='Sommertag') #7
ax.plot(x2[0:96]/4, T_4_neu, label='Hochsommertag') #5
ax.plot(x2[0:96]/4, T_5_neu, label='Herbsttag') #6
ax.plot(x2[0:96]/4, T_7_neu, label='kühler Herbsttag', color='grey', linestyle=(0,(5,5))) #8
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.ylabel('Temperatur in °C')
plt.xlabel('Tageszeit in h')
#plt.savefig(Safeordner + 'Temperaturverlauf_'+TRY+'.svg')
#plt.savefig(Safeordner + 'Temperaturverlauf_'+TRY+'.pdf')
#tikzplotlib.save(Safeordner + 'Temperaturverlauf_'+TRY+'.tex')
plt.show()
#print(sum(T_0_neu)/96)