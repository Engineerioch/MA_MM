import sklearn
from sklearn.datasets import load_iris
from sklearn import tree
import graphviz



#import os
#os.environ["PATH"] += os.pathsep + 'D:/lma-mma/Interpreter/Library/bin'

data = load_iris()
data.target[[10, 25, 24]]
list(data.target_names)
print(data)
print(data.target_names)


from sklearn import tree
iris = load_iris()
x, y = iris.data, iris.target
clf = tree.DecisionTreeClassifier()
clf = clf.fit(x, y)

#tree.plot_tree(clf)



dot_data = tree.export_graphviz(clf, out_file=None,
                     feature_names=iris.feature_names,
                     class_names=iris.target_names,
                     filled=True, rounded=True,
                     special_characters=True)
graph = graphviz.Source(dot_data)
tree.plot_tree(clf)
graph = graphviz.Source(dot_data)
graph.render('iris')
#graph.save