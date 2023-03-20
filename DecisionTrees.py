import sklearn
from sklearn.datasets import load_iris
from sklearn import tree
import graphviz
import numpy as np
import csv
from sklearn import tree


#import os
#os.environ["PATH"] += os.pathsep + 'D:/lma-mma/Interpreter/Library/bin'


data = []
with open ("Data_1440_1_168_4_24.csv") as file:
    reader = csv.reader(file, delimiter=",")
    for row in reader:
        row_values = [float(val) for val in row]
        data.append(row_values)
TWW = False
if TWW == True:
    fn = ('T_Air', 'Q_Hou_Dem', 'P_PV', 'P_EL_Dem', 'T_Sto', 'T_TWW', 'Q_TWW',  'COP_1', 'COP_2', 'T_Mean')
else:
    fn = ('T_Air', 'Q_Hou_Dem', 'P_PV', 'P_EL_Dem', 'T_Sto', 'COP_1', 'COP_2', 'T_Mean')

y_Opti = np.loadtxt("Modes_1440_1_168_4_24.csv")


x, y = data, y_Opti
clf = tree.DecisionTreeClassifier()
clf = clf.fit(x, y)
print (x , y)

#tree.plot_tree(clf)



dot_data = tree.export_graphviz(clf, out_file=None,
                     feature_names= fn,
                     #class_names=data,
                     filled=True, rounded=True,
                     special_characters=True)
graph = graphviz.Source(dot_data)
tree.plot_tree(clf)
graph = graphviz.Source(dot_data)
graph.render('Test')
#graph.save