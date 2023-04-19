import sklearn
from sklearn.datasets import load_iris
from sklearn import tree
import graphviz
import numpy as np
import csv
from sklearn import tree
import sklearn
import matplotlib.pyplot as plt

#import os
#os.environ["PATH"] += os.pathsep + 'D:/lma-mma/Interpreter/Library/bin'

Pfad = 'D:/lma-mma/Repos/MA_MM/Results/Optimierung/TWW/'
data = []
with open (Pfad + "Input_1080_1_360_4_24_Cluster_normal_Var_TWW_Medium_Norm.csv") as file:
    reader = csv.reader(file, delimiter=",")
    for row in reader:
        row_values = [float(val) for val in row]
        data.append(row_values)
TWW = True
if TWW == True:
    fn = ('T_Air', 'Q_Hou_Dem', 'P_PV', 'P_EL_Dem', 'Q_TWW') #, 'c_grid')#, 'T_TWW', 'Q_TWW',  'COP_1', 'COP_2', 'T_Mean')
    cn = ('Modus 0', 'Modus 1', 'Modus 2', 'Modus 3')
else:
    fn = ('T_Air', 'Q_Hou_Dem', 'P_PV', 'P_EL_Dem', 'T_Sto', 'COP_1', 'COP_2', 'T_Mean')
    cn = ('Modus 0', 'Modus 1', 'Modus 2')
y_Opti = np.loadtxt(Pfad + "Modes_1080_1_360_4_24_Cluster_normal_Var_TWW_Medium_Norm.csv")



x, y = data, y_Opti
clf = tree.DecisionTreeClassifier(criterion="gini", splitter="best")#, max_depth=None, min_samples_split=2, min_samples_leaf=2, max_features=None)
clf = clf.fit(x, y)
#print (x , y)


dot_data = tree.export_graphviz(clf, out_file=None,
                     feature_names= fn,
                     class_names=cn,
                     filled=True, rounded=True,
                     special_characters=True
                                )

graph = graphviz.Source(dot_data)
tree.plot_tree(clf)
graph = graphviz.Source(dot_data)
graph.render('Test_')

plt.show()