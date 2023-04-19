#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Handles all interactions with a FMU simulation

Author: sgo,aku
"""

import fmpy
import shutil
import time
import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
from plot_results_to_files import latex_base
from plot_results_to_files import latex_fullpage

FMU_Name = 'HPS_DHW_200_Buffer_300'
#FMU_Name = 'HeatPumpSystemProcessModel'
#FMU_Name = 'HeatPumpSystemAndControl'


#### Dateninput

TRY = 'cold'

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
print(Q_hou_dem)

#####Q_hou_dem = Data.iloc[:, 1]
#P_PV = Data.iloc[:, 2]
#P_EL_Dem = Data.iloc[:, 3] * 1000

QTWW = TWWData.iloc[:, 4]
print(len(QTWW))
TSetpDHW = TWWData.iloc[:, 5]
mDHW_flow_in = TWWData.iloc[:, 7]
#Wind_Speed = Data.iloc[:, 7]
#HGloHor = Data.iloc[:, 8]

#xp = np.arange(0.0, 8759, 1.0)
#xnew = np.arange(0.0, 8759, time_step)


ModeFile = 'Modes_Januar_cold'
Uebergabe = pd.read_csv('D:/lma-mma/Repos/MA_MM/Results/DecisionTrees/'+ ModeFile +'.csv')
Mode0 = Uebergabe.iloc[:,0]
Mode1 = Uebergabe.iloc[:,1]
Mode2 = Uebergabe.iloc[:,2]
Mode3 = Uebergabe.iloc[:,3]


class fmu_handler():
    """
    The fmu handler class
    """

    def __init__(self,
                 start_time,
                 stop_time,
                 step_size,
                 sim_tolerance,
                 fmu_file,
                 instanceName,
                 ):
        """[summary]

        Args:
            start_time ([int]): Start time in sec usually 0
            sim_date ([datetime]): the datetime of the simulation time
            stop_time ([int]): Stop time in sec
            step_size ([int]): The time step efficiency after which data is exchanged
            sim_tolerance ([float]): The numeric tolerance of the solver usual 0.001
            fmu_file ([string]): The name of the FMU file
            instanceName ([type]): A name of the FMU instance. FMPY specific can be random
        """
        self.start_time = start_time  # start time
        self.stop_time = stop_time  # stop time
        self.step_size = step_size  # The macro time step
        self.sim_tolerance = sim_tolerance  # The total simulation tolerance
        self.fmu_file = fmu_file
        self.instanceName = instanceName


        # read the model description
        self.model_description = fmpy.read_model_description(self.fmu_file)

        # Collect all variables
        #self.variables = {}
        #for variable in self.model_description.modelVariables:
        #    self.variables[variable.name] = variable
        self.variables = {}
        for variable in self.model_description.modelVariables:
            self.variables[variable.name] = variable

        # extract the FMU
        self.unzipdir = fmpy.extract(self.fmu_file)


        # create fmu obj
        self.fmu = fmpy.fmi2.FMU2Slave(guid=self.model_description.guid,
                                       unzipDirectory=self.unzipdir,
                                       modelIdentifier=self.model_description.coSimulation.modelIdentifier,
                                       instanceName=self.instanceName)

        # instantiate fmu
        self.fmu.instantiate()

    def setup(self):
        # The current simulation time
        self.current_time = self.start_time

        # initialize model
        self.fmu.reset()
        self.fmu.setupExperiment(
            startTime=self.start_time, stopTime=self.stop_time, tolerance=self.sim_tolerance)

    def initialize(self):
        self.fmu.enterInitializationMode()
        self.fmu.exitInitializationMode()

    def get_value(self, var_name: str):
        """
        Get a single variable.
        """

        variable = self.variables[var_name]
        vr = [variable.valueReference]

        if variable.type == 'Real':
            return self.fmu.getReal(vr)[0]
        elif variable.type in ['Integer', 'Enumeration']:
            return self.fmu.getInteger(vr)[0]
        elif variable.type == 'Boolean':
            value = self.fmu.getBoolean(vr)[0]
            return value != 0
        else:
            raise Exception("Unsupported type: %s" % variable.type)

    def set_value(self, var_name, value):
        """
        Set a single variable.
        var_name: str
        """

        variable = self.variables[var_name]
        vr = [variable.valueReference]

        if variable.type == 'Real':
            self.fmu.setReal(vr, [float(value)])
        elif variable.type in ['Integer', 'Enumeration']:
            self.fmu.setInteger(vr, [int(value)])
        elif variable.type == 'Boolean':
            self.fmu.setBoolean(vr, [value != 0.0 or value != False or value != "False"])
        else:
            raise Exception("Unsupported type: %s" % variable.type)

    def do_step(self):
        # check if stop time is reached
        if self.current_time < self.stop_time:
            # do simulation step
            status = self.fmu.doStep(
                currentCommunicationPoint=self.current_time,
                communicationStepSize=self.step_size)
            # augment current time step
            self.current_time += self.step_size
            finished = False
        else:
            print('Simulation finished')
            finished = True

        return finished

    def close(self):
        self.fmu.terminate()
        self.fmu.freeInstance()
        shutil.rmtree(self.unzipdir)
        print('FMU released')

    def read_variables(self, vrs_list: list):
        """
        Reads multiple variable values of FMU.
        vrs_list as list of strings
        Method retruns a dict with FMU variable names as key
        """
        res = {}
        # read current variable values ans store in dict
        for var in vrs_list:
            res[var] = self.get_value(var)

        # add current time to results
        res['SimTime'] = self.current_time

        return res

    def set_variables(self, var_dict: dict):
        '''
        Sets multiple variables.
        var_dict is a dict with variable names in keys.
        '''

        for key in var_dict:
            self.set_value(key, var_dict[key])
        return "Variable set!!"

    def __enter__(self):
        self.fmu.terminate()
        self.fmu.freeInstance()


if __name__ == "__main__":
    # load fmu and setup
    fmu = fmu_handler(start_time=3600 * 0,
                      stop_time=3600 * 72,
                      step_size=900,
                      sim_tolerance=0.01,
                      fmu_file='D:/lma-mma/Repos/fubic/ExtractingRulesStudy/FMUs/HPS_DHW_200_Buffer_300.fmu',
                      instanceName='test1',
                      )

    fmu.setup()

    # initialize
    fmu.set_value('TSetpDHW', 80)
    fmu.initialize()

    # flag for while loop
    finished = False

    time_step_weather_real = 0.25  # hours, time step of data
    m_flow_Cons = []
    TSupplyCons = []
    TReturnnCons = []
    P_EL_HP = []
    Q_HP = []
    TMeaSupHP = []
    TDHWStoTop = []
    TDHWStoBot = []
    TBufStoTop = []
    TBufStoBot = []
    SimTime = []

    while not finished:
        fmu.set_value('TAmb', T_Air[int((fmu.current_time / 900))])
        fmu.set_value('Q_hou_dem', Q_hou_dem[int((fmu.current_time / 900))])
        #        fmu.set_value('P_PV', P_PV[int((fmu.current_time / 3600) * time_step_weather_real)])
        #        fmu.set_value('P_EL_Dem', P_EL_Dem[int((fmu.current_time / 3600) * time_step_weather_real)])
        #        fmu.set_value('WindSpeed', Wind_Speed[int((fmu.current_time / 3600) * time_step_weather_real)])
        #
        #        fmu.set_value('HGloHor', HGloHor[int((fmu.current_time / 3600) * time_step_weather_real)])
        fmu.set_value('Mode0', Mode0[int((fmu.current_time / 900))])
        fmu.set_value('Mode1', Mode1[int((fmu.current_time / 900))])
        fmu.set_value('Mode2', Mode2[int((fmu.current_time / 900))])
        fmu.set_value('Mode3', Mode3[int((fmu.current_time / 900))])


        if TSetpDHW[int((fmu.current_time / 900))] == 0:
            fmu.set_value('TSetpDHW', 10)
        else:
            fmu.set_value('TSetpDHW',TSetpDHW[int((fmu.current_time / 900) )])
        fmu.set_value('mDHW_flow_in', mDHW_flow_in[int((fmu.current_time / 900))] / 60 )


        # read result at current time step

#        m_flow_Cons.append(fmu.read_variables(['m_flow_Cons']))
        #m_flow_Cons.append(fmu.get_value('m_flow_Cons'))
        m_flow_Cons.append(fmu.get_value('mDHW_flow_in'))
        TSupplyCons.append(fmu.get_value('TSupplyCons'))
        TReturnnCons.append(fmu.get_value('TReturnCons'))
        P_EL_HP.append(fmu.get_value('HPPEle'))
        Q_HP.append(fmu.get_value('HPQCon'))
        TMeaSupHP.append(fmu.get_value('TMeaSupHP'))
        TDHWStoTop.append(fmu.get_value('TDHWStoTop'))
        TDHWStoBot.append(fmu.get_value('TDHWStoBot'))
        TBufStoTop.append(fmu.get_value('TBufStoTop'))
        TBufStoBot.append(fmu.get_value('TBufStoBot'))
        SimTime.append(fmu.current_time)


#        print(Q_hou_dem[int((fmu.current_time / 900) * time_step_weather_real)])
        # set rewrite inputs
 #       fmu.set_variables({'volumeFlow_air': 3000, 'T_Air_In': 10, 'T_water_in': 70})
        # do step
#        print(TSetpDHW[int((fmu.current_time / 3600) * time_step_weather_real)])
#        print(T_Air[int((fmu.current_time / 900) * time_step_weather_real)])

        finished = fmu.do_step()


    # close fmu
    fmu.close()

    Mode0.tolist()
#    print(len(Mode0))
    Modus = []
    for i in range(0, len(Mode0 + 1)):
        if Mode0[i] == 1:
              Modus.append(0)
        elif Mode1[i] == 1:
              Modus.append(1)
        elif Mode2[i] == 1:
              Modus.append(2)
        else:
              Modus.append(3)

#ERST DIE SIM INPUT DATEN IM TESTRAUM ERSTELLEN!!!!

#    print('Q_HP')
#    print(Q_HP)
#    print('m_flow_Cons')
#    print(m_flow_Cons[0])
#    print('TSupplyCons')
#    print(TSupplyCons)
#    print('P_EL_HP')
#    print(P_EL_HP)
#    print('TMeaSupHP')
#    print(TMeaSupHP)
#    print('TDHWStoTop')
#    print(TDHWStoTop)
#    print('TDHWStoBot')
#    print(TDHWStoBot)
#    print('TBufStoBot')
#    print(TBufStoBot)
#    print('TBufStoTop')
#print(TBufStoTop)
    plt.rcParams.update(latex_fullpage)

    # Extract the values of m_flow_Cons and SimTime
#    m_flow_Cons = [d[i]['m_flow_Cons'] for i in range(0, len(d), 2)]
#    SimTime = [d[i]['SimTime'] for i in range(0, len(d), 2)]
    # Create a scatter plot
    Laenge = len(TBufStoBot)
    fig, ax = plt.subplots(4, 2)
    ax[0,0].plot(np.array(SimTime)/3600, Q_HP)
    # Set the x-label and y-label
#    SimTime = np.arange(1)
    plt.xlabel('SimTime')
    ax[0,0].set_ylabel('Q_HP')
    # Show the plot

    #ax[0,1].plot(np.array(SimTime)/3600, mDHW_flow_in[0:len(TBufStoBot)])
    ax[0, 1].plot(np.array(SimTime) / 3600, m_flow_Cons)
    # Set the x-label and y-label
    #    SimTime = np.arange(1)
    plt.xlabel('SimTime')
    plt.ylabel('m_flow_Cons')
#    plt.savefig('D:/lma-mma/Repos/MA_MM/Datensicherung/Test/1')
    # Show the plot
#    plt.show()

#    fig, ax = plt.subplots(1, 2, figsize=(6.5, 2.9))
    ax[1,0].plot(np.array(SimTime)/3600, TDHWStoTop)
    # Set the x-label and y-label
    #    SimTime = np.arange(1)
#    plt.xlabel('SimTime')
    ax[1,0].set_ylabel('TDHWTop')
    # Show the plot

    ax[1,1].plot(np.array(SimTime)/3600, TDHWStoBot)
    # Set the x-label and y-label
    #    SimTime = np.arange(1)
#    plt.xlabel('SimTime')
    ax[1,1].set_ylabel('TDHWBot')
    # Show the plot
#    plt.savefig('D:/lma-mma/Repos/MA_MM/Datensicherung/Test/2')
#    plt.show()

#    fig, ax = plt.subplots(1, 2, figsize=(6.5, 2.9))
    ax[2,0].plot(np.array(SimTime)/3600, TBufStoTop)
    # Set the x-label and y-label
    #    SimTime = np.arange(1)
#    ax[3,0].set_xlabel('SimTime')
    ax[2,0].set_ylabel('TStoTop')
    # Show the plot

    ax[2,1].plot(np.array(SimTime)/3600, TBufStoBot)
    # Set the x-label and y-label
    #    SimTime = np.arange(1)
#    plt.xlabel('SimTime')
    ax[2,1].set_ylabel('TStoBot')
    # Show the plot

    ax[3,0].plot(np.array(SimTime)/3600, Modus[0:len(TBufStoBot)])
    # Set the x-label and y-label
    #    SimTime = np.arange(1)
    #    plt.xlabel('SimTime')
    ax[3,0].set_ylabel('Modus')



    ax[3,1].plot(np.array(SimTime)/3600, QTWW[0:len(TBufStoBot)])
    # Set the x-label and y-label
    #    SimTime = np.arange(1)
    #    plt.xlabel('SimTime')
    ax[3,1].set_ylabel('QTWW')




    plt.savefig('D:/lma-mma/Repos/MA_MM/Datensicherung/Test/3.pdf')
    plt.show()

#    print(sum(QTWW[0:96]))


