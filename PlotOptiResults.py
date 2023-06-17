import fmpy as fmpy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tikzplotlib

from plot_results_to_files import latex_fullpage
from plot_results_to_files import pp_figure
from rwth_colors import colors
from rwth_colors import plot_colors
#plot_colors()
plt.rcParams.update(latex_fullpage)

##### This File is made to plot the Optimization results
# Set here what the results are from: TRY: 'normal', 'warm' or 'cold'
TRY = 'normal'
# Type: 'Clusterday', 'Clusteryear' or 'TRY'
Type = 'Clusterday'
filename_start = '0_025_48_4_24_'+Type+ '_'

# If You have a Heat Storage size, that is not 300l for PS or 200l for TWW-Storage you have to adapt the following line
filename_save_rest = TRY+'_Fix_TWW_Small_Norm'
filename_rest = '_'+filename_save_rest+'.csv'
Data = 'Data_'
Mode = 'Modes_'
Direct = 'D://lma-mma/Repos/MA_MM/Results/Optimierung/TWW/Clusterday/'
Directory = 'D://lma-mma/Repos/MA_MM/Results/Optimierung/TWW/'
Savedirect = 'D://lma-mma/Repos/MA_MM/Datensicherung/Presi/'+filename_save_rest

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
q_hp_w =[]
m_1 = []
m_2 = []
m_3 = []
m_4 = []
m_5 = []
m_6 = []
m_7 = []
m_8 = []
m_w = []
Sto_1 =[]
Sto_2 =[]
Sto_3 =[]
Sto_4 =[]
Sto_5 =[]
Sto_6 =[]
Sto_7 =[]
Sto_8 =[]
Sto_w = []
TWW_1 = []
TWW_2 = []
TWW_3 = []
TWW_4 = []
TWW_5 = []
TWW_6 = []
TWW_7 = []
TWW_8 = []
TWW_w = []

pv_1 = []
pv_2 = []
pv_3 = []
pv_4 = []
pv_5 = []
pv_6 = []
pv_7 = []
pv_8 = []
pv_w = []

q_hou_1 = []
q_hou_2 = []
q_hou_3 = []
q_hou_4 = []
q_hou_5 = []
q_hou_6 = []
q_hou_7 = []
q_hou_8 = []
q_hou_w = []




c_5 = []

# Reading of data of Clusterdays and create list with each data for each day
for i in range(0,8,1):
    df = []
    df = pd.read_csv(Direct+Data+filename_start+str(i)+filename_rest, header=None, names=['T_Air', 'Q_Hou', 'P_PV', 'P_EL_Dem', 'T_Mean', 'c_grid', 'Q_TWW', 'T_Sto', 'T_TWW', 'COP_1', 'COP_2', 'Q_HP',  'Q_Penalty'])
    mf = pd.read_csv(Direct+Mode+filename_start+str(i)+filename_rest, header=None, names=['Modes'])
    if i == 0:
        q_hp_1.append(df['Q_HP'])
        Sto_1.append(df['T_Sto'])
        TWW_1.append(df['T_TWW'])
        m_1.append(mf['Modes'])
        pv_1.append(df['P_PV'])
        q_hou_1.append(df['Q_Hou'])
    elif i == 1:
        q_hp_2.append(df['Q_HP'])
        Sto_2.append(df['T_Sto'])
        TWW_2.append(df['T_TWW'])
        m_2.append(mf['Modes'])
        pv_2.append(df['P_PV'])
        q_hou_2.append(df['Q_Hou'])
    elif i == 2:
        q_hp_3.append(df['Q_HP'])
        Sto_3.append(df['T_Sto'])
        TWW_3.append(df['T_TWW'])
        m_3.append(mf['Modes'])
        pv_3.append(df['P_PV'])
        q_hou_3.append(df['Q_Hou'])
    elif i == 3:
        q_hp_4.append(df['Q_HP'])
        Sto_4.append(df['T_Sto'])
        TWW_4.append(df['T_TWW'])
        m_4.append(mf['Modes'])
        pv_4.append(df['P_PV'])
        q_hou_4.append(df['Q_Hou'])
    elif i == 4:
        q_hp_5.append(df['Q_HP'])
        Sto_5.append(df['T_Sto'])
        TWW_5.append(df['T_TWW'])
        m_5.append(mf['Modes'])
        pv_5.append(df['P_PV'])
        q_hou_5.append(df['Q_Hou'])
    elif i == 5:
        q_hp_6.append(df['Q_HP'])
        Sto_6.append(df['T_Sto'])
        TWW_6.append(df['T_TWW'])
        m_6.append(mf['Modes'])
        pv_6.append(df['P_PV'])
        q_hou_6.append(df['Q_Hou'])
    elif i == 6:
        q_hp_7.append(df['Q_HP'])
        Sto_7.append(df['T_Sto'])
        TWW_7.append(df['T_TWW'])
        m_7.append(mf['Modes'])
        c_5.append(df['c_grid'])
        pv_7.append(df['P_PV'])
        q_hou_7.append(df['Q_Hou'])
    elif i == 7:
        q_hp_8.append(df['Q_HP'])
        Sto_8.append(df['T_Sto'])
        TWW_8.append(df['T_TWW'])
        m_8.append(mf['Modes'])
        pv_8.append(df['P_PV'])
        q_hou_8.append(df['Q_Hou'])


# If Type = 'Clusterday': select the second line, if Type='TRY' or 'Clusteryear' select the first line
#Time = np.arange(0,34944,1)
Time = np.arange(0,24*3,0.25)
#Time=np.arange(0,24,0.25)
#print(c_5[0][40:80])


#################################### Create a plot for each typteday

#fig, ax = plt.subplots(4, 2) #sharey=True)
#ax[0,0].plot(np.array(Time), q_hp_1[0][96:192]*4/1000, label='$\dot{Q_{\mathrm{WP}}}$')
#ax2 = ax[0,0].twinx()
#ax2.plot(np.array(Time), m_1[0][96:192], color='#4B81C4', drawstyle='steps', linestyle='dashed', label='Modus')
#ax[0,0].set_ylabel('$\dot{Q_{\mathrm{WP}}}$ in kW')
#ax[0,0].set_ylim(-0.500,10.5)
#ax[0,0].set_yticks(np.arange(0,12.500,2.500))
#ax2.set_yticks(np.arange(0,4,1))
#ax2.set_ylim(-0.15,3.15)
#ax2.set_yticklabels([])
#ax[0,0].set_title('kalter Wintertag')
#ax[0,0].legend(loc='lower left', handles=[ax[0,0].lines[0], ax2.lines[0]], labels=['$\dot{Q_{\mathrm{WP}}}$', 'Modus'],fontsize='small')
#
#ax[0,1].plot(np.array(Time), q_hp_3[0][96:192]*4/1000)
#ax2 = ax[0,1].twinx()
#ax[0,1].set_yticklabels([])
#ax2.set_ylabel('Modus')
#ax2.plot(np.array(Time), m_3[0][96:192], color='#4B81C4',drawstyle='steps',linestyle='dashed')
#ax[0,1].set_ylim(-0.500,10.5)
#ax2.set_ylim(-0.15,3.15)
#ax[0,1].set_yticks(np.arange(0,12.500,2.500))
#ax2.set_yticks(np.arange(0,4,1))
#ax[0,1].set_title('Wintertag')
#
#
#ax[1,0].plot(np.array(Time), q_hp_2[0][96:192]*4/1000)
#ax2 = ax[1,0].twinx()
#ax[1,0].set_ylim(-0.500,10.5)
#ax2.plot(np.array(Time), m_2[0][96:192], color='#4B81C4', drawstyle='steps',linestyle='dashed')
#ax[1,0].set_yticks(np.arange(0,12.500,2.500))
#ax2.set_yticks(np.arange(0,4,1))
#ax2.set_yticklabels([])
#ax2.set_ylim(-0.15,3.15)
#ax[1,0].set_ylabel('$\dot{Q_{\mathrm{WP}}}$ in kW')
#ax[1,0].set_title('Regentag')
#
#
#
#ax[1,1].plot(np.array(Time), q_hp_4[0][96:192]*4/1000)
#ax2 = ax[1,1].twinx()
#ax[1,1].set_ylim(-0.500,10.5)
#ax[1,1].set_yticks(np.arange(0,12.500,2.500))
#ax[1,1].set_yticklabels([])
#ax2.set_yticks(np.arange(0,4,1))
#ax2.set_ylabel('Modus')
#ax2.set_ylim(-0.15,3.15)
#ax2.plot(np.array(Time), m_4[0][96:192], color='#4B81C4',drawstyle='steps',linestyle='dashed')
#ax[1,1].set_title('Frühlingstag')
#
#ax[2,0].plot(np.array(Time), q_hp_7[0][96:192]*4/1000)
#ax2 = ax[2,0].twinx()
#ax[2,0].set_ylim(-0.500,10.5)
#ax2.plot(np.array(Time), m_7[0][96:192], color='#4B81C4',drawstyle='steps',linestyle='dashed')
#ax[2,0].set_yticks(np.arange(0,12.500,2.500))
#ax2.set_yticks(np.arange(0,4,1))
#ax2.set_yticklabels([])
#ax2.set_ylim(-0.15,3.15)
#ax[2,0].set_ylabel('$\dot{Q_{\mathrm{WP}}}$ in W')
#ax[2,0].set_title('Sommertag')
#
#
#ax[2,1].plot(np.array(Time), q_hp_5[0][96:192]*4/1000)
#ax2 = ax[2,1].twinx()
#ax[2,1].set_ylim(-0.500,10.5)
#ax[2,1].set_yticks(np.arange(0,12.500,2.500))
#ax2.set_yticks(np.arange(0,4,1))
#ax[2,1].set_yticklabels([])
#ax2.set_ylabel('Modus')
#ax2.set_ylim(-0.15,3.15)
#ax2.plot(np.array(Time), m_5[0][96:192], color='#4B81C4',drawstyle='steps',linestyle='dashed')
#ax[2,1].set_title('Hochsommertag')
#
#ax[3,0].plot(np.array(Time), q_hp_6[0][96:192]*4/1000)
#ax[3,0].set_xlabel('Zeit in h')
#ax2 = ax[3,0].twinx()
#ax[3,0].set_ylim(-0.500,10.5)
#ax[3,0].set_yticks(np.arange(0,12.500,2.500))
#ax2.set_yticks(np.arange(0,4,1))
#ax2.set_yticklabels([])
#ax2.plot(np.array(Time), m_6[0][96:192], color='#4B81C4',drawstyle='steps',linestyle='dashed')
#ax[3,0].set_ylabel('$\dot{Q_{\mathrm{WP}}}$ in W')
#ax[3,0].set_title('Herbsttag')
#
#ax[3,1].plot(np.array(Time), q_hp_8[0][96:192]*4/1000)
#ax[3,1].set_xlabel('Zeit in h')
#ax[3,1].set_yticklabels([])
#ax2 = ax[3,1].twinx()
#ax[3,1].set_ylim(-0.500,10.5)
#ax[3,1].set_yticks(np.arange(0,12.500,2.500))
#ax2.set_yticks(np.arange(0,4,1))
#ax2.set_ylabel('Modus')
#ax2.set_ylim(-0.15,3.15)
#ax2.plot(np.array(Time), m_8[0][96:192], color='#4B81C4',drawstyle='steps',linestyle='dashed')
#ax[3,1].set_title('kühler Herbsttag')
#plt.savefig(Savedirect+'_Alle.svg')
#tikzplotlib.save(Savedirect+'_Alle.tex')
#plt.savefig(Savedirect+'_Alle.pdf')
#plt.show()
#
######################
#
#fig, ax = plt.subplots(4, 2)
#ax[0,0].plot(np.array(Time), Sto_1[0][96:192]-273.15 , label='$T_{\mathrm{PS}}$')
#ax[0,0].plot(np.array(Time), TWW_1[0][96:192]-273.15, label='$T_{\mathrm{TWW}}$')
#ax[0,0].set_ylabel('$T$ in °C')
#ax[0,0].set_ylim(17,72)
#ax[0,0].set_yticks([20,35,50,65])
#ax[0,0].set_yticklabels([20,35,50,65])
#ax[0,0].set_title('kalter Sommertag')
#ax[0,0].legend(loc='lower left', handles=[ax[0,0].lines[0], ax2.lines[0]], labels=['$T_{\mathrm{PS}}$', '$T_{\mathrm{TWW}}$'])#,fontsize='small')
#
#ax[0,1].plot(np.array(Time), Sto_3[0][96:192]-273.15)
#ax[0,1].plot(np.array(Time), TWW_3[0][96:192]-273.15)
#ax[0,1].set_yticklabels([])
#ax[0,1].set_ylim(17,72)
#ax[0,1].set_yticks([20,35,50,65])
#ax[0,1].set_title('Wintertag')
#
#
#ax[1,0].plot(np.array(Time), Sto_2[0][96:192]-273.15)
#ax[1,0].plot(np.array(Time), TWW_2[0][96:192]-273.15)
#ax[1,0].set_ylim(17,72)
#ax[1,0].set_yticks([20,35,50,65])
#ax[1,0].set_ylabel('$T$ in °C')
#ax[1,0].set_title('Regentag')
#
#
#
#ax[1,1].plot(np.array(Time), Sto_4[0][96:192]-273.15)
#ax[1,1].plot(np.array(Time), TWW_4[0][96:192]-273.15)
#ax[1,1].set_ylim(17,72)
#ax[1,1].set_yticks([20,35,50,65])
#ax[1,1].set_yticklabels([])
#ax[1,1].set_title('Frühlingstag')
#
#ax[2,0].plot(np.array(Time), Sto_7[0][96:192]-273.15)
#ax[2,0].plot(np.array(Time), TWW_7[0][96:192]-273.15)
#ax[2,0].set_ylim(17,72)
#ax[2,0].set_yticks([20,35,50,65])
#ax[2,0].set_ylabel('$T$ in °C')
#ax[2,0].set_title('Sommertag')
#
#
#ax[2,1].plot(np.array(Time), Sto_5[0][96:192]-273.15)
#ax[2,1].plot(np.array(Time), TWW_5[0][96:192]-273.15)
#ax[2,1].set_ylim(17,72)
#ax[2,1].set_yticks([20,35,50,65])
#ax[2,1].set_yticklabels([])
#ax[2,1].set_title('Hochsommertag')
#
#ax[3,0].plot(np.array(Time), Sto_6[0][96:192]-273.15)
#ax[3,0].plot(np.array(Time), TWW_6[0][96:192]-273.15)
#ax[3,0].set_xlabel('Zeit in h')
#ax[3,0].set_ylim(17,72)
#ax[3,0].set_yticks([20,35,50,65])
#ax[3,0].set_ylabel('$T$ in °C')
#ax[3,0].set_title('Herbsttag')
#
#ax[3,1].plot(np.array(Time), Sto_8[0][96:192]-273.15)
#ax[3,1].plot(np.array(Time), TWW_8[0][96:192]-273.15)
#ax[3,1].set_xlabel('Zeit in h')
#ax[3,1].set_yticklabels([])
#ax[3,1].set_ylim(17,72)
#ax[3,1].set_yticks([20,35,50,65])
#ax[3,1].set_title('kühler Herbsttag')
#plt.savefig(Savedirect+'_Alle_T.svg')
#tikzplotlib.save(Savedirect+'_Alle_T.tex')
#plt.savefig(Savedirect+'_Alle_T.pdf')
#plt.show()


#plt.rcParams.update(pp_figure)
#fig, ax = plt.subplots()
#ax.plot(np.array(Time), q_hp_1[0][96:192]*4, label = '$\dot{Q_{\mathrm{WP}}}$')
#ax.set_xlabel('Zeit in h')
#ax.set_ylabel('$\dot{Q_{\mathrm{WP}}}$ in W')
#ax.set_ylim(-500,10500)
#ax2 = ax.twinx()
#ax2.set_ylabel('Modus')
#ax2.set_ylim(-0.15,3.15)
#ax2.plot(np.array(Time), m_1[0][96:192], color='#4B81C4', label = 'Modus',drawstyle='steps',linestyle='dashed' )
#ax2.set_yticks([0,1,2,3])
#ax.set_yticks(np.arange(0,12500,2500))
#ax2.set_yticks(np.arange(0,4,1))
#handles, labels =[],[]
#for ax in [ax, ax2]:
#    for h, l in zip(*ax.get_legend_handles_labels()):
#        handles.append(h)
#        labels.append(l)
#plt.legend(handles, labels, loc='lower left',fontsize='small')
#plt.savefig(Savedirect+'_kalterWintertag.svg')
#tikzplotlib.save(Savedirect+'_kalterWintertag.tex')
#plt.savefig(Savedirect+'_kalterWintertag.pdf')
#plt.show()
#
#fig, ax = plt.subplots()
#ax.plot(np.array(Time), q_hp_2[0][96:192]*4, label = '$\dot{Q_{\mathrm{WP}}}$')
#ax.set_xlabel('Zeit in h')
#ax.set_ylabel('$\dot{Q_{\mathrm{WP}}}$ in W')
#ax.set_ylim(-500,10500)
#ax2 = plt.twinx()
#ax2.set_ylabel('Modus')
#ax2.set_ylim(-0.15,3.15)
#ax2.plot(np.array(Time), m_2[0][96:192], color='#4B81C4', label = 'Modus',drawstyle='steps',linestyle='dashed')
#ax2.set_yticks([0,1,2,3])
#handles, labels =[],[]
#ax.set_yticks(np.arange(0,12500,2500))
#ax2.set_yticks(np.arange(0,4,1))
#for ax in [ax, ax2]:
#    for h, l in zip(*ax.get_legend_handles_labels()):
#        handles.append(h)
#        labels.append(l)
#plt.legend(handles, labels, loc='lower left',fontsize='small')
#plt.savefig(Savedirect+'_Regentag.svg')
#tikzplotlib.save(Savedirect+'_Regentag.tex')
#plt.savefig(Savedirect+'_Regentag.pdf')
#plt.show()
#
#fig, ax = plt.subplots()
#ax.plot(np.array(Time), q_hp_3[0][96:192]*4, label = '$\dot{Q_{\mathrm{WP}}}$')
#ax.set_xlabel('Zeit in h')
#ax.set_ylabel('$\dot{Q_{\mathrm{WP}}}$ in W')
#ax.set_ylim(-500,10500)
#ax2 = ax.twinx()
#ax2.set_ylabel('Modus')
#ax2.set_ylim(-0.15,3.15)
#ax.set_yticks(np.arange(0,12500,2500))
#ax2.set_yticks(np.arange(0,4,1))
#ax2.plot(np.array(Time), m_3[0][96:192], color='#4B81C4', label = 'Modus',drawstyle='steps',linestyle='dashed')
#ax2.set_yticks([0,1,2,3])
#handles, labels =[],[]
#for ax in [ax, ax2]:
#    for h, l in zip(*ax.get_legend_handles_labels()):
#        handles.append(h)
#        labels.append(l)
#plt.legend(handles, labels, loc='lower left',fontsize='small')
#plt.savefig(Savedirect+'_Wintertag.svg')
#tikzplotlib.save(Savedirect+'_Wintertag.tex')
#plt.savefig(Savedirect+'_Wintertag.pdf')
#plt.show()
#
#fig, ax = plt.subplots()
#ax.plot(np.array(Time), q_hp_4[0][96:192]*4, label = '$\dot{Q_{\mathrm{WP}}}$')
#ax.set_xlabel('Zeit in h')
#ax.set_ylabel('$\dot{Q_{\mathrm{WP}}}$ in W')
#ax.set_ylim(-500,10500)
#ax2 = plt.twinx()
#ax2.set_ylabel('Modus')
#ax2.set_ylim(-0.15,3.15)
#ax2.plot(np.array(Time), m_4[0][96:192], color='#4B81C4', label = 'Modus',drawstyle='steps',linestyle='dashed')
#ax2.set_yticks([0,1,2,3])
#ax.set_yticks(np.arange(0,12500,2500))
#ax2.set_yticks(np.arange(0,4,1))
#handles, labels =[],[]
#for ax in [ax, ax2]:
#    for h, l in zip(*ax.get_legend_handles_labels()):
#        handles.append(h)
#        labels.append(l)
#plt.legend(handles, labels, loc='upper left',fontsize='small')
#plt.savefig(Savedirect+'_Fruehlingstag.svg')
#tikzplotlib.save(Savedirect+'_Fruehlingstag.tex')
#plt.savefig(Savedirect+'_Fruehlingstag.pdf')
#plt.show()
#
#fig, ax = plt.subplots()
#ax.plot(np.array(Time), q_hp_5[0][96:192]*4, label = '$\dot{Q_{\mathrm{WP}}}$')
#ax.set_xlabel('Zeit in h')
#ax.set_ylabel('$\dot{Q_{\mathrm{WP}}}$ in W')
#ax.set_ylim(-500,10500)
#ax2 = plt.twinx()
#ax2.set_ylabel('Modus')
#ax2.set_ylim(-0.15,3.15)
#ax2.plot(np.array(Time), m_5[0][96:192], color='#4B81C4', label = 'Modus',drawstyle='steps', linestyle='dashed')
#ax2.set_yticks([0,1,2,3])
#handles, labels =[],[]
#ax.set_yticks(np.arange(0,12500,2500))
#ax2.set_yticks(np.arange(0,4,1))
#for ax in [ax, ax2]:
#    for h, l in zip(*ax.get_legend_handles_labels()):
#        handles.append(h)
#        labels.append(l)
#plt.legend(handles, labels,fontsize='small')
#plt.savefig(Savedirect+'_Hochsommertag.svg')
#tikzplotlib.save(Savedirect+'_Hochsommertag.tex')
#plt.savefig(Savedirect+'_Hochsommertag.pdf')
#plt.show()
#
#fig, ax = plt.subplots()
#ax.plot(np.array(Time), q_hp_6[0][96:192]*4, label = '$\dot{Q_{\mathrm{WP}}}$')
#ax.set_xlabel('Zeit in h')
#ax.set_ylabel('$\dot{Q_{\mathrm{WP}}}$ in W')
#ax.set_ylim(-500,10500)
#ax2 = plt.twinx()
#ax2.set_ylabel('Modus')
#ax2.set_ylim(-0.15,3.15)
#ax2.plot(np.array(Time), m_6[0][96:192], color='#4B81C4', label = 'Modus',drawstyle='steps',linestyle='dashed')
#ax2.set_yticks([0,1,2,3])
#ax.set_yticks(np.arange(0,12500,2500))
#ax2.set_yticks(np.arange(0,4,1))
#handles, labels =[],[]
#for ax in [ax, ax2]:
#    for h, l in zip(*ax.get_legend_handles_labels()):
#        handles.append(h)
#        labels.append(l)
#plt.legend(handles, labels,fontsize='small')
#plt.savefig(Savedirect+'_Herbsttag.svg')
#tikzplotlib.save(Savedirect+'_Herbsttag.tex')
#plt.savefig(Savedirect+'_Herbsttag.pdf')
#plt.show()
#
#fig, ax = plt.subplots()
#ax.plot(np.array(Time), q_hp_7[0][96:192]*4, label = '$\dot{Q_{\mathrm{WP}}}$')
#ax.set_xlabel('Zeit in h')
#ax.set_ylim(-500,10500)
#ax.set_ylabel('$\dot{Q_{\mathrm{WP}}}$ in W')
##plt.xlabel('Clustertag 8')
#ax2 = plt.twinx()
#ax2.set_ylabel('Modus')
#ax2.set_ylim(-0.15,3.15)
#ax.set_yticks(np.arange(0,12500,2500))
#ax2.set_yticks(np.arange(0,4,1))
#ax2.plot(np.array(Time), m_7[0][96:192], color='#4B81C4', label = 'Modus',drawstyle='steps',linestyle='dashed')
#ax2.set_yticks([0,1,2,3])
#handles, labels =[],[]
#for ax in [ax, ax2]:
#    for h, l in zip(*ax.get_legend_handles_labels()):
#        handles.append(h)
#        labels.append(l)
#plt.legend(handles, labels,fontsize='small')
#plt.savefig(Savedirect+'_Sommertag.svg')
#tikzplotlib.save(Savedirect+'_Sommertag.tex')
#plt.savefig(Savedirect+'_Sommertag.pdf')
##plt.show()
#
#fig, ax = plt.subplots()
#ax.plot(np.array(Time), q_hp_8[0][96:192]*4, label='$\dot{Q_{\mathrm{WP}}}$')
#ax.set_xlabel('Zeit in h')
#ax.set_ylabel('$\dot{Q_{\mathrm{WP}}}$ in W')
#ax.set_ylim(-500,10500)
#ax2 = ax.twinx()
#ax2.set_ylabel('Modus')
#ax2.set_ylim(-0.15,3.15)
#ax.set_yticks(np.arange(0,12500,2500))
#ax2.set_yticks(np.arange(0,4,1))
#ax2.set_ylabel('Modus')
#ax2.set_yticks([0,1,2,3])
#ax2.plot(np.array(Time), m_8[0][96:192], color='#4B81C4', label='Modus', drawstyle='steps',linestyle='dashed')
#handles, labels =[],[]
#for ax in [ax, ax2]:
#    for h, l in zip(*ax.get_legend_handles_labels()):
#        handles.append(h)
#        labels.append(l)
#plt.legend(handles, labels, loc='upper left',fontsize='small')
#ax2.set_ylabel('Modus')
#plt.savefig(Savedirect+'_kuehlerHerbsttag.svg')
#tikzplotlib.save(Savedirect+'_kuehlerHerbsttag.tex')
#plt.savefig(Savedirect+'_kuehlerHerbsttag.pdf')
#plt.show()
##
##
##
#
#
#
#
#fig, ax = plt.subplots()
#ax.plot(np.array(Time), Sto_1[0][96:192]-273.15, label = '$T_{\mathrm{PS}}$')
#ax.plot(np.array(Time), TWW_1[0][96:192]-273.15, color='#4B81C4', label = '$T_{\mathrm{TWW}}$',linestyle='dashed')
#ax.set_xlabel('Zeit in h')
#ax.set_ylabel('$T$ in °C')
#ax.set_ylim(17,72)
#ax.set_yticks([20,35,50,65])
#plt.legend(loc='lower left')
##plt.savefig(Savedirect+'_kalterWintertag_T.svg')
##tikzplotlib.save(Savedirect+'_kalterWintertag_T.tex')
##plt.savefig(Savedirect+'_kalterWintertag_T.pdf')
#plt.show()
#
#
#fig, ax = plt.subplots()
#ax.plot(np.array(Time), Sto_2[0][96:192]-273.15, label = '$T_{\mathrm{PS}}$')
#ax.plot(np.array(Time), TWW_2[0][96:192]-273.15, color='#4B81C4', label = '$T_{\mathrm{TWW}}$',linestyle='dashed')
#ax.set_xlabel('Zeit in h')
#ax.set_ylabel('$T$ in °C')
#ax.set_ylim(17,72)
#ax.set_yticks([20,35,50,65])
#plt.legend(loc='lower left')
#plt.savefig(Savedirect+'_Regentag_T.svg')
#tikzplotlib.save(Savedirect+'_Regentag_T.tex')
#plt.savefig(Savedirect+'_Regentag_T.pdf')
#plt.show()
#
#fig, ax = plt.subplots()
#ax.plot(np.array(Time), Sto_3[0][96:192]-273.15, label = '$T_{\mathrm{PS}}$')
#ax.plot(np.array(Time), TWW_3[0][96:192]-273.15, color='#4B81C4', label = '$T_{\mathrm{TWW}}$',linestyle='dashed')
#ax.set_xlabel('Zeit in h')
#ax.set_ylabel('$T$ in °C')
#ax.set_ylim(17,72)
#ax.set_yticks([20,35,50,65])
#plt.legend(loc='lower left', fontsize= 'medium')
#plt.savefig(Savedirect+'_Wintertag_T.svg')
#tikzplotlib.save(Savedirect+'_Wintertag_T.tex')
#plt.savefig(Savedirect+'_Wintertag_T.pdf')
#plt.show()
#
#fig, ax = plt.subplots()
#ax.plot(np.array(Time), Sto_4[0][96:192]-273.15, label = '$T_{\mathrm{PS}}$')
#ax.plot(np.array(Time), TWW_4[0][96:192]-273.15, color='#4B81C4', label ='$T_{\mathrm{TWW}}$', linestyle='dashed')
#ax.set_xlabel('Zeit in h')
#ax.set_ylabel('$T$ in °C')
#ax.set_ylim(17,72)
#ax.set_yticks([20,35,50,65])
#plt.legend(loc='upper left')
#plt.savefig(Savedirect+'_Fruehlingstag_T.svg')
#tikzplotlib.save(Savedirect+'_Fruehlingstag_T.tex')
#plt.savefig(Savedirect+'_Fruehlingstag_T.pdf')
#plt.show()
#
#fig, ax = plt.subplots()
#ax.plot(np.array(Time), Sto_5[0][96:192]-273.15, label = '$T_{\mathrm{PS}}$')
#ax.plot(np.array(Time), TWW_5[0][96:192]-273.15, color='#4B81C4', label = '$T_{\mathrm{TWW}}$', linestyle='dashed')
#ax.set_xlabel('Zeit in h')
#ax.set_ylabel('$T$ in °C')
#ax.set_ylim(17,72)
#ax.set_yticks([20,35,50,65])
#plt.legend(loc='right')
#plt.savefig(Savedirect+'_Hochsommertag_T.svg')
#tikzplotlib.save(Savedirect+'_Hochsommertag_T.tex')
#plt.savefig(Savedirect+'_Hochsommertag_T.pdf')
#plt.show()
#
#fig, ax = plt.subplots()
#ax.plot(np.array(Time), Sto_6[0][96:192]-273.15, label ='$T_{\mathrm{PS}}$')
#ax.set_xlabel('Zeit in h')
#ax.set_ylabel('$T$ in °C')
#ax.plot(np.array(Time), TWW_6[0][96:192]-273.15, color='#4B81C4', label = '$T_{\mathrm{TWW}}$', linestyle='dashed')
#ax.set_ylim(17,72)
#ax.set_yticks([20,35,50,65])
#plt.legend(loc='upper left')
#plt.savefig(Savedirect+'_Herbsttag_T.svg')
#tikzplotlib.save(Savedirect+'_Herbsttag_T.tex')
#plt.savefig(Savedirect+'_Herbsttag_T.pdf')
#plt.show()
#
#fig, ax = plt.subplots()
#ax.plot(np.array(Time), Sto_7[0][96:192]-273.15, label = '$T_{\mathrm{PS}}$')
#ax.plot(np.array(Time), TWW_7[0][96:192]-273.15, color='#4B81C4', label = '$T_{\mathrm{TWW}}$', linestyle='dashed')
#ax.set_xlabel('Zeit in h')
#ax.set_ylabel('$T$ in °C')
#ax.set_ylim(17,72)
#ax.set_yticks([20,35,50,65])
#plt.legend(loc='right')
#plt.savefig(Savedirect+'_Sommertag_T.svg')
#tikzplotlib.save(Savedirect+'_Sommertag_T.tex')
#plt.savefig(Savedirect+'_Sommertag_T.pdf')
##plt.show()
#
#fig, ax = plt.subplots()
#ax.plot(np.array(Time), Sto_8[0][96:192]-273.15, label='$T_{\mathrm{PS}}$')
#ax.plot(np.array(Time), TWW_8[0][96:192]-273.15, color='#4B81C4', label='$T_{\mathrm{TWW}}$', linestyle='dashed')
#ax.set_xlabel('Zeit in h')
#ax.set_ylabel('$T$ in °C')
#ax.set_ylim(17,72)
#ax.set_yticks([20,35,50,65])
#plt.legend(loc='lower left')
#plt.savefig(Savedirect+'_kuehlerHerbsttag_T.svg')
#tikzplotlib.save(Savedirect+'_kuehlerHerbsttag_T.tex')
#plt.savefig(Savedirect+'_kuehlerHerbsttag_T.pdf')
#plt.show()

#
#plt.rcParams.update(latex_fullpage)
#fig, ax= plt.subplots(8,1)
#ax[0].plot(np.array(Time), q_hp_1[0][96:192]*4/1000, label='$\dot{Q_{\mathrm{WP}}}$')
#ax2 = ax[0].twinx()
#ax[0].set_ylim(-0.500,10.5)
#ax[0].set_yticks(np.arange(0,12.500,5.000))
#ax[0].set_ylabel('$\dot{Q_{\mathrm{WP}}}$ in kW')
#ax2.set_yticks(np.arange(0,4,1))
#ax2.set_ylim(-0.15,3.15)
#ax2.set_ylabel('Modus')
#ax2.plot(np.array(Time), m_1[0][96:192], label='Modus', color='#4B81C4', drawstyle='steps', linestyle='dashed')
#ax[0].set_xticklabels([])
#ax[1].plot(np.array(Time), Sto_1[0][96:192]-273.15, label='$T_{\mathrm{PS}}$', color='#F49961', linestyle= 'dotted')
#ax[1].plot(np.array(Time), TWW_1[0][96:192]-273.15, label='$T_{\mathrm{TWW}}$', color='#8768B4',linestyle='dashdot')
#ax[1].set_ylabel('$T$ in °C')
#ax[1].set_ylim(17,72)
#ax[1].set_yticks([20,45,70])
#ax[1].set_xticklabels([])
#
#ax[2].plot(np.array(Time), q_hp_3[0][96:192]*4/1000, label='$\dot{Q_{\mathrm{WP}}}$')
#ax[2].plot(np.array(Time), m_3[0][96:192], label='Modus')
#ax2 = ax[2].twinx()
#ax[2].set_ylim(-0.500,10.5)
#ax[2].set_yticks(np.arange(0,12.500,5.000))
#ax[2].set_ylabel('$\dot{Q_{\mathrm{WP}}}$ in kW')
#ax2.set_yticks(np.arange(0,4,1))
#ax2.set_ylim(-0.15,3.15)
#ax2.set_ylabel('Modus')
#ax[3].plot(np.array(Time), Sto_3[0][96:192]-273.15, label='$T_{\mathrm{PS}}$', color='#F49961', linestyle= 'dotted')
#ax[3].plot(np.array(Time), TWW_3[0][96:192]-273.15, label='$T_{\mathrm{TWW}}$', color='#8768B4',linestyle='dashdot')
#ax[3].set_ylabel('$T$ in °C')
#ax[3].set_ylim(17,72)
#ax[3].set_yticks([20,45,70])
#ax[3].set_xticklabels([])
#ax[3].set_ylabel('$T$ in °C')
#ax[3].set_ylim(17,72)
#ax[3].set_yticks([20,45,70])
#ax[3].set_xticklabels([])
#
#ax[4].plot(np.array(Time), q_hp_2[0][96:192]*4/1000, label='$\dot{Q_{\mathrm{WP}}}$')
#ax[4].plot(np.array(Time), m_2[0][96:192], label='Modus')
#ax2 = ax[4].twinx()
#ax[4].set_ylim(-0.500,10.5)
#ax[4].set_yticks(np.arange(0,12.500,5.000))
#ax[4].set_ylabel('$\dot{Q_{\mathrm{WP}}}$ in kW')
#ax2.set_yticks(np.arange(0,4,1))
#ax2.set_ylim(-0.15,3.15)
#ax2.set_ylabel('Modus')
#ax[5].plot(np.array(Time), Sto_2[0][96:192]-273.15, label='$T_{\mathrm{PS}}$', color='#F49961', linestyle= 'dotted')
#ax[5].plot(np.array(Time), TWW_2[0][96:192]-273.15, label='$T_{\mathrm{TWW}}$', color='#8768B4',linestyle='dashdot')
#ax[5].set_ylabel('$T$ in °C')
#ax[5].set_ylim(17,72)
#ax[5].set_yticks([20,45,70])
#ax[5].set_xticklabels([])
#ax[5].set_ylabel('$T$ in °C')
#ax[5].set_ylim(17,72)
#ax[5].set_yticks([20,45,70])
#ax[5].set_xticklabels([])
#
#ax[6].plot(np.array(Time), q_hp_4[0][96:192]*4/1000, label='$\dot{Q_{\mathrm{WP}}}$')
#ax[6].plot(np.array(Time), m_4[0][96:192], label='Modus')
#ax2 = ax[6].twinx()
#ax[6].set_ylim(-0.500,10.5)
#ax[6].set_yticks(np.arange(0,12.500,5.000))
#ax[6].set_ylabel('$\dot{Q_{\mathrm{WP}}}$ in kW')
#ax2.set_yticks(np.arange(0,4,1))
#ax2.set_ylim(-0.15,3.15)
#ax2.set_ylabel('Modus')
#ax[7].plot(np.array(Time), Sto_4[0][96:192]-273.15, label='$T_{\mathrm{PS}}$', color='#F49961', linestyle= 'dotted')
#ax[7].plot(np.array(Time), TWW_4[0][96:192]-273.15, label='$T_{\mathrm{TWW}}$', color='#8768B4',linestyle='dashdot')
#ax[7].set_ylabel('$T$ in °C')
#ax[7].set_ylim(17,72)
#ax[7].set_yticks([20,45,70])
#ax[7].set_ylabel('$T$ in °C')
#ax[7].set_ylim(17,72)
#ax[7].set_yticks([20,45,70])
#ax[7].set_xlabel('Zeit in h')
#plt.subplots_adjust(hspace=0.1)
#
#plt.show()
#
#fig, axs = plt.subplots(4, 2, figsize=(10, 20))
## Erster Plot
#axs1 = axs[0, 0].twinx()
#axs[0, 0].plot(np.array(Time), q_hp_1[0][96:192]*4/1000, label='$\dot{Q_{\mathrm{WP}}}$')
#axs[0, 0].set_ylim(-0.500,10.5)
#axs[0, 0].set_yticks(np.arange(0,12.500,5.000))
#axs[0, 0].set_ylabel('$\dot{Q_{\mathrm{WP}}}$ in kW')
#axs1.set_yticks(np.arange(0,4,1))
#axs1.set_ylim(-0.15,3.15)
#axs1.set_ylabel('Modus')
#axs1.plot(np.array(Time), m_1[0][96:192], label='Modus', color='#4B81C4', drawstyle='steps', linestyle='dashed')
#axs[0, 0].set_xticklabels([])
#axs[0, 1].plot(np.array(Time), Sto_1[0][96:192]-273.15, label='$T_{\mathrm{PS}}$', color='#F49961', linestyle= 'dotted')
#axs[0, 1].plot(np.array(Time), TWW_1[0][96:192]-273.15, label='$T_{\mathrm{TWW}}$', color='#8768B4',linestyle='dashdot')
#axs[0, 1].set_ylabel('$T$ in °C')
#axs[0, 1].set_ylim(17,72)
#axs[0, 1].set_yticks([20,45,70])
#axs[0, 1].set_xticklabels([])
## Zweiter Plot
#axs2 = axs[1, 0].twinx()
#axs[1, 0].plot(np.array(Time), q_hp_3[0][96:192]*4/1000, label='$\dot{Q_{\mathrm{WP}}}$')
#axs[1, 0].set_ylim(-0.500,10.5)
#axs[1, 0].set_yticks(np.arange(0,12.500,5.000))
#axs[1, 0].set_ylabel('$\dot{Q_{\mathrm{WP}}}$ in kW')
#axs2.set_yticks(np.arange(0,4,1))
#axs2.set_ylim(-0.15,3.15)
#axs2.set_ylabel('Modus')
#axs[1, 0].plot(np.array(Time), m_3[0][96:192], label='Modus')
#axs[1, 1].plot(np.array(Time), Sto_3[0][96:192]-273.15, label='$T_{\mathrm{PS}}$', color='#F49961', linestyle= 'dotted')
#axs[1, 1].plot(np.array(Time), TWW_3[0][96:192]-273.15, label='$T_{\mathrm{TWW}}$', color='#8768B4',linestyle='dashdot')
#axs[1, 1].set_ylabel('$T$ in °C')
#axs[1, 1].set_ylim(17,72)
#axs[1, 1].set_yticks([20,45,70])
#axs[1, 1].set_xticklabels([])
#plt.show()


plt.rcParams.update(pp_figure)
#fig, axs = plt.subplots(2, 1)
#axs[0].plot(np.array(Time), q_hp_1[0][96:192]*4/1000, label='$\dot{Q}_{\mathrm{WP}}$')
#ax2 = axs[0].twinx()
#axs[0].set_ylim(-0.500,10.5)
#axs[0].set_yticks(np.arange(0,12.500,5.000))
#axs[0].set_ylabel('$\dot{Q}_{\mathrm{WP}}$ in kW')
#axs[0].set_title('kalter Wintertag', loc='left')
#ax2.set_yticks(np.arange(0,4,1))
#ax2.set_ylim(-0.15,3.15)
#ax2.set_ylabel('Modus')
#ax2.plot(np.array(Time), m_1[0][96:192], label='Modus', color='#4B81C4', drawstyle='steps', linestyle='dashed')
#axs[0].set_xticklabels([])
#axs[1].plot(np.array(Time), Sto_1[0][96:192]-273.15, label='$T_{\mathrm{PS}}$', color='#F49961', linestyle= 'dotted')
#axs[1].plot(np.array(Time), TWW_1[0][96:192]-273.15, label='$T_{\mathrm{TWW}}$', color='#8768B4',linestyle='dashdot')
#axs[1].set_ylabel('$T$ in °C')
#axs[1].set_ylim(17,72)
#axs[1].set_yticks([20,45,70])
#fig.legend(ncol=4, bbox_to_anchor=(0.95,1.0), fontsize='small', frameon=False)
#axs[1].set_xlabel('Zeit in h')
#plt.savefig(Savedirect+TRY+'_kalterWintertag.svg')
#tikzplotlib.save(Savedirect+TRY+'_kalterWintertag.tex')
#plt.savefig(Savedirect+TRY+'_kalterWintertag.pdf')
#plt.show()
###
#fig, axs = plt.subplots(2, 1)
#axs[0].plot(np.array(Time), q_hp_3[0][96:192]*4/1000, label='$\dot{Q}_{\mathrm{WP}}$')
#ax2 = axs[0].twinx()
#axs[0].set_ylim(-0.500,10.5)
#axs[0].set_yticks(np.arange(0,12.500,5.000))
#axs[0].set_ylabel('$\dot{Q}_{\mathrm{WP}}$ in kW')
#axs[0].set_title('Wintertag', loc='left')
#ax2.set_yticks(np.arange(0,4,1))
#ax2.set_ylim(-0.15,3.15)
#ax2.set_ylabel('Modus')
#ax2.plot(np.array(Time), m_3[0][96:192], label='Modus', color='#4B81C4', drawstyle='steps', linestyle='dashed')
#axs[0].set_xticklabels([])
#axs[1].plot(np.array(Time), Sto_3[0][96:192]-273.15, label='$T_{\mathrm{PS}}$', color='#F49961', linestyle= 'dotted')
#axs[1].plot(np.array(Time), TWW_3[0][96:192]-273.15, label='$T_{\mathrm{TWW}}$', color='#8768B4',linestyle='dashdot')
#axs[1].set_ylabel('$T$ in °C')
#axs[1].set_ylim(17,72)
#axs[1].set_yticks([20,45,70])
#axs[1].set_xlabel('Zeit in h')
#
#
#fig.legend(ncol=4, bbox_to_anchor=(0.95,1.0), fontsize='small', frameon=False)
#plt.savefig(Savedirect+TRY+'_Wintertag.svg')
#tikzplotlib.save(Savedirect+TRY+'_Wintertag.tex')
#plt.savefig(Savedirect+TRY+'_Wintertag.pdf')
#plt.show()
###
#fig, axs = plt.subplots(2, 1)
#axs[0].plot(np.array(Time), q_hp_2[0][96:192]*4/1000, label='$\dot{Q}_{\mathrm{WP}}$')
#ax2 = axs[0].twinx()
#axs[0].set_ylim(-0.500,10.5)
#axs[0].set_yticks(np.arange(0,12.500,5.000))
#axs[0].set_ylabel('$\dot{Q}_{\mathrm{WP}}$ in kW')
#axs[0].set_title('bewölkter Tag', loc='left')
#ax2.set_yticks(np.arange(0,4,1))
#ax2.set_ylim(-0.15,3.15)
#ax2.set_ylabel('Modus')
#ax2.plot(np.array(Time), m_2[0][96:192], label='Modus', color='#4B81C4', drawstyle='steps', linestyle='dashed')
#axs[0].set_xticklabels([])
#axs[1].plot(np.array(Time), Sto_2[0][96:192]-273.15, label='$T_{\mathrm{PS}}$', color='#F49961', linestyle= 'dotted')
#axs[1].plot(np.array(Time), TWW_2[0][96:192]-273.15, label='$T_{\mathrm{TWW}}$', color='#8768B4',linestyle='dashdot')
#axs[1].set_ylabel('$T$ in °C')
#axs[1].set_ylim(17,72)
#axs[1].set_yticks([20,45,70])
#axs[1].set_label('Zeit in h')
#fig.legend(ncol=4, bbox_to_anchor=(0.95,1.0), fontsize='small', frameon=False)
#axs[1].set_xlabel('Zeit in h')
#plt.savefig(Savedirect+TRY+'_Regentag.svg')
#tikzplotlib.save(Savedirect+TRY+'_Regentag.tex')
#plt.savefig(Savedirect+TRY+'_Regentag.pdf')
#plt.show()
###
###
#fig, axs = plt.subplots(2, 1)
#axs[0].plot(np.array(Time), q_hp_4[0][96:192]*4/1000, label='$\dot{Q}_{\mathrm{WP}}}$')
#ax2 = axs[0].twinx()
#axs[0].set_ylim(-0.500,10.5)
#axs[0].set_yticks(np.arange(0,12.500,5.000))
#axs[0].set_ylabel('$\dot{Q}_{\mathrm{WP}}}$ in kW')
#axs[0].set_title('Übergangstag 1', loc='left')
#axs[0].set_xticklabels([])
#ax2.set_yticks(np.arange(0,4,1))
#ax2.set_ylim(-0.15,3.15)
#ax2.set_ylabel('Modus')
#ax2.plot(np.array(Time), m_4[0][96:192], label='Modus', color='#4B81C4', drawstyle='steps', linestyle='dashed')
#axs[1].plot(np.array(Time), Sto_4[0][96:192]-273.15, label='$T_{\mathrm{PS}}$', color='#F49961', linestyle= 'dotted')
#axs[1].plot(np.array(Time), TWW_4[0][96:192]-273.15, label='$T_{\mathrm{TWW}}$', color='#8768B4',linestyle='dashdot')
#axs[1].set_ylabel('$T$ in °C')
#axs[1].set_ylim(17,72)
#axs[1].set_yticks([20,45,70])
#axs[1].set_xlabel('Zeit in h')
#fig.legend(ncol=4, bbox_to_anchor=(0.95,1.0), fontsize='small', frameon=False)
#plt.savefig(Savedirect+TRY+'_Fruehlingstag.svg')
#tikzplotlib.save(Savedirect+TRY+'_Fruehlingstag.tex')
#plt.savefig(Savedirect+TRY+'_Fruehlingstag.pdf')
#plt.show()
####
#fig, axs = plt.subplots(2, 1)
#axs[0].plot(np.array(Time), q_hp_7[0][96:192]*4/1000, label='$\dot{Q}_{\mathrm{WP}}$')
#ax2 = axs[0].twinx()
#axs[0].set_ylim(-0.500,10.5)
#axs[0].set_yticks(np.arange(0,12.500,5.000))
#axs[0].set_ylabel('$\dot{Q}_{\mathrm{WP}}$ in kW')
#axs[0].set_title('Sommertag', loc='left')
#ax2.set_yticks(np.arange(0,4,1))
#ax2.set_ylim(-0.15,3.15)
#ax2.set_ylabel('Modus')
#ax2.plot(np.array(Time), m_7[0][96:192], label='Modus', color='#4B81C4', drawstyle='steps', linestyle='dashed')
#axs[0].set_xticklabels([])
#axs[1].plot(np.array(Time), Sto_7[0][96:192]-273.15, label='$T_{\mathrm{PS}}$', color='#F49961', linestyle= 'dotted')
#axs[1].plot(np.array(Time), TWW_7[0][96:192]-273.15, label='$T_{\mathrm{TWW}}$', color='#8768B4',linestyle='dashdot')
#axs[1].set_ylabel('$T$ in °C')
#axs[1].set_ylim(17,72)
#axs[1].set_yticks([20,45,70])
#axs[1].set_xlabel('Zeit in h')
#fig.legend(ncol=4, bbox_to_anchor=(0.95,1.0), fontsize='small', frameon=False)
#plt.savefig(Savedirect+TRY+'_Sommertag.svg')
#tikzplotlib.save(Savedirect+TRY+'_Sommertag.tex')
#plt.savefig(Savedirect+TRY+'_Sommertag.pdf')
#plt.show()
###
###
#fig, axs = plt.subplots(2, 1)
#axs[0].plot(np.array(Time), q_hp_5[0][96:192]*4/1000, label='$\dot{Q}_{\mathrm{WP}}$')
#ax2 = axs[0].twinx()
#axs[0].set_ylim(-0.500,10.5)
#axs[0].set_yticks(np.arange(0,12.500,5.000))
#axs[0].set_ylabel('$\dot{Q}_{\mathrm{WP}}$ in kW')
#axs[0].set_title('Hochsommertag', loc='left')
#ax2.set_yticks(np.arange(0,4,1))
#ax2.set_ylim(-0.15,3.15)
#ax2.set_ylabel('Modus')
#ax2.plot(np.array(Time), m_5[0][96:192], label='Modus', color='#4B81C4', drawstyle='steps', linestyle='dashed')
#axs[0].set_xticklabels([])
#axs[1].plot(np.array(Time), Sto_5[0][96:192]-273.15, label='$T_{\mathrm{PS}}$', color='#F49961', linestyle= 'dotted')
#axs[1].plot(np.array(Time), TWW_5[0][96:192]-273.15, label='$T_{\mathrm{TWW}}$', color='#8768B4',linestyle='dashdot')
#axs[1].set_ylabel('$T$ in °C')
#axs[1].set_ylim(17,72)
#axs[1].set_yticks([20,45,70])
#axs[1].set_xlabel('Zeit in h')
#fig.legend(ncol=4, bbox_to_anchor=(0.95,1.0), fontsize='small', frameon=False)
#plt.savefig(Savedirect+TRY+'_Hochsommertag.svg')
#tikzplotlib.save(Savedirect+TRY+'_Hochsommertag.tex')
#plt.savefig(Savedirect+TRY+'_Hochsommertag.pdf')
#plt.show()
###
###
#fig, axs = plt.subplots(2, 1)
#axs[0].plot(np.array(Time), q_hp_6[0][96:192]*4/1000, label='$\dot{Q}_{\mathrm{WP}}$')
#ax2 = axs[0].twinx()
#axs[0].set_ylim(-0.500,10.5)
#axs[0].set_yticks(np.arange(0,12.500,5.000))
#axs[0].set_ylabel('$\dot{Q}_{\mathrm{WP}}$ in kW')
#axs[0].set_title('Übergangstag 2', loc='left')
#ax2.set_yticks(np.arange(0,4,1))
#ax2.set_ylim(-0.15,3.15)
#ax2.set_ylabel('Modus')
#ax2.plot(np.array(Time), m_6[0][96:192], label='Modus', color='#4B81C4', drawstyle='steps', linestyle='dashed')
#axs[0].set_xticklabels([])
#axs[1].plot(np.array(Time), Sto_6[0][96:192]-273.15, label='$T_{\mathrm{PS}}$', color='#F49961', linestyle= 'dotted')
#axs[1].plot(np.array(Time), TWW_6[0][96:192]-273.15, label='$T_{\mathrm{TWW}}$', color='#8768B4',linestyle='dashdot')
#axs[1].set_ylabel('$T$ in °C')
#axs[1].set_ylim(17,72)
#axs[1].set_yticks([20,45,70])
#axs[1].set_xlabel('Zeit in h')
#fig.legend(ncol=4, bbox_to_anchor=(0.95,1.0), fontsize='small', frameon=False)
#plt.savefig(Savedirect+TRY+'_Herbsttag.svg')
#tikzplotlib.save(Savedirect+TRY+'_Herbsttag.tex')
#plt.savefig(Savedirect+TRY+'_Herbsttag.pdf')
#plt.show()
###
###
#fig, axs = plt.subplots(2, 1)
#axs[0].plot(np.array(Time), q_hp_8[0][96:192]*4/1000, label='$\dot{Q}_{\mathrm{WP}}$')
#ax2 = axs[0].twinx()
#axs[0].set_ylim(-0.500,10.5)
#axs[0].set_yticks(np.arange(0,12.500,5.000))
#axs[0].set_ylabel('$\dot{Q}_{\mathrm{WP}}$ in kW')
#axs[0].set_title('bewölkter Übergangstag', loc='left')
#axs[0].set_xticklabels([])
#ax2.set_yticks(np.arange(0,4,1))
#ax2.set_ylim(-0.15,3.15)
#ax2.set_ylabel('Modus')
#ax2.plot(np.array(Time), m_8[0][96:192], label='Modus', color='#4B81C4', drawstyle='steps', linestyle='dashed')
#axs[1].plot(np.array(Time), Sto_8[0][96:192]-273.15, label='$T_{\mathrm{PS}}$', color='#F49961', linestyle= 'dotted')
#axs[1].plot(np.array(Time), TWW_8[0][96:192]-273.15, label='$T_{\mathrm{TWW}}$', color='#8768B4',linestyle='dashdot')
#axs[1].set_ylabel('$T$ in °C')
#axs[1].set_ylim(17,72)
#axs[1].set_yticks([20,45,70])
#axs[1].set_xlabel('Zeit in h')
#fig.legend(ncol=4, bbox_to_anchor=(1.01,1.0), fontsize='small', frameon=False)
#plt.savefig(Savedirect+TRY+'_kuehlerHerbsttag.svg')
#tikzplotlib.save(Savedirect+TRY+'_kuehlerHerbsttag.tex')
#plt.savefig(Savedirect+TRY+'_kuehlerHerbsttag.pdf')
#plt.show()
###
#q_hou = []
#p_pv = []
#p_el = []
#t_air = []

################################## Read data for TRY optimization to create the plots for TRY-Data ####################
df = pd.read_csv(Directory + Data + '0_025_8736_4_24_TRY_normal_Fix_TWW_Small_Norm.csv', header=None,
                 names=['T_Air', 'Q_Hou', 'P_PV', 'P_EL_Dem', 'T_Mean', 'c_grid', 'Q_TWW', 'T_Sto', 'T_TWW', 'COP_1',
                        'COP_2', 'Q_HP', 'Q_Penalty'])
#q_hou.append(df['Q_Hou'])
#p_pv.append(df['P_PV'])
#p_el.append(df['P_EL_Dem'])
#t_air.append(df['T_Air'])
mf = pd.read_csv(Directory + Mode + '0_025_8736_4_24_TRY_normal_Fix_TWW_Small_Norm.csv', header=None, names=['Modes'])
q_hp_w.append(df['Q_HP'])
Sto_w.append(df['T_Sto'])
TWW_w.append(df['T_TWW'])
m_w.append(mf['Modes'])
q_hou_w.append(df['Q_Hou'])
pv_w.append(df['P_PV'])
#print(len(m_w))
#print(len(q_hou[0]))
##
print(q_hou_w)

plt.rcParams.update(pp_figure)
#fig, axs = plt.subplots(3, 1)
#axs[0].plot(np.array(Time), q_hp_w[0][1344:1632]*4/1000, label='$\dot{Q}_{\mathrm{WP}}$', color=colors[("blue", 100)])
#ax2 = axs[0].twinx()
#axs[0].set_ylim(-0.500,10.5)
#axs[0].set_yticks(np.arange(0,12.500,5.000))
#axs[0].set_ylabel('$\dot{Q}_{\mathrm{WP}}$ in kW')
#axs[0].set_title('-', loc='left')
#axs[0].set_xticks(np.arange(12,84,24))
#ax2.set_yticks(np.arange(0,4,1))
#ax2.set_ylim(-0.15,3.15)
#ax2.set_ylabel('Modus')
#ax2.plot(np.array(Time), m_w[0][1344:1632], label='Modus', drawstyle='steps', color=colors[("red", 100)])#, drawstyle='steps', linestyle='dashed')
#axs[0].set_xticklabels([])
#axs[1].plot(np.array(Time), Sto_w[0][1344:1632]-273.15, label='$T_{\mathrm{PS}}$', color=colors[("orange", 100)])#, color='#F49961'), linestyle= 'dotted')
#axs[1].plot(np.array(Time), TWW_w[0][1344:1632]-273.15, label='$T_{\mathrm{TWW}}$', color=colors[("turqoise", 100)])
#axs[1].set_ylabel('$T$ in °C')
#axs[1].set_ylim(17,72)
#axs[1].set_yticks([20,45,70])
#xticks_labels = ['14.1', '15.1', '16.1']  # labels of the ticks
#axs[1].set_xticks(np.arange(12,84,24))
#axs[1].set_xticklabels([])
#axs[2].set_xticks(np.arange(12,84,24))
#axs[2].set_xticklabels(xticks_labels)
#axs[2].set_xlabel('Zeit in d')
#axs[2].plot(np.array(Time), q_hou_w[0][1344:1632]*4/1000, label='$\dot{Q}_{\mathrm{Haus}}$',color=colors[("green", 100)])
#ax3 = axs[2].twinx()
#ax3.plot(np.array(Time), pv_w[0][1344:1632]*4/1000, label='$P_{\mathrm{PV}}$',color=colors[("bordeaux", 100)])
#ax3.set_ylim(-0.15,6.15)
#ax3.set_ylabel('$P_\mathrm{PV}$ in kW')
#axs[2].set_ylim(-0.500,10.5)
#axs[2].set_yticks(np.arange(0,11.500,5.000))
#axs[2].set_ylabel('$\dot{Q}_{\mathrm{Haus}}$ in kW')


fig, axs = plt.subplots(3, 1)
axs[0].plot(np.array(Time), q_hp_w[0][1344:1632]*4/1000, label='$\dot{Q}_{\mathrm{WP}}$', color=colors[("red", 100)])
ax2 = axs[0].twinx()
axs[0].set_ylim(-0.500,10.5)
axs[0].set_yticks(np.arange(0,12.500,5.000))
axs[0].set_ylabel('$\dot{Q}_{\mathrm{WP}}$ in kW')
axs[0].set_title('$~$', loc='left')
axs[0].set_xticks(np.arange(12,84,24))
ax2.set_yticks(np.arange(0,4,1))
ax2.set_ylim(-0.15,3.15)
ax2.set_ylabel('Modus')
ax2.plot(np.array(Time), m_w[0][1344:1632], label='Modus', drawstyle='steps', color=colors[("blue", 75)])#, drawstyle='steps', linestyle='dashed')
axs[0].set_xticklabels([])
axs[1].plot(np.array(Time), Sto_w[0][1344:1632]-273.15, label='$T_{\mathrm{PS}}$', color=colors[("orange", 100)])#, color='#F49961'), linestyle= 'dotted')
axs[1].plot(np.array(Time), TWW_w[0][1344:1632]-273.15, label='$T_{\mathrm{TWW}}$', color=colors[("turqoise", 100)])
axs[1].set_ylabel('$T$ in °C')
axs[1].set_ylim(17,72)
axs[1].set_yticks([20,45,70])
xticks_labels = ['14.1', '15.1', '16.1']  # labels of the ticks
axs[1].set_xticks(np.arange(12,84,24))
axs[1].set_xticklabels([])
axs[2].set_xticks(np.arange(12,84,24))
axs[2].set_xticklabels(xticks_labels)
axs[2].set_xlabel('Zeit in d')
axs[2].plot(np.array(Time), q_hou_w[0][1344:1632]*4/1000, label='$\dot{Q}_{\mathrm{Haus}}$',color=colors[("green", 100)])
ax3 = axs[2].twinx()
ax3.plot(np.array(Time), pv_w[0][1344:1632]*4/1000, label='$P_{\mathrm{PV}}$',color=colors[("bordeaux", 100)])
ax3.set_ylim(-0.15,6.15)
ax3.set_ylabel('$P_\mathrm{PV}$ in kW')
axs[2].set_ylim(-0.500,10.5)
axs[2].set_yticks(np.arange(0,11.500,5.000))
axs[2].set_ylabel('$\dot{Q}_{\mathrm{Haus}}$ in kW')
legend_handles = [
    plt.Line2D([], [], color=colors[("red", 100)]),
    plt.Line2D([], [], color=colors[("blue", 75)]),
    plt.Line2D([], [], color=colors[("orange", 100)]),
    plt.Line2D([], [], color=colors[("turqoise", 100)]),
    plt.Line2D([], [], color=colors[("green", 100)]),
    plt.Line2D([], [], color=colors[("bordeaux", 100)])
]
legend_labels = ['$\dot{Q}_{\mathrm{WP}}$', 'Modus', '$T_{\mathrm{PS}}$', '$T_{\mathrm{TWW}}$', '$\dot{Q}_{\mathrm{Haus}}$', '$P_{\mathrm{PV}}$']
fig.legend(legend_handles, legend_labels, ncol=6, bbox_to_anchor=(0.95, 1.025), fontsize='small', frameon=False)
axs[1].axvspan(0, 24, color='grey', alpha=0.2)
axs[2].axvspan(0, 24, color='grey', alpha=0.2)
axs[0].axvspan(0, 24, color='grey', alpha=0.2)
axs[1].axvspan(48, 72, color='grey', alpha=0.2)
axs[0].axvspan(48, 72, color='grey', alpha=0.2)
axs[2].axvspan(48, 72, color='grey', alpha=0.2)
plt.savefig(Savedirect+'_TRY_norm_JanWoche.svg')
tikzplotlib.save(Savedirect+'_TRY_norm_JanWoche.tex')
plt.savefig(Savedirect+'_TRY_norm_JanWoche.pdf')
plt.savefig(Savedirect+'_TRY_norm_JanWoche.png')
plt.show()

##
fig, axs = plt.subplots(3, 1)
axs[0].plot(np.array(Time), q_hp_w[0][8640:8928]*4/1000, label='$\dot{Q}_{\mathrm{WP}}$', color=colors[("red", 100)])
ax2 = axs[0].twinx()
axs[0].set_ylim(-0.500,10.5)
axs[0].set_yticks(np.arange(0,12.500,5.000))
axs[0].set_ylabel('$\dot{Q}_{\mathrm{WP}}$ in kW')
axs[0].set_title('$~$', loc='left')
axs[0].set_xticks(np.arange(12,84,24))
ax2.set_yticks(np.arange(0,4,1))
ax2.set_ylim(-0.15,3.15)
ax2.set_ylabel('Modus')
ax2.plot(np.array(Time), m_w[0][8640:8928], label='Modus', drawstyle='steps', color=colors[("blue", 75)])#, drawstyle='steps', linestyle='dashed')
axs[0].set_xticklabels([])
axs[1].plot(np.array(Time), Sto_w[0][8640:8928]-273.15, label='$T_{\mathrm{PS}}$', color=colors[("orange", 100)])#, color='#F49961'), linestyle= 'dotted')
axs[1].plot(np.array(Time), TWW_w[0][8640:8928]-273.15, label='$T_{\mathrm{TWW}}$', color=colors[("turqoise", 100)])
axs[1].set_ylabel('$T$ in °C')
axs[1].set_ylim(17,72)
axs[1].set_yticks([20,45,70])
xticks_labels = ['1.4', '2.4', '3.4']  # labels of the ticks
axs[1].set_xticks(np.arange(12,84,24))
axs[1].set_xticklabels([])
axs[2].set_xticks(np.arange(12,84,24))
axs[2].set_xticklabels(xticks_labels)
axs[2].set_xlabel('Zeit in d')
axs[2].plot(np.array(Time), q_hou_w[0][8640:8928]*4/1000, label='$\dot{Q}_{\mathrm{Haus}}$',color=colors[("green", 100)])
ax3 = axs[2].twinx()
ax3.plot(np.array(Time), pv_w[0][8640:8928]*4/1000, label='$P_{\mathrm{PV}}$',color=colors[("bordeaux", 100)])
ax3.set_ylim(-0.15,6.15)
ax3.set_ylabel('$P_\mathrm{PV}$ in kW')
axs[2].set_ylim(-0.500,10.5)
axs[2].set_yticks(np.arange(0,11.500,5.000))
axs[2].set_ylabel('$\dot{Q}_{\mathrm{Haus}}$ in kW')
legend_handles = [
    plt.Line2D([], [], color=colors[("red", 100)]),
    plt.Line2D([], [], color=colors[("blue", 75)]),
    plt.Line2D([], [], color=colors[("orange", 100)]),
    plt.Line2D([], [], color=colors[("turqoise", 100)]),
    plt.Line2D([], [], color=colors[("green", 100)]),
    plt.Line2D([], [], color=colors[("bordeaux", 100)])
]
legend_labels = ['$\dot{Q}_{\mathrm{WP}}$', 'Modus', '$T_{\mathrm{PS}}$', '$T_{\mathrm{TWW}}$', '$\dot{Q}_{\mathrm{Haus}}$', '$P_{\mathrm{PV}}$']
fig.legend(legend_handles, legend_labels, ncol=6, bbox_to_anchor=(0.95, 1.025), fontsize='small', frameon=False)
axs[1].axvspan(0, 24, color='grey', alpha=0.2)
axs[2].axvspan(0, 24, color='grey', alpha=0.2)
axs[0].axvspan(0, 24, color='grey', alpha=0.2)
axs[1].axvspan(48, 72, color='grey', alpha=0.2)
axs[0].axvspan(48, 72, color='grey', alpha=0.2)
axs[2].axvspan(48, 72, color='grey', alpha=0.2)
plt.savefig(Savedirect+'_TRY_norm_AprWoche.png')
plt.show()







fig, axs = plt.subplots(3, 1)
axs[0].plot(np.array(Time), q_hp_w[0][17376:17664]*4/1000, label='$\dot{Q}_{\mathrm{WP}}$', color=colors[("red", 100)])
ax2 = axs[0].twinx()
axs[0].set_ylim(-0.500,10.5)
axs[0].set_yticks(np.arange(0,12.500,5.000))
axs[0].set_ylabel('$\dot{Q}_{\mathrm{WP}}$ in kW')
axs[0].set_title('$~$', loc='left')
axs[0].set_xticks(np.arange(12,84,24))
ax2.set_yticks(np.arange(0,4,1))
ax2.set_ylim(-0.15,3.15)
ax2.set_ylabel('Modus')
ax2.plot(np.array(Time), m_w[0][17376:17664], label='Modus', drawstyle='steps', color=colors[("blue", 75)])#, drawstyle='steps', linestyle='dashed')
axs[0].set_xticklabels([])
axs[1].plot(np.array(Time), Sto_w[0][17376:17664]-273.15, label='$T_{\mathrm{PS}}$', color=colors[("orange", 100)])#, color='#F49961'), linestyle= 'dotted')
axs[1].plot(np.array(Time), TWW_w[0][17376:17664]-273.15, label='$T_{\mathrm{TWW}}$', color=colors[("turqoise", 100)])
axs[1].set_ylabel('$T$ in °C')
axs[1].set_ylim(17,72)
axs[1].set_yticks([20,45,70])
xticks_labels = ['1.7', '2.7', '3.7']  # labels of the ticks
axs[1].set_xticks(np.arange(12,84,24))
axs[1].set_xticklabels([])
axs[2].set_xticks(np.arange(12,84,24))
axs[2].set_xticklabels(xticks_labels)
axs[2].set_xlabel('Zeit in d')
axs[2].plot(np.array(Time), q_hou_w[0][17376:17664]*4/1000, label='$\dot{Q}_{\mathrm{Haus}}$',color=colors[("green", 100)])
ax3 = axs[2].twinx()
ax3.plot(np.array(Time), pv_w[0][17376:17664]*4/1000, label='$P_{\mathrm{PV}}$',color=colors[("bordeaux", 100)])
ax3.set_ylim(-0.15,6.15)
ax3.set_ylabel('$P_\mathrm{PV}$ in kW')
axs[2].set_ylim(-0.500,10.5)
axs[2].set_yticks(np.arange(0,11.500,5.000))
axs[2].set_ylabel('$\dot{Q}_{\mathrm{Haus}}$ in kW')
legend_handles = [
    plt.Line2D([], [], color=colors[("red", 100)]),
    plt.Line2D([], [], color=colors[("blue", 75)]),
    plt.Line2D([], [], color=colors[("orange", 100)]),
    plt.Line2D([], [], color=colors[("turqoise", 100)]),
    plt.Line2D([], [], color=colors[("green", 100)]),
    plt.Line2D([], [], color=colors[("bordeaux", 100)])
]
legend_labels = ['$\dot{Q}_{\mathrm{WP}}$', 'Modus', '$T_{\mathrm{PS}}$', '$T_{\mathrm{TWW}}$', '$\dot{Q}_{\mathrm{Haus}}$', '$P_{\mathrm{PV}}$']
fig.legend(legend_handles, legend_labels, ncol=6, bbox_to_anchor=(0.95, 1.025), fontsize='small', frameon=False)
axs[1].axvspan(0, 24, color='grey', alpha=0.2)
axs[2].axvspan(0, 24, color='grey', alpha=0.2)
axs[0].axvspan(0, 24, color='grey', alpha=0.2)
axs[1].axvspan(48, 72, color='grey', alpha=0.2)
axs[0].axvspan(48, 72, color='grey', alpha=0.2)
axs[2].axvspan(48, 72, color='grey', alpha=0.2)
plt.savefig(Savedirect+'_TRY_norm_JulWoche.svg')
tikzplotlib.save(Savedirect+'_TRY_norm_JulWoche.tex')
plt.savefig(Savedirect+'_TRY_norm_JulWoche.pdf')
plt.savefig(Savedirect+'_TRY_norm_JulWoche.png')

plt.show()


fig, axs = plt.subplots(3, 1)
axs[0].plot(np.array(Time), q_hp_w[0][26208:26496]*4/1000, label='$\dot{Q}_{\mathrm{WP}}$', color=colors[("red", 100)])
ax2 = axs[0].twinx()
axs[0].set_ylim(-0.500,10.5)
axs[0].set_yticks(np.arange(0,12.500,5.000))
axs[0].set_ylabel('$\dot{Q}_{\mathrm{WP}}$ in kW')
axs[0].set_title('$~$', loc='left')
axs[0].set_xticks(np.arange(12,84,24))
ax2.set_yticks(np.arange(0,4,1))
ax2.set_ylim(-0.15,3.15)
ax2.set_ylabel('Modus')
ax2.plot(np.array(Time), m_w[0][26208:26496], label='Modus', drawstyle='steps', color=colors[("blue", 75)])#, drawstyle='steps', linestyle='dashed')
axs[0].set_xticklabels([])
axs[1].plot(np.array(Time), Sto_w[0][26208:26496]-273.15, label='$T_{\mathrm{PS}}$', color=colors[("orange", 100)])#, color='#F49961'), linestyle= 'dotted')
axs[1].plot(np.array(Time), TWW_w[0][26208:26496]-273.15, label='$T_{\mathrm{TWW}}$', color=colors[("turqoise", 100)])
axs[1].set_ylabel('$T$ in °C')
axs[1].set_ylim(17,72)
axs[1].set_yticks([20,45,70])
xticks_labels = ['1.10', '2.10', '3.10']  # labels of the ticks
axs[1].set_xticks(np.arange(12,84,24))
axs[1].set_xticklabels([])
axs[2].set_xticks(np.arange(12,84,24))
axs[2].set_xticklabels(xticks_labels)
axs[2].set_xlabel('Zeit in d')
axs[2].plot(np.array(Time), q_hou_w[0][26208:26496]*4/1000, label='$\dot{Q}_{\mathrm{Haus}}$',color=colors[("green", 100)])
ax3 = axs[2].twinx()
ax3.plot(np.array(Time), pv_w[0][26208:26496]*4/1000, label='$P_{\mathrm{PV}}$',color=colors[("bordeaux", 100)])
ax3.set_ylim(-0.15,6.15)
ax3.set_ylabel('$P_\mathrm{PV}$ in kW')
axs[2].set_ylim(-0.500,10.5)
axs[2].set_yticks(np.arange(0,11.500,5.000))
axs[2].set_ylabel('$\dot{Q}_{\mathrm{Haus}}$ in kW')
legend_handles = [
    plt.Line2D([], [], color=colors[("red", 100)]),
    plt.Line2D([], [], color=colors[("blue", 75)]),
    plt.Line2D([], [], color=colors[("orange", 100)]),
    plt.Line2D([], [], color=colors[("turqoise", 100)]),
    plt.Line2D([], [], color=colors[("green", 100)]),
    plt.Line2D([], [], color=colors[("bordeaux", 100)])
]
legend_labels = ['$\dot{Q}_{\mathrm{WP}}$', 'Modus', '$T_{\mathrm{PS}}$', '$T_{\mathrm{TWW}}$', '$\dot{Q}_{\mathrm{Haus}}$', '$P_{\mathrm{PV}}$']
fig.legend(legend_handles, legend_labels, ncol=6, bbox_to_anchor=(0.95, 1.025), fontsize='small', frameon=False)
axs[1].axvspan(0, 24, color='grey', alpha=0.2)
axs[2].axvspan(0, 24, color='grey', alpha=0.2)
axs[0].axvspan(0, 24, color='grey', alpha=0.2)
axs[1].axvspan(48, 72, color='grey', alpha=0.2)
axs[0].axvspan(48, 72, color='grey', alpha=0.2)
axs[2].axvspan(48, 72, color='grey', alpha=0.2)
plt.savefig(Savedirect+'_TRY_norm_OktWoche.png')
plt.show()


#fig, axs = plt.subplots(2, 1)
#axs[0].plot(np.array(Time), q_hp_w[0][8640:8928]*4/1000, label='$\dot{Q}_{\mathrm{WP}}$')
#ax2 = axs[0].twinx()
#axs[0].set_ylim(-0.500,10.5)
#axs[0].set_yticks(np.arange(0,12.500,5.000))
#axs[0].set_ylabel('$\dot{Q}_{\mathrm{WP}}$ in kW')
#axs[0].set_title('April', loc='left')
#axs[0].set_xticks(np.arange(12,84,24))
#ax2.set_yticks(np.arange(0,4,1))
#ax2.set_ylim(-0.15,3.15)
#ax2.set_ylabel('Modus')
#ax2.plot(np.array(Time), m_w[0][8640:8928], label='Modus', color='#4B81C4', drawstyle='steps', linestyle='dashed')
#axs[0].set_xticklabels([])
#axs[1].plot(np.array(Time), Sto_w[0][8640:8928]-273.15, label='$T_{\mathrm{PS}}$', color='#F49961', linestyle= 'dotted')
#axs[1].plot(np.array(Time), TWW_w[0][8640:8928]-273.15, label='$T_{\mathrm{TWW}}$', color='#8768B4',linestyle='dashdot')
#axs[1].set_ylabel('$T$ in °C')
#axs[1].set_ylim(17,72)
#axs[1].set_yticks([20,45,70])
#fig.legend(ncol=4, bbox_to_anchor=(0.95,1.0), fontsize='small', frameon=False)
#xticks_labels = ['1.4', '2.4', '3.4']  # labels of the ticks
#axs[1].set_xticks(np.arange(12,84,24))
#axs[1].set_xticklabels(xticks_labels)
#axs[1].set_xlabel('Zeit in d')
#axs[1].axvspan(0, 24, color='grey', alpha=0.2)
#axs[0].axvspan(0, 24, color='grey', alpha=0.2)
#axs[1].axvspan(48, 72, color='grey', alpha=0.2)
#axs[0].axvspan(48, 72, color='grey', alpha=0.2)
#plt.savefig(Savedirect+'_TRY_norm_AprWoche.svg')
#tikzplotlib.save(Savedirect+'_TRY_norm_AprWoche.tex')
#plt.savefig(Savedirect+'_TRY_norm_AprWoche.pdf')
#plt.show()
##
#plt.rcParams.update(pp_figure)
#fig, axs = plt.subplots(2, 1)
#axs[0].plot(np.array(Time), q_hp_w[0][17376:17664]*4/1000, label='$\dot{Q}_{\mathrm{WP}}$')
#ax2 = axs[0].twinx()
#axs[0].set_ylim(-0.500,10.5)
#axs[0].set_yticks(np.arange(0,12.500,5.000))
#axs[0].set_ylabel('$\dot{Q}_{\mathrm{WP}}$ in kW')
#axs[0].set_title('Juli', loc='left')
#axs[0].set_xticks(np.arange(12,84,24))
#ax2.set_yticks(np.arange(0,4,1))
#ax2.set_ylim(-0.15,3.15)
#ax2.set_ylabel('Modus')
#ax2.plot(np.array(Time), m_w[0][17376:17664], label='Modus', color='#4B81C4', drawstyle='steps', linestyle='dashed')
#axs[0].set_xticklabels([])
#axs[1].plot(np.array(Time), Sto_w[0][17376:17664]-273.15, label='$T_{\mathrm{PS}}$', color='#F49961', linestyle= 'dotted')
#axs[1].plot(np.array(Time), TWW_w[0][17376:17664]-273.15, label='$T_{\mathrm{TWW}}$', color='#8768B4',linestyle='dashdot')
#axs[1].set_ylabel('$T$ in °C')
#axs[1].set_ylim(17,72)
#axs[1].set_yticks([20,45,70])
#fig.legend(ncol=4, bbox_to_anchor=(0.95,1.0), fontsize='small', frameon=False)
#xticks_labels = ['1.7', '2.7', '3.7']  # labels of the ticks
#axs[1].set_xticks(np.arange(12,84,24))
#axs[1].set_xticklabels(xticks_labels)
#axs[1].set_xlabel('Zeit in d')
#axs[1].axvspan(0, 24, color='grey', alpha=0.2)
#axs[0].axvspan(0, 24, color='grey', alpha=0.2)
#axs[1].axvspan(48, 72, color='grey', alpha=0.2)
#axs[0].axvspan(48, 72, color='grey', alpha=0.2)
#plt.savefig(Savedirect+'_TRY_norm_JulWoche.svg')
#tikzplotlib.save(Savedirect+'_TRY_norm_JulWoche.tex')
#plt.savefig(Savedirect+'_TRY_norm_JulWoche.pdf')
#plt.show()
##
#fig, axs = plt.subplots(2, 1)
#axs[0].plot(np.array(Time), q_hp_w[0][26208:26496]*4/1000, label='$\dot{Q}_{\mathrm{WP}}$')
#ax2 = axs[0].twinx()
#axs[0].set_ylim(-0.500,10.5)
#axs[0].set_yticks(np.arange(0,12.500,5.000))
#axs[0].set_ylabel('$\dot{Q}_{\mathrm{WP}}$ in kW')
#axs[0].set_title('Oktober', loc='left')
#axs[0].set_xticks(np.arange(12,84,24))
#ax2.set_yticks(np.arange(0,4,1))
#ax2.set_ylim(-0.15,3.15)
#ax2.set_ylabel('Modus')
#ax2.plot(np.array(Time), m_w[0][26208:26496], label='Modus', color='#4B81C4', drawstyle='steps', linestyle='dashed')
#axs[0].set_xticklabels([])
#axs[1].plot(np.array(Time), Sto_w[0][26208:26496]-273.15, label='$T_{\mathrm{PS}}$', color='#F49961', linestyle= 'dotted')
#axs[1].plot(np.array(Time), TWW_w[0][26208:26496]-273.15, label='$T_{\mathrm{TWW}}$', color='#8768B4',linestyle='dashdot')
#axs[1].set_ylabel('$T$ in °C')
#axs[1].set_ylim(17,72)
#axs[1].set_yticks([20,45,70])
#fig.legend(ncol=4, bbox_to_anchor=(0.95,1.0), fontsize='small', frameon=False)
#xticks_labels = ['1.10', '2.10', '3.10']  # labels of the ticks
#axs[1].set_xticks(np.arange(12,84,24))
#axs[1].set_xticklabels(xticks_labels)
#axs[1].set_xlabel('Zeit in d')
#axs[1].axvspan(0, 24, color='grey', alpha=0.2)
#axs[0].axvspan(0, 24, color='grey', alpha=0.2)
#axs[1].axvspan(48, 72, color='grey', alpha=0.2)
#axs[0].axvspan(48, 72, color='grey', alpha=0.2)
#plt.savefig(Savedirect+'_TRY_norm_OktWoche.svg')
#tikzplotlib.save(Savedirect+'_TRY_norm_OktWoche.tex')
#plt.savefig(Savedirect+'_TRY_norm_OktWoche.pdf')
#plt.show()
#
#Time = np.arange(0, 24 * 7, 0.25)
#


#for ax in [ax, ax2]:
#    for h, l in zip(*ax.get_legend_handles_labels()):
#        handles.append(h)
#        labels.append(l)
#plt.legend(loc='upper right',fontsize='small')
#plt.savefig(Savedirect+'_Stoergroeßen.svg')
#tikzplotlib.save(Savedirect+'_Stoergroesen_P.tex')
#plt.savefig(Savedirect+'_Stoergroesen_P.pdf')
#plt.show()

plt.rcParams.update(pp_figure)
#fig, axs = plt.subplots()
#axs.plot(np.array(Time), q_hou_w[0][1344:1632]*4/1000, label='$\dot{Q}_{\mathrm{Haus}}$')
#ax2 = axs.twinx()
#axs.set_ylim(-0.500,10.5)
#axs.set_yticks(np.arange(0,11.500,2.5000))
#axs.set_ylabel('$\dot{Q}_{\mathrm{Haus}}$ in kW')
#axs.set_title('Januar', loc='left')
#axs.set_xticks(np.arange(12,84,24))
#ax2.set_yticks(np.arange(0,4,1))
#ax2.set_ylim(-0.15,3.15)
#ax2.plot(np.array(Time), pv_w[0][1344:1632]*4/1000, label='$P_{\mathrm{PV}}$', color='#4B81C4', drawstyle='steps', linestyle='dashed')
#ax2.set_ylabel('$P_{\mathrm{PV}}$ in kW')
#ax2.set_yticks(np.arange(0,6,1))
#ax2.set_ylim(-0.3,5.3)
#fig.legend(ncol=2, bbox_to_anchor=(0.95,1.0), fontsize='small', frameon=False)
#xticks_labels = ['14.1', '15.1', '16.1']  # labels of the ticks
#axs.set_xticks(np.arange(12,84,24))
#axs.set_xticklabels(xticks_labels)
#axs.set_xlabel('Zeit in d')
#axs.axvspan(0, 24, color='grey', alpha=0.2)
#axs.axvspan(48, 72, color='grey', alpha=0.2)
#plt.savefig(Savedirect+'_TRY_norm_JanWoche_p.svg')
#tikzplotlib.save(Savedirect+'_TRY_norm_JanWoche_p.tex')
#plt.savefig(Savedirect+'_TRY_norm_JanWoche_p.pdf')
#plt.show()



#plt.rcParams.update(pp_figure)
#fig, axs = plt.subplots()
#axs.plot(np.array(Time), q_hou_w[0][8640:8928]*4/1000, label='$\dot{Q}_{\mathrm{Haus}}$')
#ax2 = axs.twinx()
#axs.set_ylim(-0.500,10.5)
#axs.set_yticks(np.arange(0,11.500,2.5000))
#axs.set_ylabel('$\dot{Q}_{\mathrm{Haus}}$ in kW')
#axs.set_title('April', loc='left')
#axs.set_xticks(np.arange(12,84,24))
#ax2.set_yticks(np.arange(0,4,1))
#ax2.set_ylim(-0.15,3.15)
#ax2.plot(np.array(Time), pv_w[0][8640:8928]*4/1000, label='$P_{\mathrm{PV}}$', color='#4B81C4', drawstyle='steps', linestyle='dashed')
#ax2.set_ylabel('$P_{\mathrm{PV}}$ in kW')
#ax2.set_yticks(np.arange(0,6,1))
#ax2.set_ylim(-0.3,5.3)
#fig.legend(ncol=2, bbox_to_anchor=(0.95,1.0), fontsize='small', frameon=False)
#xticks_labels = ['1.4', '2.4', '3.4']  # labels of the ticks
#axs.set_xticks(np.arange(12,84,24))
#axs.set_xticklabels(xticks_labels)
#axs.set_xlabel('Zeit in d')
#axs.axvspan(0, 24, color='grey', alpha=0.2)
#axs.axvspan(48, 72, color='grey', alpha=0.2)

#plt.savefig(Savedirect+'_TRY_norm_AprWoche_p.svg')
#tikzplotlib.save(Savedirect+'_TRY_norm_AprWoche_p.tex')
#plt.savefig(Savedirect+'_TRY_norm_AprWoche_p.pdf')
#plt.show()






plt.rcParams.update(pp_figure)
fig, axs = plt.subplots()
axs.plot(np.array(Time), q_hou_w[0][17376:17664]*4/1000, label='$\dot{Q}_{\mathrm{Haus}}$')
ax2 = axs.twinx()
axs.set_ylim(-0.500,10.5)
axs.set_yticks(np.arange(0,11.500,2.5000))
axs.set_ylabel('$\dot{Q}_{\mathrm{Haus}}$ in kW')
axs.set_title('Juli', loc='left')
axs.set_xticks(np.arange(12,84,24))
#ax2.set_yticks(np.arange(0,4,1))
#ax2.set_ylim(-0.15,3.15)
ax2.plot(np.array(Time), pv_w[0][17376:17664]*4/1000, label='$P_{\mathrm{PV}}$', color='#4B81C4', drawstyle='steps', linestyle='dashed')
ax2.set_ylabel('$P_{\mathrm{PV}}$ in kW')
ax2.set_yticks(np.arange(0,6,1))
ax2.set_ylim(-0.3,5.3)
fig.legend(ncol=2, bbox_to_anchor=(0.95,1.0), fontsize='small', frameon=False)
xticks_labels = ['1.7', '2.7', '3.7']  # labels of the ticks
axs.set_xticks(np.arange(12,84,24))
axs.set_xticklabels(xticks_labels)
axs.set_xlabel('Zeit in d')
axs.axvspan(0, 24, color='grey', alpha=0.2)
axs.axvspan(48, 72, color='grey', alpha=0.2)

#plt.savefig(Savedirect+'_TRY_norm_JulWoche_p.svg')
#tikzplotlib.save(Savedirect+'_TRY_norm_JulWoche_p.tex')
#plt.savefig(Savedirect+'_TRY_norm_JulWoche_p.pdf')
#plt.show()

#plt.rcParams.update(pp_figure)
#fig, axs = plt.subplots()
#axs.plot(np.array(Time), q_hou_w[0][26208:26496]*4/1000, label='$\dot{Q}_{\mathrm{Haus}}$')
#ax2 = axs.twinx()
#axs.set_ylim(-0.500,10.5)
#axs.set_yticks(np.arange(0,11.500,2.5000))
#axs.set_ylabel('$\dot{Q}_{\mathrm{Haus}}$ in kW')
#axs.set_title('Oktober', loc='left')
#axs.set_xticks(np.arange(12,84,24))
#ax2.set_yticks(np.arange(0,4,1))
#ax2.set_ylim(-0.15,3.15)
#ax2.plot(np.array(Time), pv_w[0][26208:26496]*4/1000, label='$P_{\mathrm{PV}}$', color='#4B81C4', drawstyle='steps', linestyle='dashed')
#ax2.set_ylabel('$P_{\mathrm{PV}}$ in kW')
#ax2.set_yticks(np.arange(0,6,1))
#ax2.set_ylim(-0.3,5.3)
#fig.legend(ncol=2, bbox_to_anchor=(0.95,1.0), fontsize='small', frameon=False)
#xticks_labels = ['1.10', '2.10', '3.10']  # labels of the ticks
#axs.set_xticks(np.arange(12,84,24))
#axs.set_xticklabels(xticks_labels)
#axs.set_xlabel('Zeit in d')
#axs.axvspan(0, 24, color='grey', alpha=0.2)
#axs.axvspan(48, 72, color='grey', alpha=0.2)

#plt.savefig(Savedirect+'_TRY_norm_OktWoche_p.svg')
#tikzplotlib.save(Savedirect+'_TRY_norm_OktWoche_p.tex')
#plt.savefig(Savedirect+'_TRY_norm_OktWoche_p.pdf')
#plt.show()

#
#fig, axs = plt.subplots(2, 1)
#axs[0].plot(np.array(Time), q_hp_w[0][26208:26496]*4/1000, label='$\dot{Q}_{\mathrm{WP}}$')
#ax2 = axs[0].twinx()
#axs[0].set_ylim(-0.500,10.5)
#axs[0].set_yticks(np.arange(0,12.500,5.000))
#axs[0].set_ylabel('$\dot{Q}_{\mathrm{WP}}$ in kW')
#axs[0].set_title('Oktober', loc='left')
#axs[0].set_xticks(np.arange(12,84,24))
#ax2.set_yticks(np.arange(0,4,1))
#ax2.set_ylim(-0.15,3.15)
#ax2.set_ylabel('Modus')
#ax2.plot(np.array(Time), m_w[0][26208:26496], label='Modus', color='#4B81C4', drawstyle='steps', linestyle='dashed')
#
#
#axs[1].set_ylabel('$T$ in °C')
#axs[1].set_ylim(17,72)
#axs[1].set_yticks([20,45,70])
#fig.legend(ncol=4, bbox_to_anchor=(0.95,1.0), fontsize='small', frameon=False)
#xticks_labels = ['1.10', '2.10', '3.10']  # labels of the ticks
#axs[1].set_xticks(np.arange(12,84,24))
#axs[1].set_xticklabels(xticks_labels)
#axs[1].set_xlabel('Zeit in d')
#axs[1].axvspan(0, 24, color='grey', alpha=0.2)
#axs[0].axvspan(0, 24, color='grey', alpha=0.2)
#axs[1].axvspan(48, 72, color='grey', alpha=0.2)
#axs[0].axvspan(48, 72, color='grey', alpha=0.2)
#plt.savefig(Savedirect+'_TRY_norm_OktWoche_p.svg')
#tikzplotlib.save(Savedirect+'_TRY_norm_OktWoche_p.tex')
#plt.savefig(Savedirect+'_TRY_norm_OktWoche_p.pdf')
#plt.show()
#
#Time = np.arange(0, 24 * 7, 0.25)




