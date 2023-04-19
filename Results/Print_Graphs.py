import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()

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

#### Tell which Dataa you want to plot on the first (left) y-Axis: ###
YAchse1 = 'Mode'


#### Tell which Dataa you want to plot on the first (left) y-Axis: ###
YAchse2 = 'COP_1'
YAchse3= 'COP_2'

# Extract time-step and Q_HP data
#time_step = range(0, len(df.iloc[1, 0]))
YValues1 = []
YValues2 = []
YValues3 = []

YValues1 = df.iloc[0,:].values
YValues2 = df.iloc[1,:].values
YValues3 = df.iloc[20,:].values
## Don't change this. This will add the Name of the Data and delete it from the list to plot the values###
## It also defines the lenght of the plot ##
yachse1 = YValues1[0]
YValues1 = np.delete(YValues1, 0)
yachse2 = YValues2[0]
YValues2 = np.delete(YValues2, 0)
YValues3 = np.delete(YValues3, 0)
XValues = range(len(YValues1)) #[0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15, 15.5, 16, 16.5, 17, 17.5, 18, 18.5, 19, 19.5, 20, 20.5, 21, 21.5, 22, 22.5, 23, 23.5, 24, 24.5]
time_step = XValues


# Create a line graph of Q_HP vs time-step

#plt.yticks(np.arange(290, 310, step=2))

ax2 = ax.twinx()
ax.plot(time_step, YValues1, color='r')

#ax2.plot(time_step,YValues3, color='g', label='COP_1')
ax2.plot(time_step, YValues2 , color='b', label='Q_HP')

plt.xlabel('Time-step')
ax.set_ylabel(yachse1, color='r')
ax2.set_ylabel('Q_HP in W')


ax2.set_ylim(bottom=0, top=10500)
ax.set_ylim(bottom=0, top=3.15)
plt.title('HP-Modes mit TWW. Speicher klein ')
plt.legend(loc='upper left')
plt.tight_layout()
plt.show()
