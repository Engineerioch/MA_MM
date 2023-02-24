import matplotlib.pyplot as plt
import numpy as np

#fig, ax = plt.subplots()

# Werte für Tabelle erstellen
#table_data = [
#    ["Mode", save_results['Mode']],
#    ["Player 2", save_results['Q_HP']],
    #  ["Player 3", 33],
    #  ["Player 4", 25],
    #  ["Player 5", 12]
#]

# Tabelle erstellen
#table = ax.table(cellText=table_data, loc='center')
#plt.show()


import pandas as pd
import matplotlib.pyplot as plt

# Read CSV file and store data in a Pandas DataFrame
df = pd.read_csv('Real_Results/results.csv', delimiter=',')
YAchse = 'Mode'

#print(df['Q_HP'])
# Extract time-step and Q_HP data
#time_step = range(0, len(df.iloc[1, 0]))
YValues =[]
YValues = df.iloc[0,:].values
#print(YValues[1])
yachse = YValues[0]
YValues = np.delete(YValues, 0)
#print(Q_HP)
XValues = range(0, len(YValues),1)
time_step = XValues
#print (Q_HP[6])
# Create a line graph of Q_HP vs time-step
plt.plot(time_step, YValues)
plt.xlabel('Time-step')
plt.ylabel(yachse)
plt.title('HP-Modes in Kalt TRY mit TWW')
plt.show()