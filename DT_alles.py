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


ResultPath = 'D:/lma-mma/Repos/MA_MM/Results/DecisionTrees/'
File_Stem = '0_025_8760_4_24_Clusteryear_cold_Fix_TWW_Small_Norm'
File_Stem_Test = '0_025_8760_4_24_Clusteryear_normal_Fix_TWW_Small_Norm'
Speicherort = "D:/lma-mma/Repos/MA_MM/Datensicherung/"

# Import Data to create DT
    # Set if the Input-Data considers TWW
TWW = True

if TWW == True:
    fn = ('T_Air', 'Q_Hou_Dem', 'P_PV', 'P_EL_Dem', 'T_Mean', 'c_grid' ,'Q_TWW')
#so wird Data TRY gespeichert:    T_Air, Q_Hou, P_PV, P_EL_Dem, T_Mean, c_grid, Q_TWW, T_Sto, T_TWW, COP_1, COP_2
#so wird Data Clusteryear gespeichert: T_Reihe, Q_Reihe, PV_Reihe, PEL_Reihe, TM_Reihe, Cel_Reihe, QTWW_Reihe
    cn = ('Modus 0', 'Modus 1', 'Modus 2', 'Modus 3')
    Pfad = 'D:/lma-mma/Repos/MA_MM/Results/Optimierung/TWW/'
else:
    fn = ('T_Air', 'Q_Hou_Dem', 'P_PV', 'P_EL_Dem', 'T_Mean' , 'c_grid')
#so wird Data TRY gespeichert:    T_Air, Q_Hou, P_PV, P_EL_Dem, T_Mean, c_grid, T_Sto, COP_1, COP_2
#so wird Data Clusteryear gespeichert:    T_Reihe, Q_Reihe, PV_Reihe, PEL_Reihe, TM_Reihe, Cel_Reihe
    cn = ('Modus 0', 'Modus 1', 'Modus 2')
    Pfad = 'D:/lma-mma/Repos/MA_MM/Results/Optimierung/Puffer/'


# Import Feature Data
data = []
with open (Pfad + "Data_" + File_Stem + '.csv') as file:
    reader = csv.reader(file, delimiter=",")
    for i, row in enumerate(reader):
        row_values = [float(val) for val in row]
        data.append(row_values)
y_Opti = np.loadtxt(Pfad + "Modes_"+ File_Stem + ".csv", skiprows=0)

#Import Signal-Data
testdata= []
Testdatei = "0_025_744_4_24_TRY_cold_Fix_TWW_Small_Norm"
with open (Pfad + "Input_" + Testdatei + '.csv') as file:
    reader = csv.reader(file, delimiter=",")
    for i, row in enumerate(reader):
        row_values = [float(val) for val in row]
        testdata.append(row_values)

y_Testdata = np.loadtxt(Pfad + "Modes_" + Testdatei + '.csv', skiprows=0)




########################################################################################################################
######################################### Create Decision Trees ########################################################

#data1=[[1,2,1,1],[2,1,1,1],[1,2,2,2],[2,2,2,1]]
#s1 = [[0],[1],[0],[2]]
#fn= ["X[0]","X[1]","X[2]","X[3]"]


X_train, X_test, y_train, y_test = train_test_split(data, y_Opti, random_state=0)
clf = tree.DecisionTreeClassifier(criterion="gini", max_depth=9, max_features=None, splitter="best")

clf = clf.fit(data, y_Opti)
#
dot_data = tree.export_graphviz(clf, out_file=None,
                     feature_names= fn,
                     class_names=cn,
                     filled=True, rounded=True,
                     special_characters=True,
                                impurity=True,
                                rotate=False,
                                proportion=False,
                                )

graph = graphviz.Source(dot_data)
tree.plot_tree(clf)
graph = graphviz.Source(dot_data)
graph.render(Speicherort + 'Ursprünglicher Baum')
plt.savefig(Speicherort + 'UrsprünglicherBaum.svg')
tikzplotlib.save((Speicherort + 'UrsprünglicherBaum'))
plt.show

############################### Genauigkeit eines Uneschnittenen Baumes über die Tiefe #################################
#Accuracy_origin = []
#Accuracy_test = []

#MaximumTiefe = 15

#for i in range(1, MaximumTiefe, 1):
#clf = tree.DecisionTreeClassifier(criterion="gini", max_depth=i)

# clf = tree.DecisionTreeClassifier(criterion="gini")
#clf = clf.fit(data, y_Opti)

y_predTestdata = clf.predict(testdata)
y_pred1 = clf.predict(X_test)

#Accuracy_origin.append(accuracy_score(y_test, y_pred1))
#Accuracy_test.append(accuracy_score(y_Testdata, y_predTestdata))


#print(Accuracy_origin)
#print(Accuracy_test)


################################# Predict outcome with other parts of Splitted Data from Decision Tree ##################

y_pred1 = clf.predict(X_test)
score = clf.score(X_test, y_test)
y_predTestdata = clf.predict(testdata)
score = clf.score(testdata, y_predTestdata)

Com_PrePun = ConfusionMatrixDisplay.from_predictions(y_test, y_pred1, cmap=plt.cm.YlOrRd)
plt.xlabel("Prognostizierter Modus vor dem Pre-Puning")
plt.ylabel("Wahrer Modus")


#plt.plot(fig, ax1)
plt.show()

print(score)
print('Genauigkeit des einfachen Baumes mit den Testdaten aus dem geclusterten TRY ist: ' + str(accuracy_score(y_test, y_pred1)))
print('Genauigkeit des einfachen Baumes mit den Daten aus einem anderen Testset TRY ist: ' + str(accuracy_score(y_Testdata, y_predTestdata)))

################################## Cross Validaton mit GridSearch
params_tree = {
    'criterion':  ['gini', 'entropy'],
    'max_depth':  [5,6,7,8],
    'max_features': [2, 3, 4, 5, 6],
    'splitter': ['best'],
    'min_samples_split': [30, 50, 100, 120, 150],
    'min_samples_leaf': [30, 50,100]
}

clf = GridSearchCV(
    estimator=tree.DecisionTreeClassifier(),
    param_grid=params_tree,
    cv=5,
    n_jobs=-1,
    verbose=1,
)
#
#
#
Baum = clf.fit(X_train, y_train)
print(Baum.best_params_)
best_params = Baum.best_params_
dt = tree.DecisionTreeClassifier(criterion=best_params['criterion'], max_depth=best_params['max_depth'], max_features=best_params['max_features'],
min_samples_leaf=best_params['min_samples_leaf'], min_samples_split=best_params['min_samples_split'], splitter= best_params['splitter'])
dt.fit(X_train, y_train)

tree.plot_tree(dt)
##
#
##
##
y_predTestdataACV = dt.predict(testdata)
y_pred2 = dt.predict(X_test)
##
print('Genauigkeit nach dem Pre-Puning ist mit dem unbekannten Testset: ' + str(accuracy_score(y_Testdata, y_predTestdataACV)))
print('Genauigkeit nach dem Pre-Puning ist mit dem Testset: ' + str(accuracy_score(y_test, y_pred2)))
Con_Pruning = ConfusionMatrixDisplay.from_predictions(y_Testdata, y_predTestdataACV, cmap=plt.cm.YlOrRd)
#
#
plt.xlabel("Prognostizierter Modus nach dem Pre-Puning")
plt.ylabel("Wahrer Modus")
#plt.show()


####
##
##
fig, axs = plt.subplots(1, 2, figsize=(6.5, 2.9), sharey=True)#, gridspec_kw={'width_ratios': [1, 1]})
#labels = "Modus 0", "Modus 1", "Modus 2", "Modus 3"
C1 = confusion_matrix(y_test, y_pred1)
C2 = confusion_matrix(y_Testdata, y_predTestdataACV)
#
##
disp = ConfusionMatrixDisplay(C1).plot(cmap=plt.cm.YlOrRd, ax=axs[0])
disp.im_.colorbar.remove()
disp.ax_.set_xlabel('Prognostizierter Modus')
disp.ax_.set_ylabel('Wahrer Modus')
disp.ax_.set_aspect('equal')#, adjustable='box')
##
##
disp2 = ConfusionMatrixDisplay(C2).plot(cmap=plt.cm.YlOrRd, ax=axs[1])
disp2.ax_.set_xlabel('Prognostizierter Modus')
disp2.ax_.set_ylabel('')
disp2.ax_.set_aspect('equal')#, adjustable='box')
plt.subplots_adjust(wspace=0.2, left=0.125, right=0.9, bottom=0.1, top=0.9, hspace=0.2)
#fig.text(0.4,0, "Prognostizierter Modus", ha='left')
#
#
#
#plt.show()
##
#plt.tight_layout()
##plt.savefig()
##
##
##########################################################################################################################
##
#Best =
#
path = clf.cost_complexity_pruning_path(X_train, y_train)
ccp_alphas, impurities = path.ccp_alphas, path.impurities
##
#fig, ax = plt.subplots()
#ax.plot(ccp_alphas[:-1], impurities[:-1], marker="", drawstyle="steps-post")
#ax.set_xlabel("Effektives " + r'$\alpha$')
#ax.set_ylabel("Unreinheit der Blätter")
#plt.rcParams.update(latex_base)
#
#print(len(y_test)) -> 8760
###print(len(y_train)) -> 26280
plt.rcParams.update(latex_base)
#tikzplotlib.save('D://lma-mma/Repos/MA_MM/Test_base15')
#plt.savefig('D://lma-mma/Repos/MA_MM/Test_base15.pdf')
#plt.show()



#tree.DecisionTreeClassifier(criterion=best_params['criterion'], max_depth=best_params['max_depth'], max_features=best_params['max_features'],
#min_samples_leaf=best_params['min_samples_leaf'], min_samples_split=best_params['min_samples_split'], splitter= best_params['splitter'])
#
#
clfs = []
for ccp_alpha in ccp_alphas:
#    dt = tree.DecisionTreeClassifier(random_state=0, ccp_alpha=ccp_alpha, criterion=best_params['criterion'], max_features=best_params['max_features'],
#min_samples_leaf=best_params['min_samples_leaf'], min_samples_split=best_params['min_samples_split'], splitter= best_params['splitter'])

    PostPrune = tree.DecisionTreeClassifier(random_state=0, ccp_alpha=ccp_alpha)
    PostPrune.fit(X_train, y_train)
    clfs.append(PostPrune)
#
print(
    "Anzahl der Knoten im letzten Baum ist: {} with ccp_alpha: {}".format(
        clfs[-1].tree_.node_count, ccp_alphas[-1]
    )
)
##
#
clfs = clfs[:-1]
ccp_alphas = ccp_alphas[:-1]
#
node_counts = [PostPrune.tree_.node_count for PostPrune in clfs]
depth = [PostPrune.tree_.max_depth for PostPrune in clfs]
fig, ax = plt.subplots(2, 1)
ax[0].plot(ccp_alphas, node_counts,  drawstyle="steps-post")
ax[0].set_xlabel(r'$\alpha$')
ax[0].set_ylabel("Anzahl der Knoten")
#ax[0].set_title("Number of nodes vs alpha")
ax[1].plot(ccp_alphas, depth, drawstyle='steps-post')
ax[1].set_xlabel(r'$\alpha$')
ax[1].set_ylabel("Baumtiefe")
#ax[1].set_title("Baumtiefe vs " + r"$\alpha$")
fig.tight_layout()
#plt.savefig('D://lma-mma/Repos/MA_MM/Test_base2.pdf')
##
plt.show()
#
#
################ Import fresh Data to test Tree Accuracy ###########################
#Laenge = len(X_train)
#X_Cluster_RealTest = []
#with open (Pfad + "Data_" + File_Stem + '.csv') as file:
#    reader = csv.reader(file, delimiter=",")
#
#
#    for row in reader:
#        row_values = [float(val) for val in row]
#        X_Cluster_RealTest.append(row_values)
#
##Import Signal-Data
#y_Cluster_RealTest = np.loadtxt(Pfad + "Modes_"+ File_Stem_Test + ".csv", skiprows=0)
#X_RealTest = []
#y_RealTest = []
#for i in range(0, Laenge):
#    X_RealTest.append(X_Cluster_RealTest[i])
#    y_RealTest.append(y_Cluster_RealTest[i])
#
#y_pred3 = dt.predict(X_RealTest)
#
#
###
train_scores = [PostPrune.score(X_train, y_train) for PostPrune in clfs]
test_scores = [PostPrune.score(X_test, y_test) for PostPrune in clfs]
test_scoresTRY = [PostPrune.score(testdata, y_Testdata) for PostPrune in clfs]
###
fig, ax = plt.subplots()
ax.set_xlabel(r'$\alpha$')
ax.set_ylabel("Genauigkeit")
##ax.set_title("GenaugikeitTrainings- und Testsets")
ax.plot(ccp_alphas, train_scores, marker=".", label="Trainingsset", drawstyle="steps-post")
#ax.plot(ccp_alphas, test_scores, marker=".", label="Testset aus dem geclusterten Jahr", drawstyle="steps-post")
ax.plot(ccp_alphas, test_scoresTRY, marker=".", label="Testset", drawstyle='steps-post')
ax.legend()
plt.show()

fig, ax = plt.subplots()
ax.set_xlabel(r'$\alpha$')
ax.set_ylabel("Genauigkeit")
ax.plot(ccp_alphas, train_scores, marker=".", label="Trainingsset", drawstyle="steps-post")
ax.plot(ccp_alphas, test_scoresTRY, marker=".", label="Testset", drawstyle='steps-post')
ax.legend()

# Set x and y limits
ax.set_xlim([0.00, 0.03])
ax.set_ylim([0.74, 0.85])

plt.show()

#plt.savefig('D://lma-mma/Repos/MA_MM/Test_base3.pdf')
#
#



##    fig1, ax1, leg1 = create_plot()
##plt.savefig('D://lma-mma/Repos/MA_MM/Test_base.pdf')
#
##plt.rcParams.update(latex_twothird)
##    fig2, ax2, leg2 = create_plot()
##plt.savefig('D://lma-mma/Repos/MA_MM/Test_tt.pdf')
#
#
##graph.save
#

##### Jahresmodi-Datei (predicted)


#x_Prediction = []
#with open (Pfad + "Data_744_025_2880_4_24_TRY_normal_Var_TWW_Medium_Norm.csv") as Pred_File:
#    reader =  csv.reader(Pred_File, delimiter = ",")
#    for row in reader:
#        row_values = [float(val) for val in row]
#        x_Prediction.append(row_values)
#y_Jahr = clf.predict(x_Prediction)
#
#
#M0 = []
#M1 = []
#M2 = []
#M3 = []
#i = 0
#for element in y_Jahr:
#
#    if y_Jahr[i] == 0:
#        M0.append(1)
#    else:
#        M0.append(0)
#    if y_Jahr[i] == 1:
#        M1.append(1)
#    else:
#        M1.append(0)
#    if y_Jahr[i] == 2:
#        M2.append(1)
#    else:
#        M2.append(0)
#    if y_Jahr[i] == 3:
#        M3.append(1)
#    else:
#        M3.append(0)
#    i = i +1
#
##Dataname= 'SimMode_'
##
#if TWW == True:
#    SaveMode = list(zip(M0, M1, M2, M3))
#else:
#    SaveMode = list(zip(M0, M1, M2))
#
#with open(ResultPath+'Modes_'+SaveFile_Stem, "w", newline="") as I:
#    writer = csv.writer(I)
#    for values in SaveMode:
#        writer.writerow(values)
#
#
#dt

# NOCHT NICHT FERTIG GECODED!!
#Parameter_file = File_Stem
#all_devs = [clf, ]
#all_devs_names = [clf, ]
#pickle.dump(all_devs, open(Parameter_file, "wb"))
#with open(devs_file, "w") as file_devs:
#    for key in all_devs:
#        file_devs.write(all_devs_names[all_devs.index(key)])
#        file_devs.write('\n')
#        for x in key:
#            file_devs.write(str(x) + "=")
#            file_devs.write(str(key[x]))
#            file_devs.write('\n')
#        file_devs.write('\n')
#    file_devs.close()