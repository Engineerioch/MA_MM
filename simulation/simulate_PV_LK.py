# -*- coding: utf-8 -*-

"""
Author: lku
"""

from simulation.fmu_handler import fmu_handler
import fmpy as fmpy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


#FMU_Name = 'HPS_DHW_200_Buffer_300(1)'
FMU_Name = 'HPS_DHW_200_Buffer_300_WithBackup'
#FMU_Name = 'HeatPumpSystemAndControl'


#### Dateninput

TRY = 'warm'
Mode = 'DB'

# Todo: Wetterdaten aus Parameters.py holen
Data = pd.read_csv('D:/lma-mma/Repos/MA_MM/input_data/Sim_Input/InputYear_cold.csv')
#Zeitschritt in h
time_step = 1

dT = pd.read_csv('D:/lma-mma/Repos/MA_MM/input_data/Opti_Input/Temperature_Berlin.csv', skiprows=0)


dQ = pd.read_csv('D:/lma-mma/Repos/MA_MM/input_data/Opti_Input/Q_Dem/Q_Heat_Dem_cold.csv')

if TRY == 'cold':

    dQ = pd.read_csv('D:/lma-mma/Repos/MA_MM/input_data/Opti_Input/Q_Dem/Q_Heat_Dem_cold.csv')
    P_PV_list = pd.read_csv('D:/lma-mma/Repos/MA_MM/input_data/Opti_Input/P_PV/P_PV_TRY_cold.csv')
    TWWData = pd.read_csv('D:/lma-mma/Repos/MA_MM/input_data/ClusteredYear/ClusteredYear_cold.csv')

elif TRY == 'normal':

    dQ = pd.read_csv('D:/lma-mma/Repos/MA_MM/input_data/Opti_Input/Q_Dem/Q_Heat_Dem_normal.csv')
    P_PV_list = pd.read_csv('D:/lma-mma/Repos/MA_MM/input_data/Opti_Input/P_PV/P_PV_TRY_normal.csv')
    TWWData = pd.read_csv('D:/lma-mma/Repos/MA_MM/input_data/ClusteredYear/ClusteredYear_normal.csv')

elif TRY == 'warm':

    dQ = pd.read_csv('D:/lma-mma/Repos/MA_MM/input_data/Opti_Input/Q_Dem/Q_Heat_Dem_warm.csv')
    P_PV_list = pd.read_csv('D:/lma-mma/Repos/MA_MM/input_data/Opti_Input/P_PV/P_PV_TRY_warm.csv')
    TWWData = pd.read_csv('D:/lma-mma/Repos/MA_MM/input_data/ClusteredYear/ClusteredYear_warm.csv')

T_Input = (dT.iloc[:, 1] + 273.15)

dQ = dQ.iloc[:, 1:]
Q_Hou_Input = dQ.sum(axis=1)

P_PV_list = P_PV_list.values.tolist()
PV = [item for sublist in P_PV_list for item in sublist]

PEL = np.loadtxt('D:/lma-mma/Repos/MA_MM/input_data/Opti_Input/ELHour.txt')

xp = np.arange(0.0, 8784, 1.0)
xnew = np.arange(0.0, 8784, 0.25)


T_Air = np.interp(xnew, xp, T_Input)
Q_hou_dem = np.interp(xnew, xp, Q_Hou_Input)
P_PV = np.interp(xnew, xp, PV)
P_EL_Dem = np.interp(xnew, xp, PEL)

QTWW = TWWData.iloc[:, 4]
TSetpDHW = TWWData.iloc[:, 5]
mDHW_flow_in = TWWData.iloc[:, 7]


Mode0 = []
Mode1 = []
Mode2 = []
Mode3 = []
if Mode=='GB':
    ModeFile = 'Modes_Jahr_warm3_GB'
    Uebergabe = pd.read_csv('D:/lma-mma/Repos/MA_MM/Results/DecisionTrees/'+ ModeFile +'.csv')
    Mode0 = Uebergabe.iloc[:,0]
    Mode1 = Uebergabe.iloc[:,1]
    Mode2 = Uebergabe.iloc[:,2]
    Mode3 = Uebergabe.iloc[:,3]
elif Mode == 'DB':
    ModeFile = 'Modes_Jahr_warm3_DB'
    Uebergabe = pd.read_csv('D:/lma-mma/Repos/MA_MM/Results/DecisionTrees/'+ ModeFile +'.csv')
    Mode0 = Uebergabe.iloc[:,0]
    Mode1 = Uebergabe.iloc[:,1]
    Mode2 = Uebergabe.iloc[:,2]
    Mode3 = Uebergabe.iloc[:,3]
elif Mode == 'TRY':
    Uebergabe = np.loadtxt('D:/lma-mma/Repos/MA_MM/Results/Optimierung/TWW/Modes_0_025_8736_4_24_TRY_warm_Fix_TWW_Small_Norm.csv', skiprows=0)
    for val in Uebergabe:
        if val == 0:
            Mode0.append(1)
            Mode1.append(0)
            Mode2.append(0)
            Mode3.append(0)
        elif val == 1:
            Mode1.append(1)
            Mode2.append(0)
            Mode3.append(0)
            Mode0.append(0)
        elif val == 2:
            Mode2.append(1)
            Mode1.append(0)
            Mode3.append(0)
            Mode0.append(0)
        elif val == 3:
            Mode3.append(1)
            Mode0.append(0)
            Mode1.append(0)
            Mode2.append(0)
elif Mode == 'Clusteryear':
    Uebergabe = np.loadtxt('D:/lma-mma/Repos/MA_MM/Results/Optimierung/TWW/Modes_0_025_8760_4_24_Clusteryear_warm_Fix_TWW_Small_Norm.csv',skiprows=0)
    for val in Uebergabe:
        if val == 0:
            Mode0.append(1)
            Mode1.append(0)
            Mode2.append(0)
            Mode3.append(0)
        elif val == 1:
            Mode1.append(1)
            Mode2.append(0)
            Mode3.append(0)
            Mode0.append(0)
        elif val == 2:
            Mode2.append(1)
            Mode1.append(0)
            Mode3.append(0)
            Mode0.append(0)
        elif val == 3:
            Mode3.append(1)
            Mode0.append(0)
            Mode1.append(0)
            Mode2.append(0)
print(len(Mode0))




def run_PV_sim(params): #, options, devs):

#    fmu_file = 'D:/lma-mma/Repos/MA_MM/FMUs/FubicModelica_PV_FMU_WithInterfaces.fmu'
#    fmu_file = 'D:/lma-mma/Repos/MA_MM/FMUs/' + FMU_Name + '.fmu'
 #   fmu_file = 'D:/lma-mma/Repos/fubic/ExtractingRulesStudy/FMUs/' + FMU_Name + '.fmu'
    fmu = fmu_handler(
        start_time=0, #params['start_time'],
        stop_time=24 * 3600, # (params['start_time']+params['prediction_horizon']-params['time_step'])*3600,
        step_size=3600 * params['time_step'],
        sim_tolerance=0.01,
        fmu_file=fmu_file,
        instanceName='test1')

    fmu.setup()

    # PV
    #fmu.set_value('PV_factor', options['PV']['PV_factor'])
    fmu.set_value('PanelsWest', 20) #devs['PV']['n_Mod'] / 2)
    fmu.set_value('PanelsEast', 0) #devs['PV']['n_Mod'] / 2)
    fmu.set_value('eta_nom_PV', 0.9801) #devs['PV']['eta_nom_PV'])
    fmu.set_value('P_Max_PV', 6000) #devs['PV']['n_Mod']  * 330)
    fmu.set_value('P_Min_PV', 0) #devs['PV']['P_Min_PV'])
    fmu.set_value('a1_PV', 0.002409) #devs['PV']['a_PV'][0])
    fmu.set_value('a2_PV', 0.00561) #devs['PV']['a_PV'][1])
    fmu.set_value('a3_PV', 0.01228) #devs['PV']['a_PV'][2])
    fmu.set_value(('tcrit'))
#    fmu.set_value(('heatPumpBufferDHW.dHW.calcmFlow.TSet', 300))



    fmu.initialize()

    # flag for while loop
    finished = False

    results = {
        'P_PV_AC':[]
    }

    time_step_weather_real = 1  # hours, time step of data

    while not finished:

        # set inputs for current time step
        fmu.set_value('TAmb', T_Air[int((fmu.current_time / 3600) * time_step_weather_real)])
        fmu.set_value('Q_hou_dem', Q_hou_dem[int((fmu.current_time / 3600) * time_step_weather_real)])
#        fmu.set_value('P_PV', P_PV[int((fmu.current_time / 3600) * time_step_weather_real)])
#        fmu.set_value('P_EL_Dem', P_EL_Dem[int((fmu.current_time / 3600) * time_step_weather_real)])
#        fmu.set_value('WindSpeed', Wind_Speed[int((fmu.current_time / 3600) * time_step_weather_real)])
#
#        fmu.set_value('HGloHor', HGloHor[int((fmu.current_time / 3600) * time_step_weather_real)])
        fmu.set_value('Mode0', Mode0[int((fmu.current_time / 3600) * time_step_weather_real)])
        fmu.set_value('Mode1', Mode1[int((fmu.current_time / 3600) * time_step_weather_real)])
        fmu.set_value('Mode2', Mode2[int((fmu.current_time / 3600) * time_step_weather_real)])
        fmu.set_value('Mode3', Mode3[int((fmu.current_time / 3600) * time_step_weather_real)])
        fmu.set_value('TSetpDHW', TSetpDHW[int((fmu.current_time / 3600) * time_step_weather_real)])
        fmu.set_value('mDHW_flow_in', mDHW_flow_in[int((fmu.current_time / 3600) * time_step_weather_real)])
#        fmu.set_value('QiErr', 300)
#        fmu.set_value(('TSetpDHW_start', 15))


        P_PV = Data.iloc[:, 2]
        P_EL_Dem = Data.iloc[:, 3] * 1000
        QTWW = Data.iloc[:, 4] * 1000
        TSetDHW = Data.iloc[:, 5]
 #       mDHW_flow_in = Data.iloc[:, 6]
        Wind_Speed = Data.iloc[:, 7]
        HGloHor = Data.iloc[:, 8]

        # read result at current time step

#        if FMU_Name == 'HeatPumpSystemAndControl':
#            results['P_PV'].append(float(fmu.get_value('DCOutputPower')))
#            results['TBufLayer4'].append(float(fmu.get_value('TBufLayer4')))
#            results['TBufLayer3'].append(float(fmu.get_value('TBufLayer3')))
#            results['TBufLayer2'].append(float(fmu.get_value('TBufLayer2')))
#            results['TBufLayer1'].append(float(fmu.get_value('TBufLayer1')))
#            results['TSupConHP'].append(float(fmu.get_value('TSupConHP')))
#            results['TSupplyCons'].append(float(fmu.get_value('TSupplyCons')))
##            results['TRetConHP'].append(float(fmu.get_value('TRetConHp')))
#            results['TSupEvaHP'].append(float(fmu.get_value('TSupEvaHp')))
#            results['TRetEvaHP'].append(float(fmu.get_value('TRetEvaHP')))


#        elif FMU_Name == 'HeatPumpSystemProcessModel':
#            results['P_PV'].append(float(fmu.get_value('DCOutputPower')))
#            results['TSupConHP'].append(float(fmu.get_value('TBufLayer4')))
#            results['TSupplyCons'].append(float(fmu.get_value('TBufLayer3')))
#            results['TReturnCons'].append(float(fmu.get_value('TBufLayer2')))
#            results['TReturnCons'].append(float(fmu.get_value('TBufLayer1')))
#            results['TRetConHP'].append(float(fmu.get_value('TSupConHP')))
#            results['TSupEvaHP'].append(float(fmu.get_value('TSupplyCons')))
#            results['TRetEvaHP'].append(float(fmu.get_value('TReturnCons')))
#            results[''].append(float(fmu.get_value('')))
#            results[''].append(float(fmu.get_value('')))


        # do step
        finished = fmu.do_step()
        if finished == True:
            break

    # close fmu
    fmu.close()

#    plt.plot(results['P_PV_AC'])
#    print(results['P_PV_AC'], sum(results['P_PV_AC']))
#    plt.show()

    return results

#if __name__ == '__main__':
#    params = {
#        'start_time': 0,
#        'prediction_horizon': 8760*3600,
#        'time_step': 3600
#    }
#
#    sim_results = run_PV_sim(params)
#
#    #plt.plot(sim_results['SOC_bat'])
#    plt.plot(sim_results['P_PV_AC'])
#    plt.show()
#
#
#    df = pd.DataFrame(sim_results['P_PV_AC'])
#    df.to_csv('Test.csv', index=False)





