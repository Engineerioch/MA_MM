import sklearn
from sklearn.datasets import load_iris
from sklearn import tree
import graphviz
import numpy as np
import csv
import pandas as pd
from sklearn import tree
import sklearn
import matplotlib.pyplot as plt
import matplotlib as mpl
from plot_results_to_files import latex_fullpage
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import confusion_matrix
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
from plot_results_to_files import latex_base

import tikzplotlib

plt.rcParams.update(latex_base)
Variante = 'Stopp'
if Variante == 'GB':
    File_origin_start = '0_025_8760_4_24_'
    File_origin_end = '_Fix_TWW_Small_Norm'
    File_Stem = File_origin_start +'Clusteryear_normal'+ File_origin_end
else:
    File_origin_start = '0_025_8736_4_24_'
    File_origin_end = '_Fix_TWW_Small_Norm'
    File_Stem = File_origin_start +'TRY_normal'+ File_origin_end

#File_Stem_Test = '0_025_8760_4_24_Clusteryear_normal_Fix_TWW_Small_Norm'
Speicherort = "D:/lma-mma/Repos/MA_MM/Datensicherung/Plots/DT/"

# Import Data to create DT
    # Set if the Modes for fmu-simulation should be predicted

predict = True

fn = ('T_Air', 'Q_Hou_Dem', 'P_PV', 'P_EL_Dem', 'c_grid' ,'Q_TWW')
#so wird Data TRY gespeichert:    T_Air, Q_Hou, P_PV, P_EL_Dem, T_Mean, c_grid, Q_TWW, T_Sto, T_TWW, COP_1, COP_2
#so wird Data Clusteryear gespeichert: T_Reihe, Q_Reihe, PV_Reihe, PEL_Reihe, TM_Reihe, Cel_Reihe, QTWW_Reihe
cn = ('Modus 0', 'Modus 1', 'Modus 2', 'Modus 3')
Pfad = 'D:/lma-mma/Repos/MA_MM/Results/Optimierung/TWW/'


# Import Feature Data
data = []
with open (Pfad + "Data_" + File_Stem + '.csv') as file:
    reader = csv.reader(file, delimiter=",")
    for i, row in enumerate(reader):
        row_values = [float(val) for val in row]
        filtered = [row[0]] + [str(float(row[i]) ) for i in range(1, 4)]+ [row[5]] + [str(float(row[6]))]
        data.append(filtered)
y_Opti = np.loadtxt(Pfad + "Modes_"+ File_Stem + ".csv", skiprows=0)

#Import Signal-Data
testdata= []
#Testdatei = "744_025_672_4_24_TRY_warm_Fix_TWW_Small_Norm"
Testdatei = '744_025_672_4_24_TRY_warm' + File_origin_end
with open (Pfad + "Input_" + Testdatei + '.csv') as file:
    reader = csv.reader(file, delimiter=",")
    for i, row in enumerate(reader):
        row_values = [float(val) for val in row]
        filtered = [row[0]] + [str(float(row[1]))] + [row[i] for i in range(2, 4)]+ [row[5]] + [str(float(row[6]))]
        testdata.append(filtered)

y_Testdata = np.loadtxt(Pfad + "Modes_" + Testdatei + '.csv', skiprows=0)


X_train, X_test, y_train, y_test = train_test_split(data, y_Opti, random_state=0)
Tiefe = 7
max_features = 5
criterion =  'gini'
splitter = 'best'
min_samples_split = 100
min_samples_leaf = 20
ccp_alpha = 0.00018

Accuracy_origin = []
Accuracy_test = []
Accuracy_log = []
MaximumTiefe = 11

for i in range(1, MaximumTiefe, 1):
    clf = tree.DecisionTreeClassifier(criterion=criterion, max_depth=i, ccp_alpha=ccp_alpha, max_features=max_features,
    min_samples_leaf=min_samples_leaf, min_samples_split=min_samples_split, splitter= splitter)


#clf = tree.DecisionTreeClassifier(criterion="gini")
    clf = clf.fit(data, y_Opti)

    y_predTestdata = clf.predict(testdata)
    y_pred1 = clf.predict(X_test)

    Accuracy_origin.append(accuracy_score(y_test, y_pred1))
    Accuracy_test.append(accuracy_score(y_Testdata, y_predTestdata))


    dot_data = tree.export_graphviz(clf, out_file=None,
                                    feature_names=fn,
                                    class_names=cn,
                                    filled=True, rounded=True,
                                    special_characters=True,
                                    impurity=True,
                                    rotate=True,
                                    proportion=False,
                                    fontname='serif')
    plt.rcParams.update(latex_fullpage)
    graph = graphviz.Source(dot_data)
    tree.plot_tree(clf)
#    graph = graphviz.Source(dot_data)
#    graph.render(Speicherort + 'FinalerBaum_BT' + str(i) + '_'+Variante + '.pdf')
#    tikzplotlib.save((Speicherort + 'FinalerBaum' + str(i)) + '_'+Variante + '.tex')

    y_predTestdata = clf.predict(testdata)

    print('Accuracy score bei Baumtiefe ' + str(i) + ' ist: ' + (str(accuracy_score(y_Testdata, y_predTestdata))))
    x_Prediction = []
    with open(Pfad + "Input_0_025_8736_4_24_TRY_warm_Fix_TWW_Small_Norm.csv") as Pred_File:
        reader = csv.reader(Pred_File, delimiter=",")
        for row in reader:
            row_values = [float(val) for val in row]
            filtered = [row[0]] + [str(float(row[1]))] + [row[i] for i in range(2, 4)] + [row[5]] + [str(float(row[6]))]
            x_Prediction.append(filtered)

    y_JahrTrue = np.loadtxt(Pfad + "Modes_" + '0_025_8736_4_24_TRY_warm_Fix_TWW_Small_Norm' + '.csv', skiprows=0)

    y_JahrPred = clf.predict(x_Prediction)
    Accuracy_log.append(accuracy_score(y_JahrTrue,y_JahrPred))
    print(accuracy_score(y_JahrTrue, y_JahrPred))

    C1 = confusion_matrix(y_JahrTrue, y_JahrPred)
    plt.rcParams.update(latex_base)
    fig = plt.figure(figsize=(4, 4))
    disp = ConfusionMatrixDisplay(C1).plot(cmap=plt.cm.YlOrRd)
    disp.ax_.set_xlabel('Prognostizierter Modus')
    disp.ax_.set_ylabel('Wahrer Modus')
    disp.ax_.set_aspect('equal')
 #   plt.savefig(Speicherort + 'Con_Final' + str(i) + '_' + Variante + '.pdf')
    plt.show()

    M0 = []
    M1 = []
    M2 = []
    M3 = []
    j = 0
    for element in y_JahrPred:
        ##
        if y_JahrPred[j] == 0:
            M0.append(1)
        else:
            M0.append(0)
        if y_JahrPred[j] == 1:
            M1.append(1)
        else:
            M1.append(0)
        if y_JahrPred[j] == 2:
            M2.append(1)
        else:
            M2.append(0)
        if y_JahrPred[j] == 3:
            M3.append(1)
        else:
            M3.append(0)
        j = j + 1

    ResultPath = 'D:/lma-mma/Repos/MA_MM/Results/DecisionTrees/'
    Dataname = 'SimMode_'
    SaveMode = list(zip(M0, M1, M2, M3))
    SaveFile_Stem = 'Jahr_warm' + str(i) + '_' + Variante + '.csv'
    with open(ResultPath + 'Modes_' + SaveFile_Stem, "w", newline="") as I:
        writer = csv.writer(I)
        for values in SaveMode:
            writer.writerow(values)

plt.rcParams.update(latex_base)
x = np.arange(1, 11, 1)
fig, ax = plt.subplots()
plt.plot(x, Accuracy_origin)
plt.plot(x, Accuracy_test)
ax.set_xlabel('Baumtiefe')
ax.set_ylabel('Genauigkeit')
leg = ax.legend(['Validierungsset','Testset'])
#plt.savefig(Speicherort + 'GenauigkeitVergleichFinalerBaum'+Variante+'.svg')
#tikzplotlib.save(Speicherort + 'GenauigkeitVergleichFinalerBaum'+Variante+'.tex')
#plt.savefig(Speicherort + 'GenauigkeitVergleichFinalerBaum'+Variante+'.pdf')
plt.show()

print(Accuracy_origin)
print(Accuracy_test)


############################ Predict the Mode for the Data that will be put in Simulation ##############################

###### Jahresmodi-Datei (predicted)
#





#Monatsdatenstamm = "_4_24_TRY_warm_Fix_TWW_Small_Norm"
#Januar_testdata  = []
#Februar_testdata  = []
#Maerz_testdata  = []
#April_testdata  = []
#Mai_testdata  = []
#Juni_testdata  = []
#Juli_testdata  = []
#August_testdata  = []
#September_testdata  = []
#Oktober_testdata  = []
#November_testdata  = []
#Dezember_testdata  = []
#
#with open (Pfad + "Input_" + '0_025_744' + Monatsdatenstamm + '.csv') as file:
#    reader = csv.reader(file, delimiter=",")
#    for i, row in enumerate(reader):
#        row_values = [float(val) for val in row]
#        filtered = [row[0]] + [str(float(row[1])*4)] + [row[i] for i in range(2, 4)]+ [row[5]] + [str(float(row[6]))]
#        Januar_testdata.append(filtered)
#y_JanuarTrue = np.loadtxt(Pfad + "Modes_" + '0_025_744_4_24_TRY_warm_Fix_TWW_Small_Norm'+ '.csv', skiprows=0)
#y_JanuarPred = clf.predict(Januar_testdata)
#Accuracy_log.append(accuracy_score(y_JanuarTrue, y_JanuarPred))
#
#with open (Pfad + "Input_" + '744_025_672' + Monatsdatenstamm + '.csv') as file:
#    reader = csv.reader(file, delimiter=",")
#    for i, row in enumerate(reader):
#        row_values = [float(val) for val in row]
#        filtered = [row[0]] + [str(float(row[1])*4)] + [row[i] for i in range(2, 4)]+ [row[5]] + [str(float(row[6]))]
#        Februar_testdata.append(filtered)
#y_FebruarTrue = np.loadtxt(Pfad + "Modes_" + '744_025_672_4_24_TRY_warm_Fix_TWW_Small_Norm'+ '.csv', skiprows=0)
#y_FebruarPred = clf.predict(Februar_testdata)
#Accuracy_log.append(accuracy_score(y_FebruarTrue, y_FebruarPred))
#
#with open (Pfad + "Input_" + '1416_025_744' + Monatsdatenstamm + '.csv') as file:
#    reader = csv.reader(file, delimiter=",")
#    for i, row in enumerate(reader):
#        row_values = [float(val) for val in row]
#        filtered = [row[0]] + [str(float(row[1])*4)] + [row[i] for i in range(2, 4)]+ [row[5]] + [str(float(row[6]))]
#        Maerz_testdata.append(filtered)
#y_MaerzTrue = np.loadtxt(Pfad + "Modes_" + '1416_025_744_4_24_TRY_warm_Fix_TWW_Small_Norm'+ '.csv', skiprows=0)
#y_MaerzPred = clf.predict(Maerz_testdata)
#Accuracy_log.append(accuracy_score(y_MaerzTrue, y_MaerzPred))
#
#with open(Pfad + "Input_" + '2160_025_720' + Monatsdatenstamm + '.csv') as file:
#    reader = csv.reader(file, delimiter=",")
#    for i, row in enumerate(reader):
#        row_values = [float(val) for val in row]
#        filtered = [row[0]] + [str(float(row[1]) * 4)] + [row[i] for i in range(2, 4)] + [row[5]] + [
#            str(float(row[6]))]
#        April_testdata.append(filtered)
#y_AprilTrue = np.loadtxt(Pfad + "Modes_" + '2160_025_720_4_24_TRY_warm_Fix_TWW_Small_Norm'+ '.csv', skiprows=0)
#y_AprilPred = clf.predict(April_testdata)
#Accuracy_log.append(accuracy_score(y_AprilTrue, y_AprilPred))
#
#with open (Pfad + "Input_" + '2880_025_744' + Monatsdatenstamm + '.csv') as file:
#    reader = csv.reader(file, delimiter=",")
#    for i, row in enumerate(reader):
#        row_values = [float(val) for val in row]
#        filtered = [row[0]] + [str(float(row[1])*4)] + [row[i] for i in range(2, 4)]+ [row[5]] + [str(float(row[6]))]
#        Mai_testdata.append(filtered)
#y_MaiTrue = np.loadtxt(Pfad + "Modes_" + '2880_025_744_4_24_TRY_warm_Fix_TWW_Small_Norm'+ '.csv', skiprows=0)
#y_MaiPred = clf.predict(Mai_testdata)
#Accuracy_log.append(accuracy_score(y_MaiTrue, y_MaiPred))
#
#with open (Pfad + "Input_" + '3624_025_720' + Monatsdatenstamm + '.csv') as file:
#    reader = csv.reader(file, delimiter=",")
#    for i, row in enumerate(reader):
#        row_values = [float(val) for val in row]
#        filtered = [row[0]] + [str(float(row[1])*4)] + [row[i] for i in range(2, 4)]+ [row[5]] + [str(float(row[6]))]
#        Juni_testdata.append(filtered)
#y_JuniTrue = np.loadtxt(Pfad + "Modes_" + '3624_025_720_4_24_TRY_warm_Fix_TWW_Small_Norm'+ '.csv', skiprows=0)
#y_JuniPred = clf.predict(Juni_testdata)
#Accuracy_log.append(accuracy_score(y_JuniTrue, y_JuniPred))
#
#with open (Pfad + "Input_" + '4344_025_744' + Monatsdatenstamm + '.csv') as file:
#    reader = csv.reader(file, delimiter=",")
#    for i, row in enumerate(reader):
#        row_values = [float(val) for val in row]
#        filtered = [row[0]] + [str(float(row[1])*4)] + [row[i] for i in range(2, 4)]+ [row[5]] + [str(float(row[6]))]
#        Juli_testdata.append(filtered)
#y_JuliTrue = np.loadtxt(Pfad + "Modes_" + '4344_025_744_4_24_TRY_warm_Fix_TWW_Small_Norm'+ '.csv', skiprows=0)
#y_JuliPred = clf.predict(Juli_testdata)
#Accuracy_log.append(accuracy_score(y_JuliTrue, y_JuliPred))
#
#with open(Pfad + "Input_" + '5088_025_744' + Monatsdatenstamm + '.csv') as file:
#    reader = csv.reader(file, delimiter=",")
#    for i, row in enumerate(reader):
#        row_values = [float(val) for val in row]
#        filtered = [row[0]] + [str(float(row[1]) * 4)] + [row[i] for i in range(2, 4)] + [row[5]] + [str(float(row[6]))]
#        August_testdata.append(filtered)
#y_AugustTrue = np.loadtxt(Pfad + "Modes_" + '5088_025_744_4_24_TRY_warm_Fix_TWW_Small_Norm'+ '.csv', skiprows=0)
#y_AugustPred = clf.predict(August_testdata)
#Accuracy_log.append(accuracy_score(y_AugustTrue, y_AugustPred))
#
#
#with open (Pfad + "Input_" + '5832_025_720' + Monatsdatenstamm + '.csv') as file:
#    reader = csv.reader(file, delimiter=",")
#    for i, row in enumerate(reader):
#        row_values = [float(val) for val in row]
#        filtered = [row[0]] + [str(float(row[1])*4)] + [row[i] for i in range(2, 4)]+ [row[5]] + [str(float(row[6]))]
#        September_testdata.append(filtered)
#y_SeptemberTrue = np.loadtxt(Pfad + "Modes_" + '5832_025_720_4_24_TRY_warm_Fix_TWW_Small_Norm'+ '.csv', skiprows=0)
#y_SeptemberPred = clf.predict(September_testdata)
#Accuracy_log.append(accuracy_score(y_SeptemberTrue, y_SeptemberPred))
#
#with open (Pfad + "Input_" + '6552_025_744' + Monatsdatenstamm + '.csv') as file:
#    reader = csv.reader(file, delimiter=",")
#    for i, row in enumerate(reader):
#        row_values = [float(val) for val in row]
#        filtered = [row[0]] + [str(float(row[1])*4)] + [row[i] for i in range(2, 4)]+ [row[5]] + [str(float(row[6]))]
#        Oktober_testdata.append(filtered)
#y_OktoberTrue = np.loadtxt(Pfad + "Modes_" + '6552_025_744_4_24_TRY_warm_Fix_TWW_Small_Norm'+ '.csv', skiprows=0)
#y_OktoberPred = clf.predict(Oktober_testdata)
#Accuracy_log.append(accuracy_score(y_OktoberTrue, y_OktoberPred))
#
#
#with open (Pfad + "Input_" + '7296_025_720' + Monatsdatenstamm + '.csv') as file:
#    reader = csv.reader(file, delimiter=",")
#    for i, row in enumerate(reader):
#        row_values = [float(val) for val in row]
#        filtered = [row[0]] + [str(float(row[1])*4)] + [row[i] for i in range(2, 4)]+ [row[5]] + [str(float(row[6]))]
#        November_testdata.append(filtered)
#y_NovemberTrue = np.loadtxt(Pfad + "Modes_" + '7296_025_720_4_24_TRY_warm_Fix_TWW_Small_Norm'+ '.csv', skiprows=0)
#y_NovemberPred = clf.predict(November_testdata)
#Accuracy_log.append(accuracy_score(y_NovemberTrue, y_NovemberPred))
#
#with open (Pfad + "Input_" + '8016_025_720' + Monatsdatenstamm + '.csv') as file:
#    reader = csv.reader(file, delimiter=",")
#    for i, row in enumerate(reader):
#        row_values = [float(val) for val in row]
#        filtered = [row[0]] + [str(float(row[1])*4)] + [row[i] for i in range(2, 4)]+ [row[5]] + [str(float(row[6]))]
#        Dezember_testdata.append(filtered)
#y_DezemberTrue = np.loadtxt(Pfad + "Modes_" + '8016_025_720_4_24_TRY_warm_Fix_TWW_Small_Norm'+ '.csv', skiprows=0)
#y_DezemberPred = clf.predict(Dezember_testdata)
#Accuracy_log.append(accuracy_score(y_DezemberTrue, y_DezemberPred))
#plt.show()
#x = np.arange(0,12,1)
#plt.plot(x, Accuracy_log)
#plt.xlabel(['Januar', 'Februar','März','April','Mai', 'Juni','Juli','August','Semptember','Oktober'])#,'November','Dezember'])
#plt.ylabel('Gemauigkeit je Monat')
#plt.show()


##




