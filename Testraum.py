import numpy as np
import math
import pandas as pd
import csv
import os
import parameter
import pickle as pickle






#myfile= "D://lma-mma/Repos/MA_MM/Cluster/OhneGewichtungCluster_Alle_1_15_1_3421_001_cold.pkl"
#objects = []
#with (open(myfile, "rb")) as openfile:#
#    while True:
#        try:
#            objects.append(pickle.load(openfile))
#        except EOFError:
#           break
#print(objects)
#
#print(objects["T_Air_8"])


##
##
##
#objects = pd.read_pickle(myfile)
#File= np.load(myfile, allow_pickle=True)
#print(File)

#print(File['T_Air_8'][2])

#for element in File['T_Air_8']
#
#import pickle
#import csv
#
## Load the data from the pickle file
#with open(myfile, 'rb') as f:
#    data = pickle.load(f)
#import pickle
#
## Access NumPy array in dictionary
#Temp = data['T_Air_8']
#Q_Dem = data['Q_Hou_Dem_8']
#P_PV = data['P_PV_8']
#P_EL_Dem = data['P_EL_Dem_8']
#
#for i in range(0,8):
#    Temp_i = []
#    Temp_i.append(Temp)
#    Q_Hou_i = []
#    Wasser = []
#    Zwei =[]
#    Drei =[]
#    Vier =[]
#    #print(Test)
#    with open("input_data/Medoid/TWW/outcome_"+ str(i+1)+ ".csv", 'r') as file:
#        reader = csv.reader(file)
#
#        for row in reader:
#            first = float(row[0])
#            second = float(row[1])
#            third = float(row[2])
#            fourth = float(row[3])
#            Wasser.append(first)
#            Zwei.append(second)
#            Drei.append(third)
#            Vier.append(fourth)
#
#    Test = list(zip(Temp[i], Q_Dem[i], P_PV[i], P_EL_Dem[i], Wasser, Zwei, Drei, Vier))
#
#    with open(f"DreiClusterTage_warm_" + str(i) + ".csv", "w", newline="") as f:
#        writer = csv.writer(f)
#
#        for j in range(0,3):
#            for values in Test:
#                writer.writerow(values)
#
#
#print(Temp_i)

#print(Wasser)

# Write the data for each day to a separate CSV file
#for day, values in data.items():
#    # Create a filename for the CSV file based on the date
#    filename = f'{day}.csv'
#    # Create a list of tuples containing the temperature and rain data for each hour of the day
#    hourly_data = list(zip(values['T_Air_8'], values['Q_Hou_Dem_8']))
#    # Write the data to a CSV file
#    with open(filename, 'w', newline='') as f:
#        writer = csv.writer(f)
#        # Write the header row
#        writer.writerow(['hour', 'temperature', 'rain'])
#        # Write each hour's data to a row in the CSV file
#        for hour, (temperature, rain) in enumerate(hourly_data):
#            writer.writerow([hour, temperature, rain])


#print(File)

#x_Opti = np.loadtxt("Data_48_1_32_4_24.csv")
#data = []
#with open ("Data_48_1_32_4_24.csv") as file:
#    reader = csv.reader(file, delimiter=",")
#    for row in reader:
#        row_values = [float(val) for val in row]
#        data.append(row_values)

#print(data)

#print(File.mapping10)


#with open("input_data/Medoid/TWW/outcome_1.csv", 'r') as file:
#    reader =csv.reader(file)
#    first = [float(row[0]) for row in reader]
#print(first)


#with open("input_data/ClusteredYear/ALT_ClusteredYear_cold.csv", 'r') as file:
#    reader = csv.reader(file)
#    T_Air = [float(row[0]) for row in reader]
#    Q_Hou_Dem = [float(row[1]) for row in reader]
#    P_PV = [float(row[2]) for row in reader]
#    P_EL_Dem = [float(row[3]) for row in reader]

#File = pd.read_csv('D://lma-mma/Repos/MA_MM/ClusteredYear_warm.csv')
#T_Air = File.iloc[:,0]
#Q_Hou_Dem = File.iloc[:, 1]
#P_PV = File.iloc[:, 2]
#P_EL_Dem = File.iloc[:, 3]
#
#print(T_Air)
#print(Q_Hou_Dem)
#print(P_PV)
#print(P_EL_Dem)
#
#Testlist = []
#with open("input_data/Medoid/TWW/outcome_6.csv", 'r') as file:
#    reader = csv.reader(file)
#    for i, row in enumerate(reader):
#        if i < 24:
##        print(row)
#            first = float(row[0])
#            Testlist.append(first)
#
#        print(first)
#       # print(second)
#print(first)


#
#Data = pd.read_csv('D:/lma-mma/Repos/MA_MM/input_data/Sim_Input/InputYear_cold.csv')
#
#
#T_Air = Data.iloc[:, 0]
#print(T_Air)

#Pfad = 'D:/lma-mma/Repos/MA_MM/Results/Optimierung/Puffer/'
#ResultPath = 'D:/lma-mma/Repos/MA_MM/Results/DecisionTrees/'
#File_Stem = '0_025_8760_4_24_Clusteryear_cold_Var_Puffer_Small'
#File_Stem_Test = '0_025_8760_4_24_Clusteryear_normal_Var_Puffer_Small'
#y_Opti = np.loadtxt(Pfad + "Modes_"+ File_Stem + ".csv", skiprows=0)
#
#print(len(y_Opti))
#


#dT = pd.read_csv('input_data/Opti_Input/Temperature_Berlin.csv', skiprows=0)
##T_Air = (dT.iloc[:, 2] + 273.15)
#T = (dT.iloc[:, 2] + 273.15)
#dQ = pd.read_csv('input_data/Opti_Input/Q_Dem/Q_Heat_Dem_warm.csv')
#dQ = dQ.iloc[: , 1:]
#Q_Hou_Dem    = dQ.sum(axis=1)
#
#
#P_PV_list = pd.read_csv('input_data/Opti_Input/P_PV/P_PV_TRY_warm.csv')
#P_PV_list = P_PV_list.values.tolist()
#P_PV = [item for sublist in P_PV_list for item in sublist]
##
#P_EL_Dem = np.loadtxt('input_data/Opti_Input/ELHour.txt')
#
#TWW = pd.read_csv('input_data/ClusteredYear/ClusteredYear_warm.csv')
#
#xp = np.arange(0.0, 8784, 1.0)
#xnew = np.arange(0.0, 8784, 0.25)
##T = Temp[0].tolist()
#T_Air = np.interp(xnew, xp, T) #Liste1)
#
#
#
#QTWW = TWW.iloc[:,4]
#fTWW = TWW.iloc[:,7]
#TpTWW =TWW.iloc[:,5]
#for i in range(len(TpTWW)):
#    if TpTWW[i] == 0:
#        TpTWW[i] = 10
#
#dW = pd.read_csv('input_data/Opti_Input/Wind_Speed_Berlin.csv', skiprows=0)
#Win_Speed= dW.iloc[:, 2]
#
#dH = pd.read_csv('input_data/Opti_Input/Global_Radiation_Berlin.csv', skiprows=0)
#HGloHor= dH.iloc[:, 2]
#
#list(zip(T_Air, Q_Hou_Dem, P_PV, P_EL_Dem, QTWW, TpTWW, fTWW, Win_Speed, HGloHor))
#
#with open(f"InputYear_warm.csv", "w", newline="") as f:
#    writer = csv.writer(f)
#    for values in zip(T_Air, Q_Hou_Dem, P_PV, P_EL_Dem, QTWW, TpTWW, fTWW, Win_Speed, HGloHor):
#        writer.writerow(values)


from sklearn import tree
import graphviz
import numpy as np
import csv
import pandas as pd
from sklearn import tree
#import sklearn
#import matplotlib.pyplot as plt
#import matplotlib as mpl
#from plot_results_to_files import latex_base
#from sklearn.model_selection import train_test_split
#from sklearn.metrics import accuracy_score
#from sklearn.model_selection import GridSearchCV
#from sklearn.metrics import confusion_matrix
#from sklearn.metrics import plot_confusion_matrix
#from sklearn.metrics import ConfusionMatrixDisplay
#from plot_results_to_files import latex_twothird
#import tikzplotlib
#
#plt.rcParams.update(latex_base)
#
#import numpy as np
#import matplotlib.pyplot as plt
#from sklearn.pipeline import Pipeline
#from sklearn.preprocessing import PolynomialFeatures
#from sklearn.linear_model import LinearRegression
#from sklearn.model_selection import cross_val_score
#
#
#def true_fun(X):
#    return np.cos(1.5 * np.pi * X)
#
#
#np.random.seed(0)
#
#n_samples = 30
#degrees = [1, 4, 15]
#
#X = np.sort(np.random.rand(n_samples))
#y = true_fun(X) + np.random.randn(n_samples) * 0.1
#
#plt.figure(figsize=(14, 6))
#for i in range(len(degrees)):
#    ax = plt.subplot(1, len(degrees), i + 1)
#    plt.setp(ax, xticks=(), yticks=())
#
#    polynomial_features = PolynomialFeatures(degree=degrees[i], include_bias=False)
#    linear_regression = LinearRegression()
#    pipeline = Pipeline(
#        [
#            ("polynomial_features", polynomial_features),
#            ("linear_regression", linear_regression),
#        ]
#    )
#    pipeline.fit(X[:, np.newaxis], y)
#
#    # Evaluate the models using crossvalidation
#    scores = cross_val_score(
#        pipeline, X[:, np.newaxis], y, scoring="neg_mean_squared_error", cv=10
#    )
#
#    X_test = np.linspace(0, 1, 100)
#    plt.plot(X_test, pipeline.predict(X_test[:, np.newaxis]), label="Modell")
#    plt.plot(X_test, true_fun(X_test), label="Reale Funktion")
#    plt.scatter(X, y, color='#F49961',s=20, label="Samples")
#    plt.xlabel("x")
#    plt.ylabel("y")
#    plt.xlim((0, 1))
#    plt.ylim((-2, 2))
#    plt.legend(loc="best")
#    if degrees[i] == 1:
#        plt.title("Underfitting")#\nMSE = {:.2e}(+/- {:.2e})".format(-scores.mean(), scores.std()))
#    elif degrees[i] == 4:
#        plt.title("Optimal")#\nMSE = {:.2e}(+/- {:.2e})".format(-scores.mean(), scores.std()))
#    else:
#        plt.title("Overfitting")#.format(-scores.mean(), scores.std()))
#
#plt.savefig('Overfitting.pdf')
#tikzplotlib.save('Overfitting')outcom

#plt.savefig('Overfitting.svg')
#plt.show()

##################### Ende #################

#File_Stem = '0_025_8760_4_24_Clusteryear_warm_Fix_TWW_Small_Norm'
#fn = ('T_Air', 'Q_Hou_Dem', 'P_PV', 'P_EL_Dem', 'T_Mean', 'c_grid' ,'Q_TWW')
##so wird Data TRY gespeichert:    T_Air, Q_Hou, P_PV, P_EL_Dem, T_Mean, c_grid, Q_TWW, T_Sto, T_TWW, COP_1, COP_2
##so wird Data Clusteryear gespeichert: T_Reihe, Q_Reihe, PV_Reihe, PEL_Reihe, TM_Reihe, Cel_Reihe, QTWW_Reihe
#cn = ('Modus 0', 'Modus 1', 'Modus 2', 'Modus 3')
#Pfad = 'D:/lma-mma/Repos/MA_MM/Results/Optimierung/TWW/'



# Import Feature Data
#data = []
#with open (Pfad + "Data_" + File_Stem + '.csv') as file:
#    reader = csv.reader(file, delimiter=",")
#    for i, row in enumerate(reader):
#        row_values = [float(val) for val in row]
#        filtered = [row[0]] + [str(float(row[i]) * 4) for i in range(1, 4)]+ [row[5]] + [str(float(row[6]) * 4)]
#        data.append(filtered)

#print(data[0])


##############################################
TRY = 'cold'

header = ['Tair','QHouDem','PPV','PELDem','QTWW','Tp','Tmin','f']
myfile = "D://lma-mma/Repos/MA_MM/Cluster/Cluster_Alle_8_8_1_3421_001_"+TRY+".pkl"
## Load the data from the pickle file
with open(myfile, 'rb') as f:
    data = pickle.load(f)
#import pickle

## Access NumPy array in dictionary
xp = np.arange(0.0, 24, 1.0)
xnew = np.arange(0.0, 24, 0.25)

Temp = data['T_Air_8']
Q_Dem = data['Q_Hou_Dem_8']

print(Temp)

T = Temp[0].tolist()
#T_Input = np.interp(xnew, xp, T) #Liste1)


P_PV = data['P_PV_8']
P_EL_Dem = data['P_EL_Dem_8']

Endliste = []
#Endliste.append(Q_Dem)
#print(len(Q_Dem))

#print(len(Endliste[0]))


for i in range(0,8):

    Wasser = []
    Zwei =[]
    Drei =[]
    Vier =[]
    #print(Test)
    with open("input_data/Medoid/TWW/"+TRY+"/outcome_"+ str(i+1)+ ".csv", 'r') as file:
        reader = csv.reader(file)

        for row in reader:
            first = float(row[0])
            second = float(row[1])
            third = float(row[2])
            fourth = float(row[3])
            Wasser.append(first)
            Zwei.append(second)
            Drei.append(third)
            Vier.append(fourth)

    Liste1 = Temp[i].tolist()
    T_Input = np.interp(xnew, xp, Liste1)

    Liste2 = Q_Dem[i].tolist()
    Q_Hou = np.interp(xnew, xp, Liste2)

    Liste3 = P_PV[i].tolist()
    PV = np.interp(xnew, xp, Liste3)

    Liste4 = P_EL_Dem[i].tolist()
    PEL = np.interp(xnew, xp, Liste4)

    Test = list(zip(T_Input, Q_Hou, PV, PEL, Wasser, Zwei, Drei, Vier))
#    Test = list(zip(T_Input, Q_Dem[i], P_PV[i], P_EL_Dem[i], Wasser, Zwei, Drei, Vier))
#    print(Test)

    #print(T_Input)
    with open(f"DreiClusterTage_"+TRY+"_" + str(i) + ".csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([g for g in header])
        for j in range(0,3):
            for values in Test:
                writer.writerow(values)
#