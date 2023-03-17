import sklearn
from sklearn.datasets import load_iris
from sklearn import tree
import graphviz
import numpy as np
import csv



#import os
#os.environ["PATH"] += os.pathsep + 'D:/lma-mma/Interpreter/Library/bin'

data = load_iris()
data.target[[10, 25, 24]]
list(data.target_names)
print(data)
print(data.target_names)




from sklearn import tree
iris = load_iris()

data = []
with open ("Data_1440_1_168_4_24.csv") as file:
    reader = csv.reader(file, delimiter=",")
    for row in reader:
        row_values = [float(val) for val in row]
        data.append(row_values)



y_Opti = np.loadtxt("Modes_1440_1_168_4_24.csv")


x, y = data, y_Opti
clf = tree.DecisionTreeClassifier()
clf = clf.fit(x, y)
print (x , y)

#tree.plot_tree(clf)



dot_data = tree.export_graphviz(clf, out_file=None,
                     feature_names= ('T_Air', 'Q_Hou_Dem', 'P_PV', 'P_EL_Dem'),
                     #class_names=data,
                     filled=True, rounded=True,
                     special_characters=True)
graph = graphviz.Source(dot_data)
tree.plot_tree(clf)
graph = graphviz.Source(dot_data)
graph.render('iris')
#graph.save