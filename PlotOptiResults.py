import fmpy as fmpy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from plot_results_to_files import latex_fullpage
from plot_results_to_files import latex_base

plt.rcParams.update(latex_fullpage)
filename_start = '0_025_48_4_24_Clusterday_'
filename_rest = '_cold_Fix_TWW_Small_Norm.csv'
Data = 'Data_'
Mode = 'Modes_'
Direct = 'D://lma-mma/Repos/MA_MM/Results/Optimierung/TWW/Clusterday/'
Savedirect = 'D://lma-mma/Repos/MA_MM/Datensicherung/Clusteropti/'

df = []
mf =[]
q_hp_1 = []
q_hp_2 = []
q_hp_3 = []
q_hp_4 = []
q_hp_5 = []
q_hp_6 = []
q_hp_7 = []
q_hp_8 = []
m_1 = []
m_2 = []
m_3 = []
m_4 = []
m_5 = []
m_6 = []
m_7 = []
m_8 = []


for i in range(0,8,1):
    df = []
    df = pd.read_csv(Direct+Data+filename_start+str(i)+filename_rest, header=None, names=['T_Air', 'Q_Hou', 'P_PV', 'P_EL_Dem', 'T_Mean', 'c_grid', 'Q_TWW', 'T_Sto', 'T_TWW', 'COP_1', 'COP_2', 'Q_HP',  'Q_Penalty'])
    mf = pd.read_csv(Direct+Mode+filename_start+str(i)+filename_rest, header=None, names=['Modes'])
    if i == 0:
        q_hp_1.append(df['Q_HP'])
        m_1.append(mf['Modes'])
    elif i == 1:
        q_hp_2.append(df['Q_HP'])
        m_2.append(mf['Modes'])
    elif i == 2:
        q_hp_3.append(df['Q_HP'])
        m_3.append(mf['Modes'])
    elif i == 3:
        q_hp_4.append(df['Q_HP'])
        m_4.append(mf['Modes'])
    elif i == 4:
        q_hp_5.append(df['Q_HP'])
        m_5.append(mf['Modes'])
    elif i == 5:
        q_hp_6.append(df['Q_HP'])
        m_6.append(mf['Modes'])
    elif i == 6:
        q_hp_7.append(df['Q_HP'])
        m_7.append(mf['Modes'])
    elif i == 7:
        q_hp_8.append(df['Q_HP'])
        m_8.append(mf['Modes'])

print('Lönge')
print(len(m_8))
Time = np.arange(0,24,0.25)


print(q_hp_1)
print(m_1)
fig, ax = plt.subplots(4, 2)

ax[0,0].plot(np.array(Time), q_hp_1[0][96:192]*4)
ax2 = ax[0,0].twinx()
ax2.plot(np.array(Time), m_1[0][96:192], color='#4B81C4')
# Set the x-label and y-label
#    SimTime = np.arange(1)
plt.xlabel('SimTime')
ax[0,0].set_xlabel('Clustertag 1')
ax[0,0].set_ylabel('Q_HP')
# Show the plot

#ax[0,1].plot(np.array(SimTime)/3600, mDHW_flow_in[0:len(TBufStoBot)])
ax[0, 1].plot(np.array(Time), q_hp_2[0][96:192]*4)
ax2 = ax[0,1].twinx()
ax2.plot(np.array(Time), m_2[0][96:192], color='#4B81C4')
# Set the x-label and y-label
#    SimTime = np.arange(1)
plt.xlabel('SimTime')
ax[0,1].set_xlabel('Clustertag 2')
#plt.ylabel('m_flow_Cons')
#    plt.savefig('D:/lma-mma/Repos/MA_MM/Datensicherung/Test/1')
# Show the plot
#    plt.show()

#    fig, ax = plt.subplots(1, 2, figsize=(6.5, 2.9))
ax[1,0].plot(np.array(Time), q_hp_3[0][96:192]*4)
# Set the x-label and y-label
#    SimTime = np.arange(1)
#    plt.xlabel('SimTime')
ax[1,0].set_xlabel('Clustertag 3')
ax2 = ax[1,0].twinx()
ax2.plot(np.array(Time), m_3[0][96:192], color='#4B81C4')
#ax[1,0].set_ylabel('TDHWTop')
ax[1,0].set_ylabel('Q_HP')
# Show the plot

ax[1,1].plot(np.array(Time), q_hp_4[0][96:192]*4)
# Set the x-label and y-label
#    SimTime = np.arange(1)
#    plt.xlabel('SimTime')
ax[1,1].set_xlabel('Clustertag 4')
ax2 = ax[1,1].twinx()
ax2.plot(np.array(Time), m_4[0][96:192], color='#4B81C4')
#ax[1,1].set_ylabel('TDHWBot')
#ax[1,1].set_ylabel('Q_HP')
# Show the plot
#    plt.savefig('D:/lma-mma/Repos/MA_MM/Datensicherung/Test/2')
#    plt.show()

#    fig, ax = plt.subplots(1, 2, figsize=(6.5, 2.9))
ax[2,0].plot(np.array(Time), q_hp_5[0][96:192]*4)
# Set the x-label and y-label
#    SimTime = np.arange(1)
#    ax[3,0].set_xlabel('SimTime')
ax[2,0].set_xlabel('Clustertag 5')
ax2 = ax[2,0].twinx()
ax2.plot(np.array(Time), m_5[0][96:192], color='#4B81C4')
#ax[2,0].set_ylabel('TStoTop')
ax[2,0].set_ylabel('Q_HP')
# Show the plot

ax[2,1].plot(np.array(Time), q_hp_6[0][96:192]*4)
# Set the x-label and y-label
#    SimTime = np.arange(1)
#    plt.xlabel('SimTime')
ax[2,1].set_xlabel('Clustertag 6')
ax2 = ax[2,1].twinx()
ax2.plot(np.array(Time), m_6[0][96:192], color='#4B81C4')
#ax[2,1].set_ylabel('TStoBot')
# Show the plot

ax[3,0].plot(np.array(Time), q_hp_7[0][96:192]*4)
# Set the x-label and y-label
#    SimTime = np.arange(1)
ax[3,0].set_xlabel('Clustertag 7')
ax2 = ax[3,0].twinx()
ax2.plot(np.array(Time), m_7[0][96:192], color='#4B81C4')
ax[3,0].set_ylabel('Q_HP')



ax[3,1].plot(np.array(Time), q_hp_7[0][96:192]*4)
# Set the x-label and y-label
#    SimTime = np.arange(1)
#ax[3,1].set_xlabel('Clustertag 8')
plt.xlabel('Time in h')
ax[3,1].set_xlabel('Clustertag 8')
#ax2 = ax[3,1].twinx()
ax2.plot(np.array(Time), m_8[0][96:192], color='#4B81C4')
ax[3,1].set_ylabel('Q_HP')

plt.savefig(Savedirect+'Cold_Alle.pdf')
plt.show()
#labels = ['Q_HP', 'Modus']

plt.rcParams.update(latex_base)
fig, ax = plt.subplots()
ax.plot(np.array(Time), q_hp_1[0][96:192]*4, label = 'Q_HP')
ax.set_xlabel('Time in h')
#plt.xlabel('Clustertag 8')
ax2 = ax.twinx()
ax2.plot(np.array(Time), m_1[0][96:192], color='#4B81C4', label = 'Modus' )
ax2.set_yticks([0,1,2,3])
handles, labels =[],[]
for ax in [ax, ax2]:
    for h, l in zip(*ax.get_legend_handles_labels()):
        handles.append(h)
        labels.append(l)
plt.legend(handles, labels)
plt.savefig(Savedirect+'Cold_C1.pdf')
plt.show()

fig, ax = plt.subplots()
ax.plot(np.array(Time), q_hp_2[0][96:192]*4, label = 'Q_HP')
ax.set_xlabel('Time in h')
ax.set_ylabel('Q_HP in W')
ax2 = plt.twinx()
ax2.plot(np.array(Time), m_2[0][96:192], color='#4B81C4', label = 'Modus')
ax2.set_yticks([0,1,2,3])
handles, labels =[],[]
for ax in [ax, ax2]:
    for h, l in zip(*ax.get_legend_handles_labels()):
        handles.append(h)
        labels.append(l)
plt.legend(handles, labels)
plt.savefig(Savedirect+'Cold_C2.pdf')
plt.show()

fig, ax = plt.subplots()
ax.plot(np.array(Time), q_hp_3[0][96:192]*4, label = 'Q_HP')
ax.set_xlabel('Time in h')
ax.set_ylabel('Q_HP in W')
ax2 = ax.twinx()
ax2.plot(np.array(Time), m_3[0][96:192], color='#4B81C4', label = 'Modus')
ax2.set_yticks([0,1,2,3])
handles, labels =[],[]
for ax in [ax, ax2]:
    for h, l in zip(*ax.get_legend_handles_labels()):
        handles.append(h)
        labels.append(l)
plt.legend(handles, labels)

plt.savefig(Savedirect+'Cold_C3.pdf')
plt.show()

fig, ax = plt.subplots()
ax.plot(np.array(Time), q_hp_4[0][96:192]*4, label = 'Q_HP')
ax.set_xlabel('Time in h')
ax.set_ylabel('Q_HP in W')
ax2 = plt.twinx()
ax2.plot(np.array(Time), m_4[0][96:192], color='#4B81C4', label = 'Modus')
ax2.set_yticks([0,1,2,3])
handles, labels =[],[]
for ax in [ax, ax2]:
    for h, l in zip(*ax.get_legend_handles_labels()):
        handles.append(h)
        labels.append(l)
plt.legend(handles, labels)
plt.savefig(Savedirect+'Cold_C4.pdf')
plt.show()

fig, ax = plt.subplots()
ax.plot(np.array(Time), q_hp_5[0][96:192]*4, label = 'Q_HP')
ax.set_xlabel('Time in h')
ax.set_ylabel('Q_HP in W')
ax2 = plt.twinx()
ax2.plot(np.array(Time), m_5[0][96:192], color='#4B81C4', label = 'Modus')
ax2.set_yticks([0,1,2,3])
handles, labels =[],[]
for ax in [ax, ax2]:
    for h, l in zip(*ax.get_legend_handles_labels()):
        handles.append(h)
        labels.append(l)
plt.legend(handles, labels)
plt.savefig(Savedirect+'Cold_C5.pdf')
plt.show()

fig, ax = plt.subplots()
ax.plot(np.array(Time), q_hp_6[0][96:192]*4, label = 'Q_HP')
ax.set_xlabel('Time in h')
ax.set_ylabel('Q_HP in W')
ax2 = plt.twinx()
ax2.plot(np.array(Time), m_6[0][96:192], color='#4B81C4', label = 'Modus')
ax2.set_yticks([0,1,2,3])
handles, labels =[],[]
for ax in [ax, ax2]:
    for h, l in zip(*ax.get_legend_handles_labels()):
        handles.append(h)
        labels.append(l)
plt.legend(handles, labels)
plt.savefig(Savedirect+'Cold_C6.pdf')
plt.show()

fig, ax = plt.subplots()
ax.plot(np.array(Time), q_hp_7[0][96:192]*4, label = 'Q_HP')
ax.set_xlabel('Time in h')
ax.set_ylabel('Q_HP in W')
#plt.xlabel('Clustertag 8')
ax2 = plt.twinx()
ax2.plot(np.array(Time), m_7[0][96:192], color='#4B81C4', label = 'Modus')
ax2.set_yticks([0,1,2,3])
handles, labels =[],[]
for ax in [ax, ax2]:
    for h, l in zip(*ax.get_legend_handles_labels()):
        handles.append(h)
        labels.append(l)
plt.legend(handles, labels)
plt.savefig(Savedirect+'Cold_C7.pdf')
plt.show()

fig, ax = plt.subplots()
ax.plot(np.array(Time), q_hp_8[0][96:192]*4, label='Q_HP')
ax.set_xlabel('Time in h')
ax.set_ylabel('Q_HP in W')
ax2 = ax.twinx()
ax2.set_ylabel('Modus')
ax2.set_yticks([0,1,2,3])
ax2.plot(np.array(Time), m_8[0][96:192], color='#4B81C4', label='Modus')
handles, labels =[],[]
for ax in [ax, ax2]:
    for h, l in zip(*ax.get_legend_handles_labels()):
        handles.append(h)
        labels.append(l)
plt.legend(handles, labels)
plt.savefig(Savedirect+'Cold_C8.pdf')
plt.show()


