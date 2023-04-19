import random
import csv
import numpy as np
import pickle
import pandas as pd



TRY = 'warm'

######################################## Trinkwarmwasser Randomizieren #################################################
## Dies muss zuerst gemacht werden. Der nächste teil muss dazu auskommentiert werden ###################################
## Danach Clustering machen ############################################################################################

# Sample data
#list1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,   0.105,1.4,0.105,0.105, 3.605,0.105,0.105,0.105,    0.105,0,0.105,0,    0,0,0.105,0,   0,0,0.105,0.105,    0,0,0,0.315,   0,0,0,0,    0,0,0.105,0,    0,0,0.105,0,  0,0,0.105,0,    0,0,0,0,     0.105,0.105,0.105,0,   0.105,0,0,0,    0,0,0.735,0,   3.605,0,0.105,0,    0,0,0,0, 0,0,0,0]
#list3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,   25,40,25,25,           10,25,25,25,                25,0,25,0,          0,0,10,0,      0,0,25,25,          0,0,0,10,      0,0,0,0,    0,0,25,0,       0,0,25,0,     0,0,25,0,       0,0,0,0,     25,40,40,0,            25,0,0,0,       0,0,10,0,      10, 0, 25,0,        0,0,0,0, 0,0,0,0]
#list2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,   25,40,25,25,           40,25,25,25,                25,0,25,0,          0,0,40,0,      0,0,25,25,          0,0,0,55,      0,0,0,0,    0,0,25,0,       0,0,25,0,     0,0,25,0,       0,0,0,0,     25,40,40,0,            25,0,0,0,       0,0,55,0,      40,0,10,0,          0,0,0,0, 0,0,0,0]
#list4 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,   0.2,2.67,0.2,0.2,      6.87,0.2,0.2,0.2,         0.2,0,0.2,0,           0,0,0.2,0,    0,0,0.2,0.2,        0,0,0,3,       0,0,0,0,    0,0,0.2,0,        0,0,0.2,0,      0,0,0.2,0,        0,0,0,0,     0.2,0.13,0.13,0, 0.2,0,0,0,        0,0,0.93,0,       6.87,0,0.2,0,  0,0,0,0, 0,0,0,0]
#
##list2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,40,40,25,40,25,55,0,25,25,25,0,40,25,55,40,0,0]Tp
##list3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,40,10,25,10,25,10,0,25,25,25,0,40,25,10,10,0,0]Tm
#
#print(sum(list1))
#print(len(list2))
#print(len(list3))
#print(len(list4))
#
##Create a list of tuples where each tuple contains the corresponding elements from each list
#original_data = list(zip(list1, list2, list3, list4))
#
##Keep the first 6 elements of each list fixed and shuffle the rest of the elements
#fixed_data = list(zip(list1[:24], list2[:24], list3[:24], list4[:24]))
#remaining_data = list(zip(list1[24:], list2[24:], list3[24:], list4[24:]))
#
#
## Create 8 different outcomes
#for i in range(8):
#    # Shuffle the remaining elements
#    random.shuffle(remaining_data)
#
#    # Combine the fixed and shuffled data to create the new data
#    new_data = fixed_data + remaining_data
#
#    with open(f"input_data/Medoid/TWW/"+TRY+f"/outcome_{i + 1}.csv", "w", newline="") as f:
#        writer = csv.writer(f)
#        writer.writerows(new_data)


###################################### DreiClusterTage Erstellen #######################################################
### Dies muss nach dem Clustern gemacht werden #########################################################################
####################### Unbedingt den ersten Teil aus dieser Datei auskommentieren!!! ##################################


myfile= "D://lma-mma/Repos/MA_MM/Cluster/Cluster_Alle_8_8_1_3421_001_"+TRY+".pkl"

objects = pd.read_pickle(myfile)
clustered = np.load(myfile, allow_pickle=True)




## Load the data from the pickle file
with open(myfile, 'rb') as f:
   data = pickle.load(f)



## Access NumPy array in dictionary
Temp = data['T_Air_8']
Q_Dem = data['Q_Hou_Dem_8']
P_PV = data['P_PV_8']
P_EL_Dem = data['P_EL_Dem_8']
xp = np.arange(0.0, 24, 1.0)
xnew = np.arange(0.0, 24, 0.25)

for i in range(0,8):

    T_Air   = np.interp(xnew, xp, Temp[i])
    Q_Hou   = np.interp(xnew, xp, Q_Dem[i])
    PPV     = np.interp(xnew, xp, P_PV[i])
    PEL = np.interp(xnew, xp, P_EL_Dem[i])
    Wasser = []
    Zwei =[]
    Drei =[]
    Vier =[]

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
#
    Test = list(zip(T_Air, Q_Hou, PPV, PEL, Wasser, Zwei, Drei, Vier))
    header = 'Tair','QHouDem','PPV','PELDem','QTWW','Tp','Tmin','f'
    with open(f"input_data/ClusteredDay/"+TRY+"/DreiClusterTage_"+TRY+"_" + str(i) + ".csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([g for g in header])

        for j in range(0,3):
            for values in Test:
                writer.writerow(values)

#c_grid = []
#for i in range(0,8760):
#    c_grid.append(clustered_c_grid[i])
#print(type(clustered_c_grid))
#xp = np.arange(0.0, 8760, 1.0)
#xnew = np.arange(0.0, 8760, 0.25)
#T = clustered_T_Air.tolist()
#
#T_Air = np.interp(xnew, xp, clustered_T_Air) #Liste1)
#Q_Hou= np.interp(xnew, xp, clustered_Q_Hou_Dem)
#PPV= np.interp(xnew, xp, clustered_P_PV)
#PEL= np.interp(xnew, xp, clustered_P_EL_Dem)
#print(len(c_grid))
#c =  np.interp(xnew, xp, c_grid)