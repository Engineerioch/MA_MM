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
from plot_results_to_files import latex_base
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import confusion_matrix
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
from plot_results_to_files import latex_twothird
import tikzplotlib

plt.rcParams.update(latex_base)


File_Stem = '0_025_8760_4_24_Clusteryear_cold_Fix_TWW_Small_Norm'
File_Stem_Test = '0_025_8760_4_24_Clusteryear_normal_Fix_TWW_Small_Norm'
Speicherort = "D:/lma-mma/Repos/MA_MM/Datensicherung/Plots/DT/"
SaveFile_Stem = 'Januar_cold.csv'

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
Testdatei = "0_025_744_4_24_TRY_cold_Fix_TWW_Small_Norm"
with open (Pfad + "Input_" + Testdatei + '.csv') as file:
    reader = csv.reader(file, delimiter=",")
    for i, row in enumerate(reader):
        row_values = [float(val) for val in row]
        filtered = [row[0]] + [str(float(row[1])*4)] + [row[i] for i in range(2, 4)]+ [row[5]] + [str(float(row[6]))]
        testdata.append(filtered)

y_Testdata = np.loadtxt(Pfad + "Modes_" + Testdatei + '.csv', skiprows=0)


X_train, X_test, y_train, y_test = train_test_split(data, y_Opti, random_state=0)
Tiefe = 10
max_features = 5
criterion =  'gini'
min_samples_split = 30
min_samples_leaf = 20
ccp_alpha = 0.005

Accuracy_origin = []
Accuracy_test = []

MaximumTiefe = 11

for i in range(1, MaximumTiefe, 1):
    clf = tree.DecisionTreeClassifier(criterion=criterion, max_depth=i, ccp_alpha=ccp_alpha, max_features=max_features,
    min_samples_leaf=min_samples_leaf, min_samples_split=min_samples_split, splitter= 'best')


#clf = tree.DecisionTreeClassifier(criterion="gini")
    clf = clf.fit(data, y_Opti)

    y_predTestdata = clf.predict(testdata)
    y_pred1 = clf.predict(X_test)

    Accuracy_origin.append(accuracy_score(y_test, y_pred1))
    Accuracy_test.append(accuracy_score(y_Testdata, y_predTestdata))
x = np.arange(1, 11, 1)
fig, ax = plt.subplots()
plt.plot(x, Accuracy_origin)
plt.plot(x, Accuracy_test)
ax.set_xlabel('Baumtiefe')
ax.set_ylabel('Genauigkeit')
leg = ax.legend(['Testset', 'Validierungsset'])

#plt.savefig(Speicherort + 'GenauigkeitVergleichFinalerBaum.svg')
#tikzplotlib.save(Speicherort + 'GenauigkeitVergleichFinalerBaum')
plt.savefig(Speicherort + 'GenauigkeitVergleichFinalerBaum.pdf')
plt.show()

print(Accuracy_origin)
print(Accuracy_test)
if predict == True:


    clf = tree.DecisionTreeClassifier(criterion=criterion, max_depth=Tiefe, max_features=max_features, min_samples_split = min_samples_split,
                                  min_samples_leaf = min_samples_leaf, splitter="best")

clf = clf.fit(data, y_Opti)
#
dot_data = tree.export_graphviz(clf, out_file=None,
                     feature_names= fn,
                     class_names=cn,
                     filled=True, rounded=True,
                     special_characters=True,
                                impurity=True,
                                rotate=True,
                                proportion=False,
                                fontname='serif')

graph = graphviz.Source(dot_data)
tree.plot_tree(clf)
graph = graphviz.Source(dot_data)
graph.render(Speicherort + 'FinalerBaum')
plt.savefig(Speicherort + 'FinalerBaum.svg')
tikzplotlib.save((Speicherort + 'FinalerBaum'))
plt.show
#
y_predTestdata = clf.predict(testdata)
print(accuracy_score(y_Testdata, y_predTestdata))

############################ Predict the Mode for the Data that will be put in Simulation ##############################

###### Jahresmodi-Datei (predicted)
#
#
x_Prediction = []
with open (Pfad + "Input_0_025_744_4_24_TRY_cold_Fix_TWW_Small_Norm.csv") as Pred_File:
    reader =  csv.reader(Pred_File, delimiter = ",")
    for row in reader:
        row_values = [float(val) for val in row]
        filtered = [row[0]] + [str(float(row[1])*4)] + [row[i] for i in range(2, 4)]+ [row[5]] + [str(float(row[6]))]
        x_Prediction.append(filtered)


y_Jahr = clf.predict(x_Prediction)
print(accuracy_score(y_Testdata, y_Jahr))

##
M0 = []
M1 = []
M2 = []
M3 = []
i = 0
for element in y_Jahr:
##
    if y_Jahr[i] == 0:
        M0.append(1)
    else:
        M0.append(0)
    if y_Jahr[i] == 1:
        M1.append(1)
    else:
        M1.append(0)
    if y_Jahr[i] == 2:
        M2.append(1)
    else:
        M2.append(0)
    if y_Jahr[i] == 3:
        M3.append(1)
    else:
        M3.append(0)
    i = i +1


ResultPath = 'D:/lma-mma/Repos/MA_MM/Results/DecisionTrees/'
Dataname= 'SimMode_'
SaveMode = list(zip(M0, M1, M2, M3))
SaveFile_Stem = 'Januar_cold.csv'
with open(ResultPath+'Modes_'+SaveFile_Stem, "w", newline="") as I:
    writer = csv.writer(I)
    for values in SaveMode:
        writer.writerow(values)
