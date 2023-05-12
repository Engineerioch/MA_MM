import fmpy as fmpy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tikzplotlib

from plot_results_to_files import latex_fullpage
from plot_results_to_files import latex_base

plt.rcParams.update(latex_fullpage)
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
Savedirect = 'D://lma-mma/Repos/MA_MM/Datensicherung/Sim/'
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

print(len(q_hp_GB[0]))
print(Time)
fig, axs = plt.subplots(4, 1)
axs[0].plot(np.array(Time), q_hp_DB[0][97:len(q_hp_DB[0])]/1000, label='DB')
axs[0].plot(np.array(Time), q_hp_GB[0][97:len(q_hp_GB[0])]/1000, label='GB')
axs[0].plot(np.array(Time), q_hp_TRY[0][97:len(q_hp_TRY[0])]/1000, label='MILP')
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

axs[1].plot(np.array(Time), m_DB[0][97:len(StoTop_DB[0])])
axs[1].plot(np.array(Time), m_GB[0][97:len(StoTop_GB[0])])
axs[1].plot(np.array(Time), m_TRY[0][97:len(StoTop_TRY[0])])
axs[1].set_yticks(np.arange(0, 5, 1))
axs[1].set_ylim(-0.15, 4.15)
#axs[1].plot(np.array(Time), TWWTop_GB[0][97:len(TWWTop_GB[0])] - 273.15, label='$T_{\mathrm{TWW}}$', color='#8768B4',           linestyle='dashdot')
axs[1].set_ylabel('Modus')

axs[1].set_xticks(np.arange(12, 168, 24))
axs[1].set_xticklabels([])


axs[2].plot(np.array(Time), StoTop_DB[0][97:len(StoTop_DB[0])] - 273.15)
axs[2].plot(np.array(Time), StoTop_GB[0][97:len(StoTop_TRY[0])] - 273.15)
axs[2].plot(np.array(Time), StoTop_TRY[0][97:len(StoTop_GB[0])] - 273.15)
if Monat == 'Januar':
    axs[2].axhline(y=32, color='lightgrey', linestyle='--')
else:
    pass
#axs[1].plot(np.array(Time), TWWTop_GB[0][97:len(TWWTop_GB[0])] - 273.15, label='$T_{\mathrm{TWW}}$', color='#8768B4',           linestyle='dashdot')
axs[2].set_ylabel('$T_{\mathrm{PS}}$ in °C')
axs[2].set_ylim(17, 72)
axs[2].set_yticks([20, 32, 45, 70])
axs[2].set_xticks(np.arange(12, 168, 24))
axs[2].set_xticklabels([])

TWW_mean_GB=np.mean([TWWTop_TRY[0], TWWTop_TRY[0]], axis=0)
print(TWW_mean_GB)
axs[3].plot(np.array(Time), TWWTop_DB[0][97:len(TWWTop_DB[0])] - 273.15)
axs[3].plot(np.array(Time), TWWTop_GB[0][97:len(TWWTop_TRY[0])] - 273.15)
axs[3].plot(np.array(Time), TWWTop_TRY[0][97:len(TWWTop_GB[0])] - 273.15)

#axs[1].plot(np.array(Time), TWWTop_GB[0][97:len(TWWTop_GB[0])] - 273.15, label='$T_{\mathrm{TWW}}$', color='#8768B4',           linestyle='dashdot')
axs[3].set_ylabel('$T_{\mathrm{TWW}}$ in °C')
axs[3].set_ylim(17, 72)
axs[3].set_yticks([20, 45, 70])
fig.legend(ncol=3, bbox_to_anchor=(0.95, 1.0), frameon=False)
xticks_labels = ['Mo', 'Di', 'Mi','Do','Fr','Sa','So']  # labels of the ticks
axs[3].set_xticks(np.arange(12, 168, 24))
axs[3].set_xticklabels(xticks_labels)
axs[3].set_xlabel('Zeit in d')









axs[2].axvspan(24, 48, color='grey', alpha=0.2)
axs[2].axvspan(72, 96, color='grey', alpha=0.2)
axs[2].axvspan(120, 144, color='grey',alpha=0.2)
axs[3].axvspan(24, 48, color='grey', alpha=0.2)
axs[3].axvspan(72, 96, color='grey', alpha=0.2)
axs[3].axvspan(120, 144, color='grey',alpha=0.2)
axs[1].axvspan(24, 48, color='grey', alpha=0.2)
axs[1].axvspan(72, 96, color='grey', alpha=0.2)
axs[1].axvspan(120, 144, color='grey',alpha=0.2)
axs[0].axvspan(24, 48, color='grey', alpha=0.2)
axs[0].axvspan(72, 96, color='grey', alpha=0.2)
axs[0].axvspan(120, 144, color='grey',alpha=0.2)



#plt.savefig(Savedirect + '_TRY_'+Monat+'.svg')
#tikzplotlib.save(Savedirect + '_TRY_'+Monat+'.tex')
#plt.savefig(Savedirect + '_TRY_'+Monat+'.pdf')
plt.show()

#print(Q_TWW_DB)
j=[]
TWW_Strafe_DB = []
TWW_Ges_DB = []
for i in range (97, len(Q_TWW_DB[0])):
    if TWWTop_DB[0][i] - 273.15 <= Tp_DB[0][i]:
        TWW_Strafe_DB.append(Q_TWW_DB[0][i])
#        print(TWWTop_DB[0][i]-273.15, Tp_DB[0][i])
        j.append(i)
        TWW_Ges_DB.append(Q_TWW_DB[0][i])
    else:
        TWW_Ges_DB.append(Q_TWW_DB[0][i])


TWW_Strafe_GB = []
TWW_Ges_GB = []
for i in range (97, len(Q_TWW_GB[0])):
    if TWWTop_GB[0][i] - 273.15 <= Tp_GB[0][i]:
        TWW_Strafe_GB.append(Q_TWW_GB[0][i])
 #       print(TWWTop_GB[0][i]-273.15, Tp_GB[0][i])
        j.append(i)
        TWW_Ges_GB.append(Q_TWW_GB[0][i])
    else:
        TWW_Ges_GB.append(Q_TWW_GB[0][i])


TWW_Strafe_TRY = []
TWW_Ges_TRY = []
for i in range (97, len(Q_TWW_TRY[0])):
    if TWWTop_TRY[0][i] - 273.15 <= Tp_TRY[0][i]:
        TWW_Strafe_TRY.append(Q_TWW_TRY[0][i])
#        print(TWWTop_TRY[0][i]-273.15, Tp_TRY[0][i])
        j.append(i)
        TWW_Ges_TRY.append(Q_TWW_TRY[0][i])
    else:
        TWW_Ges_TRY.append(Q_TWW_TRY[0][i])

#print(sum(TWW_Ges_TRY))
#print(sum(TWW_Ges_GB))
#print(sum(TWW_Ges_DB))
#
#print(sum(TWW_Strafe_TRY))
#print(sum(TWW_Strafe_GB))
#print(sum(TWW_Strafe_DB))
#

Power_GB = []
Power_DB =[]
Power_TRY = []

Power_WP_GB = []
Power_WP_DB =[]
Power_WP_TRY = []

Power_WP_TWW_GB = []
Power_WP_TWW_DB = []
Power_WP_TWW_TRY = []

Q_Bed = []


Cost_ = []

for i in range(97, len(P_PV_GB[0])):
    Power_GB.append(((P_EL_Bed_GB[0][i] * 1000) + P_EL_WP_GB[0][i] - P_PV_GB[0][i])/4000)
#    Power_WP_GB.append(P_EL_WP_GB[0][i]/4000)
#    Power_GB.append(P_PV_GB[0][i])
        # + P_EL_WP_GB[0][i] - P_PV_GB[0][i])
    if m_GB[0][i] == 1 or m_GB[0][i] == 2:
        Power_WP_GB.append(P_EL_WP_GB[0][i]/4000)
    else:
        Power_WP_TWW_GB.append(P_EL_WP_GB[0][i]/4000)


for i in range(97, len(P_PV_DB[0])):
    Power_DB.append(((P_EL_Bed_DB[0][i] * 1000) + P_EL_WP_DB[0][i] - P_PV_DB[0][i])/4000)
#    Power_WP_DB.append(P_EL_WP_DB[0][i]/4000)
    if m_DB[0][i] == 1 or m_DB[0][i] == 2:
        Power_WP_DB.append(P_EL_WP_DB[0][i]/4000)
    else:
        Power_WP_TWW_DB.append(P_EL_WP_DB[0][i]/4000)

for i in range(97, len(P_PV_TRY[0])):
    Power_TRY.append(((P_EL_Bed_TRY[0][i] * 1000) + P_EL_WP_TRY[0][i] - P_PV_TRY[0][i])/4000)
    Q_Bed.append(Q_Hou[0][i]/4000)
    if m_TRY[0][i] == 1 or m_TRY[0][i] == 2:
        Power_WP_TRY.append(P_EL_WP_TRY[0][i]/4000)
    else:
        Power_WP_TWW_TRY.append(P_EL_WP_TRY[0][i]/4000)




print('TWW-Nichtdeckung_GB ist [kWh]' + str(sum(TWW_Strafe_GB)))
print('TWW-Nichtdeckung_DB ist [kWh]' + str(sum(TWW_Strafe_DB)))
print('TWW-Nichtdeckung_TRY ist [kWh]' + str(sum(TWW_Strafe_TRY)))
print('TWW-Bedarf ist [kWh]' + str(sum(TWW_Ges_TRY)))



print('Power_GB ist [kWh]'+ str(sum(Power_GB)))
print('Power_DB ist [kWh]'+ str(sum(Power_DB)))
print('Power_TRY ist [kWh]'+ str(sum(Power_TRY)))
print('Power_WP_GB ist [kWh]'+ str(sum(Power_WP_GB)))
print('Power_WP_DB ist [kWh]'+ str(sum(Power_WP_DB)))
print('Power_WP_TRY ist [kWh]'+ str(sum(Power_WP_TRY)))

print('Power_WP_TWW_GB ist [kWh]'+ str(sum(Power_WP_TWW_GB)))
print('Power_WP_TWW_DB ist [kWh]'+ str(sum(Power_WP_TWW_DB)))
print('Power_WP_TWW_TRY ist [kWh]'+ str(sum(Power_WP_TWW_TRY)))


print('Wärmebedarf ist [kWh]'+ str(sum(Q_Bed)))
#print(Power_GB)
#print(P_EL_Bed_GB)
#print(P_PV_GB)
#print(P_PV_GB)


Jul_TWW_GB = 7.35
Jul_TWW_DB = 5.25
Jul_TWW_TRY = 0.315

Jul_Q_TWW = 81.585

Jul_Power_GB = -122.6
Jul_Power_DB = -118.4
Jul_Power_TRY = -126.75

Jul_Power_WP_GB = 0
Jul_Power_WP_DB = 0
Jul_Power_WP_TRY = 0

Jul_Power_WP_TWW_GB = 31.9
Jul_Power_WP_TWW_DB = 36.2
Jul_Power_WP_TWW_TRY = 27.8
Jul_Q_TWW = 81.585

Jul_Q_Hou = 0

Jan_TWW_GB = 7.35
Jan_TWW_DB = 7.45
Jan_TWW_TRY = 1.05

Jan_Q_TWW = 81.585

Jan_Power_GB = 438.9
Jan_Power_DB = 439.4
Jan_Power_TRY = 435.25

Jan_Power_WP_GB = 330.6
Jan_Power_WP_DB = 330.0
Jan_Power_WP_TRY = 297.4

Jan_Q_Hou = 793.4


plt.rcParams.update(latex_base)
bins = [0, 2.5, 5, 7.5]
GB_1 = [Jan_Power_GB, Jan_Power_WP_GB, Jul_Power_GB]
DB_1 = [Jan_Power_DB, Jan_Power_WP_DB, Jul_Power_DB]
TRY_1 = [Jan_Power_TRY, Jan_Power_WP_TRY, Jul_Power_TRY]
Bed_1 = [0, Jan_Q_Hou, Jul_Q_Hou]

GB_7 = [Jul_Power_GB, Jul_Power_WP_GB]
DB_7 = [Jul_Power_DB, Jul_Power_WP_DB]
TRY_7 = [Jul_Power_TRY, Jul_Power_WP_TRY]
Bed_7 = [0, Jan_Q_Hou, Jul_Q_Hou]

Safeordner = 'D://lma-mma/Repos/MA_MM/Datensicherung/Plots/'

x = np.arange(1,len(GB_1)+1)
width = 0.2

fig, ax = plt.subplots(1)

ax.set_xticks(x)
ax.set_xlim(0.5,3.3)
ax.set_xticklabels(['Januar Gesamt', 'Wärmeerzeugung', 'Juli Gesamt'])
ax.bar(x - 1.5*width, DB_1, width=width, label='DB')
ax.bar(x-0.5*width, GB_1 , width=width, label='GB')
ax.bar(x + 0.5*width, TRY_1, width=width, label='MILP')
ax.bar(x+ 1.5*width, Bed_1, width=width, label='Wärmebedarf')
#ax.set_title('Strombedarf')
ax.legend(loc ='upper left', ncol=2,)
#a[]x.set_ylim(0,95)
ax.set_xticks([0.9, 2, 2.9])
ax.set_xticklabels(['Januar Gesamt', 'Januar Wärmeerzeugung', 'Juli Gesamt'])
ax.axhline(0, color= 'black')
ax.set_ylabel('Energie in kWh')

plt.savefig(Safeordner + 'SimAnalyse_P.svg')
plt.savefig(Safeordner + 'SimAnalyse_P.pdf')
tikzplotlib.save(Safeordner + 'SimAnalyse_P.tex')
plt.show()

DB_2 = [(Jan_Q_TWW-Jan_TWW_DB), (Jul_Q_TWW-Jul_TWW_DB)]
GB_2 = [Jan_Q_TWW-Jan_TWW_GB, Jul_Q_TWW-Jul_TWW_GB]
TRY_2 = [Jan_Q_TWW-Jan_TWW_TRY, Jul_Q_TWW-Jul_TWW_TRY]
Bed_2 = [Jan_Q_TWW, Jul_Q_TWW]
x = np.arange(1,len(GB_2)+1)
print(GB_2)

fig, ax = plt.subplots(1)

ax.set_xticks(x)


ax.bar(x - 1.5*width, DB_2, width=width, label='DB')
ax.bar(x-0.5*width, GB_2 , width=width, label='GB')
ax.bar(x + 0.5*width, TRY_2, width=width, label='MILP')
ax.bar(x+ 1.5*width, Bed_2, width=width, label='TWW-Bedarf')
#ax.set_title('')
ax.legend(loc ='lower left', ncol=2)
#a[]x.set_ylim(0,95)
ax.set_xticks([0.999, 1.9999999999999])
ax.set_xticklabels(['Januar', 'Juli'])
#ax.axhline(0, color= 'black')
ax.set_ylabel('Energie in kWh')



plt.savefig(Safeordner + 'SimAnalyse_TWW.svg')
plt.savefig(Safeordner + 'SimAnalyse_TWW.pdf')
tikzplotlib.save(Safeordner + 'SimAnalyse_TWW.tex')
plt.show()









