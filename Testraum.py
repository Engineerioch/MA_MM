import numpy as np
import math
import pandas as pd
import csv
import os

#Q_Dem_kalt = (np.array(csvColumn2list('D:/lma-mma/MA_MM_Python/input_data/Q_Dem/Q_Heat_Dem_kalt.csv')))
#for i in Q_Dem_kalt:
 #   (Q_Dem_kalt[i])
#Q_Dem = math.fsum(Q_Dem_kalt)


##csv_array = []
##with open('D:/lma-mma/MA_MM_Python/input_data/Q_Dem/Q_Heat_Dem_warm.csv', 'r') as csv_file:
  ##  reader = csv.reader(csv_file)
    # remove headers
#    reader.next()
    # loop over rows in the file, append them to your array. each row is already formatted as a list.
  ##  for row in reader:
   ##     csv_array.append(row)

#dQ = pd.read_csv("D:/lma-mma/MA_MM_Python/input_data/Q_Dem/Q_Heat_Dem_normal.csv")
#dQ = dQ.iloc[:, 1:]
#dQ = dQ.sum(axis=1)
#print(dQ,)
""""
def get_solar_radiation_forecast(prediction_horizon, time_step, year, hour_of_year):
    file = open(os.path.join("input_data", "Global_Radiation_Berlin.csv"), "rb") # radiation in Wh/m²
    if year == "normal":
        data = np.loadtxt(file, delimiter=",", skiprows=1+hour_of_year, usecols=(1), unpack=True, max_rows=prediction_horizon+1)
    elif year == "warm":
        data = np.loadtxt(file, delimiter=",", skiprows=1+hour_of_year, usecols=(2), unpack=True, max_rows=prediction_horizon+1)
    elif year == "kalt":
        data = np.loadtxt(file, delimiter=",", skiprows=1+hour_of_year, usecols=(3), unpack=True, max_rows=prediction_horizon+1)
    if time_step == 1.0:
        sol_rad = data.tolist()
        sol_rad.pop()

"""""""""
##df = pd.read_csv('input_data/P_PV_TRY_cold.csv')
##df = df.values.tolist()
##print((df))

##P_PV_list = pd.read_csv('input_data/P_PV_TRY_warm.csv')
#        P_PV_list = np.loadtxt('D:/lma-mma/MA_MM_Python/input_data/P_PV_TRY_warm.txt')

#ELHour =open('D:/lma-mma/MA_MM_Python/input_data/ELSumProfiles_Hour.txt', 'r')
#ELQuarter=open('D:/lma-mma/MA_MM_Python/input_data/ELSumProfiles_Quarter.txt', 'r')
#Q_Heat_Dem_kalt=open('D:/lma-mma/MA_MM_Python/input_data/Q_Dem/Q_Heat_Dem_kalt.csv', 'r')
#print(Q_Heat_Dem_kalt.read())



#Q_Heat_Dem_kalt_Data=open('D:/lma-mma/MA_MM_Python/input_data/Q_Dem/Q_Heat_Dem_kalt.csv', 'r')

#Q_Heat_Dem_kalt_List = []
#for i in Q_Heat_Dem_kalt_Data:
#    Q_Heat_Dem_kalt_List.append(i)
#del Q_Heat_Dem_kalt_List[0]
#Q_Heat_Dem_kalt_Data.close()
#print('Hallo Welt')
#print(len(Q_Heat_Dem_kalt_List))


#print(Q_Heat_Dem_kalt_List[0])
#P_PV = pd.read_csv('input_data/Temperature_Berlin.csv', skiprows=0)
#L = np.zeros([35 + 1])
#for t in range(35 + 1):
#   L[t] = P_PV[t]


#print(dTCold)


dH = pd.read_csv('input_data/P_PV_TRY_cold.csv')
P_PV_list = dH.values.tolist()
dH = [item for sublist in P_PV_list for item in sublist]
#print(dH[0:10])
for i in range(0, 10):
    print(dH[i])
print(dH[10])