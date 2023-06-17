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

### tSe Variant here: DB: use the original disturbances, GB: clustered disturbances
Variante= 'DB'

## File-stem to get the data from
if Variante == 'GB':
    File_Stem = '0_025_8760_4_24_Clusteryear_normal_Fix_TWW_Small_Norm'
else:
    File_Stem = '0_025_8736_4_24_TRY_normal_Fix_TWW_Small_Norm'


#Set location to save the results
Speicherort = "/Datensicherung/Plots/DT/"

# Import Data to create DT
TWW = True

if TWW == True:
    fn = ('T_Air', 'Q_Hou_Dem', 'P_PV', 'P_EL_Dem', 'c_grid' ,'Q_TWW')
    cn = ('Modus 0', 'Modus 1', 'Modus 2', 'Modus 3')
    Pfad = 'D:/lma-mma/Repos/MA_MM/Results/Optimierung/TWW/'
else:
    fn = ('T_Air', 'Q_Hou_Dem', 'P_PV', 'P_EL_Dem', 'T_Mean' , 'c_grid')
    cn = ('Modus 0', 'Modus 1', 'Modus 2')
    Pfad = 'D:/lma-mma/Repos/MA_MM/Results/Optimierung/Puffer/'


# Import Feature Data
data = []
with open (Pfad + "Data_" + File_Stem + '.csv') as file:
    reader = csv.reader(file, delimiter=",")
    for i, row in enumerate(reader):
        row_values = [float(val) for val in row]
        filtered = [row[0]] + [str(float(row[i])) for i in range(1, 4)]+ [row[5]] + [str(float(row[6]))]
        data.append(filtered)

y_Opti = np.loadtxt(Pfad + "Modes_"+ File_Stem + ".csv", skiprows=0)

#Import Signal-Data
testdata= []
Testdatei = "744_025_672_4_24_TRY_warm_Fix_TWW_Small_Norm"
#Testdatei = "0_025_8736_4_24_TRY_warm_Fix_TWW_Small_Norm"
with open (Pfad + "Data_" + Testdatei + '.csv') as file:
    reader = csv.reader(file, delimiter=",")
    for i, row in enumerate(reader):
        row_values = [float(val) for val in row]
        filtered = [row[0]] + [str(float(row[i])) for i in range(1, 4)] + [row[5]] + [str(float(row[6]))]
        testdata.append(filtered)

y_Testdata = np.loadtxt(Pfad + "Modes_" + Testdatei + '.csv', skiprows=0)

filtered = [row[0]] + [str(float(row[i])) for i in range(1, 4)]+ [row[5]] + [str(float(row[6]))]

########################################################################################################################
######################################### Create Decision Trees ########################################################

X_train, X_test, y_train, y_test = train_test_split(data, y_Opti, random_state=0)
clf = tree.DecisionTreeClassifier(criterion="gini", max_depth=9, max_features=None, splitter="best")
clf = clf.fit(data, y_Opti)
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
graph.render(Speicherort + 'UrsprünglicherBaum'+Variante)
plt.savefig(Speicherort + 'UrsprünglicherBaum'+Variante+'.svg')
tikzplotlib.save((Speicherort + 'UrsprünglicherBaum'+Variante+'.tex'))
plt.show()

# Predict Modes from decision tree
y_predTestdata = clf.predict(testdata)
y_pred1 = clf.predict(X_test)

################################# Predict outcome with other parts of Splitted Data from Decision Tree ##################
score1 = clf.score(X_test, y_test)
print('Genauigkeit mit dem Validierungsset ist: '+ str(score1))
score2 = clf.score(testdata, y_Testdata)
print('Genauigkeit mit dem Testset ist: '+ str(score2))

################################ Create Confusion Matrix before CV #####################################################
Con_PrePun_Training = ConfusionMatrixDisplay.from_predictions(y_test, y_pred1, cmap=plt.cm.YlOrRd)
plt.xlabel("Prognostizierter Modus")
plt.ylabel("Wahrer Modus")
plt.savefig(Speicherort + 'CM_Vor_CV_ValsetCluster_BT9'+Variante+'.svg')
tikzplotlib.save(Speicherort + 'CM_Vor_CV_ValsetCluster_BT9'+Variante+'.tex')
plt.savefig(Speicherort + 'CM_Vor_CV_ValsetCluster_BT9'+Variante+'.pdf')
plt.show()

Con_PrePun_Test = ConfusionMatrixDisplay.from_predictions(y_Testdata, y_predTestdata, cmap=plt.cm.YlOrRd)
plt.xlabel("Prognostizierter Modus")
plt.ylabel("Wahrer Modus")
plt.savefig(Speicherort + 'CM_Vor_CV_TestsetTRY_BT9'+Variante+'.svg')
tikzplotlib.save(Speicherort + 'CM_Vor_CV_TestsetTRY_BT9'+Variante+'.tex')
plt.savefig(Speicherort + 'CM_Vor_CV_TestsetTRY_BT9'+Variante+'.pdf')
plt.show()

##### Plot both Confusion Matrixes next to each other
fig, axs = plt.subplots(1, 2, figsize=(6.5, 2.9), sharey=True)#, gridspec_kw={'width_ratios': [1, 1]})
C1 = confusion_matrix(y_test, y_pred1)
C2 = confusion_matrix(y_Testdata, y_predTestdata)
disp = ConfusionMatrixDisplay(C1).plot(cmap=plt.cm.YlOrRd, ax=axs[0])
disp.im_.colorbar.remove()
disp.ax_.set_xlabel('Validierungsset')
disp.ax_.set_ylabel('Wahrer Modus')
disp.ax_.set_aspect('equal')#, adjustable='box')


disp2 = ConfusionMatrixDisplay(C2).plot(cmap=plt.cm.YlOrRd, ax=axs[1])
disp2.ax_.set_xlabel('Testset')
disp2.ax_.set_ylabel('')
disp2.ax_.set_aspect('equal')#, adjustable='box')
plt.subplots_adjust(wspace=0.2, left=0.125, right=0.9, bottom=0.1, top=0.9, hspace=0.2)
fig.text(0.4,0.013, "Prognostizierter Modus", ha='left')
#
plt.tight_layout()
plt.savefig(Speicherort + 'CM_Vor_CV_Doppel_BT9'+Variante+'.svg')
tikzplotlib.save(Speicherort + 'CM_Vor_CV_Doppel_BT9'+Variante)
plt.savefig(Speicherort + 'CM_Vor_CV_Doppel_BT9'+Variante+'.pdf')
plt.show()


print('Genauigkeit des einfachen Baumes mit dem Validierungsset ist: ' + str(accuracy_score(y_test, y_pred1)))
print('Genauigkeit des einfachen Baumes mit dem Testset TRY ist: ' + str(accuracy_score(y_Testdata, y_predTestdata)))



###################################GridSearch mit Cross-Validation#####################################################
#Set parameters you want to test here:
params_tree = {
    'criterion':  ['gini'],
    'max_depth':  [8],
    'max_features': [2, 3, 4, 5, 6],
    'splitter': ['best'],
    'min_samples_split': [25, 30, 50, 100, 120, 150],
    'min_samples_leaf': [15, 20, 50,100]
}
#Set parameters for Cross Validation
clf = GridSearchCV(
    estimator=tree.DecisionTreeClassifier(),
    param_grid=params_tree,
    cv=5,
    n_jobs=-1,
    verbose=1,
)

Baum = clf.fit(X_train, y_train)
print(Baum.best_params_)

best_params = Baum.best_params_
dt = tree.DecisionTreeClassifier(criterion=best_params['criterion'], max_depth=best_params['max_depth'], max_features=best_params['max_features'],
min_samples_leaf=best_params['min_samples_leaf'], min_samples_split=best_params['min_samples_split'], splitter= best_params['splitter'])
dt.fit(X_train, y_train)
tree.plot_tree(dt)

graph = graphviz.Source(dot_data)
graph.render(Speicherort + 'BaumNachCV'+Variante)
plt.savefig(Speicherort + 'BaumNachCV'+Variante+'.svg')
tikzplotlib.save((Speicherort + 'BaumNachCV'+Variante+'.tex'))
plt.show()


y_predTestdataACV = dt.predict(testdata)
y_pred2 = dt.predict(X_test)

################################ Create Confusion Matrix after Grid-Search #####################################################

print('Genauigkeit nach dem Pre-Puning ist mit dem Validierungsset: ' + str(accuracy_score(y_test, y_pred2)))
print('Genauigkeit nach dem Pre-Puning ist mit dem Testset: ' + str(accuracy_score(y_Testdata, y_predTestdataACV)))
Con_Pruning = ConfusionMatrixDisplay.from_predictions(y_Testdata, y_predTestdataACV, cmap=plt.cm.YlOrRd)

plt.xlabel("Prognostizierter Modus nach dem Pre-Puning")
plt.ylabel("Wahrer Modus")


fig, axs = plt.subplots(1, 2, figsize=(6.5, 2.9), sharey=True)#, gridspec_kw={'width_ratios': [1, 1]})
##labels = "Modus 0", "Modus 1", "Modus 2", "Modus 3"
C1 = confusion_matrix(y_test, y_pred2)
C2 = confusion_matrix(y_Testdata, y_predTestdataACV)
##
###
disp = ConfusionMatrixDisplay(C1).plot(cmap=plt.cm.YlOrRd, ax=axs[0])
disp.im_.colorbar.remove()
disp.ax_.set_xlabel('Validierungsset')
disp.ax_.set_ylabel('Wahrer Modus')
disp.ax_.set_aspect('equal')#, adjustable='box')

###
disp2 = ConfusionMatrixDisplay(C2).plot(cmap=plt.cm.YlOrRd, ax=axs[1])
disp2.ax_.set_xlabel('Testset')
disp2.ax_.set_ylabel('')
disp2.ax_.set_aspect('equal')#, adjustable='box')
plt.subplots_adjust(wspace=0.2, left=0.125, right=0.9, bottom=0.1, top=0.9, hspace=0.2)
fig.text(0.4,0.013, "Prognostizierter Modus nach Grid Search", ha='left')

plt.savefig(Speicherort + 'CM_Nach_CV_Doppel'+Variante+'.svg')
tikzplotlib.save(Speicherort + 'CM_Nach_CV_Doppel'+Variante+'.tex')
plt.savefig(Speicherort + 'CM_Nach_CV_Doppel'+Variante+'.pdf')
plt.tight_layout()
plt.show()



###################################### Alpha über Unreinheit ###########################################################
path = dt.cost_complexity_pruning_path(X_train, y_train)
ccp_alphas, impurities = path.ccp_alphas, path.impurities
#
fig, ax = plt.subplots()
ax.plot(ccp_alphas[:-1], impurities[:-1], marker="", drawstyle="steps-post")
ax.set_xlabel("Effektives " + r'$\alpha$')
ax.set_ylabel("Unreinheit der Blätter")
plt.rcParams.update(latex_base)

plt.rcParams.update(latex_base)
plt.savefig(Speicherort + 'Alpha_Unreinheit_Val'+Variante+'.svg')
tikzplotlib.save(Speicherort + 'Alpha_Unreinheit_Val'+Variante+'.tex')
plt.savefig(Speicherort + 'Alpha_Unreinheit_Val'+Variante+'.pdf')
plt.show()

tree.DecisionTreeClassifier(criterion=best_params['criterion'], max_depth=best_params['max_depth'], max_features=best_params['max_features'],
min_samples_leaf=best_params['min_samples_leaf'], min_samples_split=best_params['min_samples_split'], splitter= best_params['splitter'])
##
##
clfs = []
for ccp_alpha in ccp_alphas:
    PostPrune = tree.DecisionTreeClassifier(random_state=0, ccp_alpha=ccp_alpha, criterion=best_params['criterion'], max_features=best_params['max_features'],
    min_samples_leaf=best_params['min_samples_leaf'], min_samples_split=best_params['min_samples_split'], splitter= best_params['splitter'])

    PostPrune.fit(X_train, y_train)
    clfs.append(PostPrune)
##
print(
    "Anzahl der Knoten im letzten Baum ist: {} with ccp_alpha: {}".format(
        clfs[-1].tree_.node_count, ccp_alphas[-1])
        )

clfs = clfs[:-1]
ccp_alphas = ccp_alphas[:-1]
##
node_counts = [PostPrune.tree_.node_count for PostPrune in clfs]
depth = [PostPrune.tree_.max_depth for PostPrune in clfs]
fig, ax = plt.subplots(2, 1)
ax[0].plot(ccp_alphas, node_counts,  drawstyle="steps-post")
ax[0].set_xlabel(r'$\alpha$')
ax[0].set_ylabel("Anzahl der Knoten")
ax[1].plot(ccp_alphas, depth, drawstyle='steps-post')
ax[1].set_xlabel(r'$\alpha$')
ax[1].set_ylabel("Baumtiefe")
fig.tight_layout()

plt.savefig(Speicherort + 'AnzahlKnoten_BT_ueber_Alpha'+Variante+'.svg')
tikzplotlib.save(Speicherort + 'AnzahlKnoten_BT_ueber_Alpha'+Variante+'.tex')
plt.savefig(Speicherort + 'AnzahlKnoten_BT_ueber_Alpha'+Variante+'.pdf')


plt.show()



train_scores = [PostPrune.score(X_train, y_train) for PostPrune in clfs]
test_scores = [PostPrune.score(X_test, y_test) for PostPrune in clfs]
test_scoresTRY = [PostPrune.score(testdata, y_Testdata) for PostPrune in clfs]
###
fig, ax = plt.subplots()
ax.set_xlabel(r'$\alpha$')
ax.set_ylabel("Genauigkeit")
##ax.set_title("GenaugikeitTrainings- und Testsets")
ax.plot(ccp_alphas, train_scores, marker=".", label="Validierungsset", drawstyle="steps-post")
#ax.plot(ccp_alphas, test_scores, marker=".", label="Testset aus dem geclusterten Jahr", drawstyle="steps-post")
ax.plot(ccp_alphas, test_scoresTRY, marker=".", label="Testset", drawstyle='steps-post')
ax.legend()

plt.savefig(Speicherort + 'Genauigkeit_ueber_Alpha_TV'+Variante+'.svg')
tikzplotlib.save(Speicherort + 'Genauigkeit_ueber_Alpha_TV'+Variante+'.tex')
plt.savefig(Speicherort + 'Genauigkeit_ueber_Alpha_TV'+Variante+'.pdf')
plt.show()

###### Reinzoomen ####


fig, ax = plt.subplots()
ax.set_xlabel(r'$\alpha$')
ax.set_ylabel("Genauigkeit")
ax.plot(ccp_alphas, train_scores, marker=".", label="Validierungsset", drawstyle="steps-post")
ax.plot(ccp_alphas, test_scoresTRY, marker=".", label="Testset", drawstyle='steps-post')
ax.legend()
ax.set_xlim([0.00, 0.001])
ax.set_ylim([0.7, 1])


plt.savefig(Speicherort + 'Genauigkeit_ueber_Alpha_TV_zoom'+Variante+'.svg')
tikzplotlib.save(Speicherort + 'Genauigkeit_ueber_Alpha_TV_zoom'+Variante+'.tex')
plt.savefig(Speicherort + 'Genauigkeit_ueber_Alpha_TV_zoom'+Variante+'.pdf')
plt.show()

### Now take the parameters from this file and create the final tree in the file 'Final_DT'