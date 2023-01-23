# -*- coding: utf-8 -*-

"""
Author: lku
"""

from simulation.fmu_handler import fmu_handler
import fmpy as fmpy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Todo: Wetterdaten aus Parameters.py holen
T_Air = pd.read_csv('D:/lma-mma/MA_MM_Python/input_data/Temperature_Berlin.csv', skiprows=0)
T_Air = T_Air.iloc[:, 3]
winSpe = pd.read_csv('D:/lma-mma/MA_MM_Python/input_data/Wind_Speed_Berlin.csv', skiprows=0)
Wind_Speed = winSpe.iloc[:, 3]
H = pd.read_csv('D:/lma-mma/MA_MM_Python/input_data/Global_Radiation_Berlin.csv', skiprows=0)
HGloHor = H.iloc[:, 3]


def run_PV_sim(params): #, options, devs):
    fmu_file = 'D:/lma-mma/MA_MM_Python/FMUs/FubicModelica_PV_FMU_WithInterfaces.fmu'
    fmu = fmu_handler(
        start_time=0, #params['start_time'],
        stop_time=8760*3600, # (params['start_time']+params['prediction_horizon']-params['time_step'])*3600,
        step_size=3600, #params['time_step']*3600,
        sim_tolerance=0.01,
        fmu_file=fmu_file,
        instanceName='PV_sim')

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


    fmu.initialize()

    # flag for while loop
    finished = False

    results = {
        'P_PV_AC':[]
    }

    time_step_weather_real = 1  # hours, time step of data

    while not finished:

        # set inputs for current time step
        fmu.set_value('TDryBulb', 273.15 + T_Air[int((fmu.current_time / 3600) * time_step_weather_real)])
        fmu.set_value('HGloHor', HGloHor[int((fmu.current_time / 3600) * time_step_weather_real)])

        # read result at current time step
        results['P_PV_AC'].append(float(fmu.get_value('P_PV_AC')))

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

if __name__ == '__main__':
    params = {
        'start_time': 0,
        'prediction_horizon': 8760*3600,
        'time_step': 3600
    }

    sim_results = run_PV_sim(params)

    #plt.plot(sim_results['SOC_bat'])
    plt.plot(sim_results['P_PV_AC'])
    plt.show()


    df = pd.DataFrame(sim_results['P_PV_AC'])
    df.to_csv('P_PV_TRY_cold', index=False)
