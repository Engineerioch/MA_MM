import fmpy as fmpy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tikzplotlib

from plot_results_to_files import latex_fullpage
from plot_results_to_files import latex_base
from plot_results_to_files import pp_figure
from rwth_colors import plot_colors
from rwth_colors import colors

############### In this file the Simulation results are plotted ###################
# First set the TRY and the month 'Januar' or 'Juli'
plt.rcParams.update(pp_figure)
TRY = 'warm_'
Monat = 'Juli'
if Monat == 'Januar':
    start_time= 312
    stop_time= 504
elif Monat == 'Juli':
    start_time = 4008
    stop_time = 4200


Data = 'Data_'

Direct = 'D://lma-mma/Repos/MA_MM/Results/Sim/'
Savedirect = 'D://lma-mma/Repos/MA_MM/Datensicherung/Presi/'
df = []
q_hou = []


q_hp_GB = []
q_hp_DB = []
q_hp_TRY = []
q_hp_CY = []

m_GB  = []
m_DB  = []
m_TRY = []
m_CY  = []

StoTop_GB  =[]
StoTop_DB  =[]
StoTop_TRY =[]
StoTop_CY  =[]
StoBot_GB  =[]
StoBot_DB  =[]
StoBot_TRY =[]
StoBot_CY  =[]

TWWTop_GB  = []
TWWTop_DB  = []
TWWTop_TRY = []
TWWTop_CY  = []
TWWBot_GB  = []
TWWBot_DB  = []
TWWBot_TRY = []
TWWBot_CY  = []

Q_TWW_GB  = []
Q_TWW_DB  = []
Q_TWW_TRY = []

Tp_GB  = []
Tp_DB  = []
Tp_TRY = []

P_EL_WP_GB  = []
P_EL_WP_DB  = []
P_EL_WP_TRY = []

P_PV_GB = []
P_PV_DB = []
P_PV_TRY = []

P_EL_Bed_GB = []
P_EL_Bed_DB = []
P_EL_Bed_TRY = []



Q_Hou = []
# Read in the results data#
Type = 'Clusteryear_'
filename = TRY + Type + str(start_time) +'_' + str(stop_time) +'.csv'
df = pd.read_csv(Direct+filename, header=None, names=['m_flow_Cons', 'TSupplyCons', 'TReturnnCons', 'P_EL_HP', 'Q_HP', 'TMeaSupHP', 'TDHWStoTop', 'TDHWStoBot', 'TBufStoTop', 'TBufStoBot', 'Modus',  'Tp', 'Q_TWW', 'Pel_PV', 'P_EL', 'Q_Hou'])
q_hp_CY.append(df['Q_HP'])
StoTop_CY.append(df['TBufStoTop'])
StoBot_CY.append(df['TBufStoBot'])
TWWTop_CY.append(df['TDHWStoTop'])
TWWBot_CY.append(df['TDHWStoBot'])
m_CY.append(df['Modus'])



Type = 'TRY_'
filename = TRY + Type + str(start_time) +'_' + str(stop_time) +'.csv'
df = pd.read_csv(Direct+filename, header=None, names=['m_flow_Cons', 'TSupplyCons', 'TReturnnCons', 'P_EL_HP', 'Q_HP', 'TMeaSupHP', 'TDHWStoTop', 'TDHWStoBot', 'TBufStoTop', 'TBufStoBot', 'Modus', 'Tp', 'Q_TWW', 'Pel_PV', 'P_EL', 'Q_Hou'])
q_hp_TRY.append(df['Q_HP'])
StoTop_TRY.append(df['TBufStoTop'])
StoBot_TRY.append(df['TBufStoBot'])
TWWTop_TRY.append(df['TDHWStoTop'])
TWWBot_TRY.append(df['TDHWStoBot'])
m_TRY.append(df['Modus'])
Q_TWW_TRY.append(df['Q_TWW'])
Tp_TRY.append(df['Tp'])
P_EL_WP_TRY.append(df['P_EL_HP'])
P_PV_TRY.append(df['Pel_PV'])
P_EL_Bed_TRY.append(df['P_EL'])
Q_Hou.append(df['Q_Hou'])

Type = 'DB_'
filename = TRY + Type + str(start_time) +'_' + str(stop_time) +'.csv'
df = pd.read_csv(Direct+filename, header=None, names=['m_flow_Cons', 'TSupplyCons', 'TReturnnCons', 'P_EL_HP', 'Q_HP', 'TMeaSupHP', 'TDHWStoTop', 'TDHWStoBot', 'TBufStoTop', 'TBufStoBot', 'Modus',  'Tp', 'Q_TWW', 'Pel_PV', 'P_EL','Q_Hou'])

q_hp_DB.append(df['Q_HP'])
StoTop_DB.append(df['TBufStoTop'])
StoBot_DB.append(df['TBufStoBot'])
TWWTop_DB.append(df['TDHWStoTop'])
TWWBot_DB.append(df['TDHWStoBot'])
m_DB.append(df['Modus'])
Q_TWW_DB.append(df['Q_TWW'])
Tp_DB.append(df['Tp'])
P_EL_WP_DB.append(df['P_EL_HP'])
P_PV_DB.append(df['Pel_PV'])
P_EL_Bed_DB.append(df['P_EL'])


Type = 'GB_'
filename = TRY + Type + str(start_time) +'_' + str(stop_time) +'.csv'
df = pd.read_csv(Direct+filename, header=None, names=['m_flow_Cons', 'TSupplyCons', 'TReturnnCons', 'P_EL_HP', 'Q_HP', 'TMeaSupHP', 'TDHWStoTop', 'TDHWStoBot', 'TBufStoTop', 'TBufStoBot', 'Modus',  'Tp', 'Q_TWW', 'Pel_PV', 'P_EL', 'Q_Hou'])

q_hp_GB.append(df['Q_HP'])
StoTop_GB.append(df['TBufStoTop'])
StoBot_GB.append(df['TBufStoBot'])
TWWTop_GB.append(df['TDHWStoTop'])
TWWBot_GB.append(df['TDHWStoBot'])
m_GB.append(df['Modus'])
Q_TWW_GB.append(df['Q_TWW'])
Tp_GB.append(df['Tp'])
P_EL_WP_GB.append(df['P_EL_HP'])
P_EL_WP_GB.append(df['P_EL_HP'])
P_PV_GB.append(df['Pel_PV'])
P_EL_Bed_GB.append(df['P_EL'])


#Time = np.arange(0,24,0.25)
Time = np.arange(0,24*7,0.25)
#### Create Plot
print(len(q_hp_GB[0]))
print(Time)
fig, axs = plt.subplots(3, 1)
axs[0].plot(np.array(Time), q_hp_DB[0][97:len(q_hp_DB[0])]/1000, label='DB', color=colors[('blue', 75)])
axs[0].plot(np.array(Time), q_hp_GB[0][97:len(q_hp_GB[0])]/1000, label='GB', color=colors[('red', 100)])
axs[0].plot(np.array(Time), q_hp_TRY[0][97:len(q_hp_TRY[0])]/1000, label='MILP', color=colors[('orange', 100)])
#axs[0].plot(np.array(Time), q_hp_DB[0][97:len(q_hp_DB[0])]/1000, label='Cluster')
#axs[0].plot(np.array(Time), q_hp_GB[0][97:len(q_hp_GB[0])]/1000, label='GB')
axs[0].set_ylim(-.500, 10.500)
axs[0].set_yticks(np.arange(0, 12.500, 5.000))
axs[0].set_ylabel('$\dot{Q}_{\mathrm{WP}}$ in kW')
axs[0].set_title(Monat, loc='left')
axs[0].set_xticks(np.arange(12, 168, 24))


#ax2.set_ylabel('Modus')
#ax2.plot(np.array(Time), Modus, label='Modus', color='#4B81C4', drawstyle='steps', linestyle='dashed')
axs[0].set_xticklabels([])
axs[1].plot(np.array(Time), m_DB[0][97:len(StoTop_DB[0])], color=colors[('blue', 75)])
axs[1].plot(np.array(Time), m_GB[0][97:len(StoTop_GB[0])], color=colors[('red', 100)])
axs[1].plot(np.array(Time), m_TRY[0][97:len(StoTop_TRY[0])], color=colors[('orange', 100)])
axs[1].set_yticks(np.arange(0,5,2))
axs[1].set_ylim(-0.15, 4.15)
axs[1].set_ylabel('Modus')
axs[1].set_xticks(np.arange(12, 168, 24))
axs[1].set_xticklabels([])
#axs[2].plot(np.array(Time), StoTop_DB[0][97:len(StoTop_DB[0])] - 273.15, color=colors[('blue', 75)])
#axs[2].plot(np.array(Time), StoTop_GB[0][97:len(StoTop_TRY[0])] - 273.15, color=colors[('red', 100)])
#axs[2].plot(np.array(Time), StoTop_TRY[0][97:len(StoTop_GB[0])] - 273.15, color=colors[('orange', 100)])
#if Monat == 'Januar':
#    axs[2].axhline(y=32, color='lightgrey', linestyle='--')
#else:
#    pass
#axs[1].plot(np.array(Time), TWWTop_GB[0][97:len(TWWTop_GB[0])] - 273.15, label='$T_{\mathrm{TWW}}$', color='#8768B4',           linestyle='dashdot')
#axs[2].set_ylabel('$T_{\mathrm{PS}}$ in °C')
axs[2].set_ylim(17, 72)
axs[2].set_yticks([20, 45, 70])
axs[2].set_xticks(np.arange(12, 168, 24))
#axs[2].set_xticklabels([])

#TWW_mean_GB=np.mean([TWWTop_TRY[0], TWWTop_TRY[0]], axis=0)
#print(TWW_mean_GB)
axs[2].plot(np.array(Time), TWWTop_DB[0][97:len(TWWTop_DB[0])] - 273.15, color=colors[('blue', 75)])
axs[2].plot(np.array(Time), TWWTop_GB[0][97:len(TWWTop_TRY[0])] - 273.15, color=colors[('red', 100)])
axs[2].plot(np.array(Time), TWWTop_TRY[0][97:len(TWWTop_GB[0])] - 273.15, color=colors[('orange', 100)])

axs[2].set_ylabel('$T_{\mathrm{TWW}}$ in °C')
#axs[3].set_ylim(17, 72)
#axs[3].set_yticks([20, 45, 70])
fig.legend(ncol=3, bbox_to_anchor=(0.95, 1.0), frameon=False)
xticks_labels = ['Mo', 'Di', 'Mi','Do','Fr','Sa','So']  # labels of the ticks
#axs[3].set_xticks(np.arange(12, 168, 24))
axs[2].set_xticklabels(xticks_labels)
axs[2].set_xlabel('Zeit in d')
axs[2].axvspan(24, 48, color='grey', alpha=0.2)
axs[2].axvspan(72, 96, color='grey', alpha=0.2)
axs[2].axvspan(120, 144, color='grey',alpha=0.2)
#axs[3].axvspan(24, 48, color='grey', alpha=0.2)
#axs[3].axvspan(72, 96, color='grey', alpha=0.2)
#axs[3].axvspan(120, 144, color='grey',alpha=0.2)
axs[1].axvspan(24, 48, color='grey', alpha=0.2)
axs[1].axvspan(72, 96, color='grey', alpha=0.2)
axs[1].axvspan(120, 144, color='grey',alpha=0.2)
axs[0].axvspan(24, 48, color='grey', alpha=0.2)
axs[0].axvspan(72, 96, color='grey', alpha=0.2)
axs[0].axvspan(120, 144, color='grey',alpha=0.2)



#plt.savefig(Savedirect + '_TRY_'+Monat+'TWW.png')
#tikzplotlib.save(Savedirect + '_TRY_'+Monat+'TWW.tex')
#plt.savefig(Savedirect + '_TRY_'+Monat+'TWW.pdf')
plt.show()








