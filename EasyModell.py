from pyomo.environ import *
from pyomo.opt import SolverStatus, TerminationCondition
import math
import numpy as np







def runeasyModell(params, options, eco, time_series, devs, iter, T_Sto_Init, T_TWW_Init):
    # Set parameter
    dt = params['time_step']  # time Step in hours
    start_time = int(params['start_time'] / params['time_step'])

    prediction_horizon = params['prediction_horizon']
    total_runtime = int(params['total_runtime'])
    time_range = range(int(prediction_horizon * (1 / params['time_step'])) + 1)
    time = range(int(prediction_horizon / params['time_step']))
    delta_t = params['time_step'] * 3600  # time Step in
    sum_control =range(int(params['control_horizon'] / params['time_step']))
    time_step = params['time_step']
    start_time_hour = int(start_time * time_step)


    # Set economic parameters
    c_payment = eco['costs']['c_payment']  # [Euro/kWh]    Feed in tariff
#    c_grid = time_series['c_grid'] / 1000               # [€/Wh] Strompreis bei Netzbezug (Teilung durch 1000 weil Rohdaten in €/kWh
    c_comfort = eco['costs']['c_comfort'] / 1000        # [€/Wh] Strafkosten bei nicht gedeckten Hauswärembedarf



    # Set Heat storage parameters
    T_Sto_Ersatz = devs['Sto']['T_Sto_Ersatz']
    T_Sto_max = devs['Sto']['T_Sto_max']
    T_Sto_min = devs['Sto']['T_Sto_min']

    m_Sto_water = devs['Sto']['Volume'] * devs['Nature']['Roh_water']
    T_Sto_Env = devs['Sto']['T_Sto_Env']
    U_Sto = devs['Sto']['U_Sto']
    h_d = devs['Sto']['h_d_ratio']
    V_Sto = devs['Sto']['Volume']
    D_Sto_In   =   ((V_Sto * 4)/math.pi * h_d)**(1/float(3))         # Innendurchmesser des Speichers
    D_Sto_Au   = D_Sto_In + 2 * devs['Sto']['S_Wall']
    A_Sto      = ((math.pi * (D_Sto_Au ** 2)) / 4) * 2 + math.pi * D_Sto_Au * (h_d * D_Sto_In)


    #Set TWW Parameters:

    m_TWW_water = devs['TWW']['Volume'] * devs['Nature']['Roh_water']
    U_TWW = devs['TWW']['U_TWW']
    h_d_TWW = devs['TWW']['h_d_ratio']
    V_TWW = devs['TWW']['Volume']
    D_TWW_In   =   ((V_TWW * 4)/math.pi * h_d_TWW)**(1/float(3))         # Innendurchmesser des TWW-Speichers
    D_TWW_Au   = D_TWW_In + 2 * devs['TWW']['S_Wall']
    A_TWW      = ((math.pi * (D_TWW_Au ** 2)) / 4) * 2 + math.pi * D_TWW_Au * (h_d * D_TWW_In)
    if options['Sto']['Type'] == 'Seperated':
        T_TWW_Min = devs['TWW']['T_TWW_Min']
    else:
        T_TWW_Min = T_Sto_Env



    # Set Consumer parameter
    T_Hou_delta_max = devs['Hou']['T_Hou_delta_max']
    m_flow_Hou = devs['Hou']['m_flow_Hou']
    T_Hou_Gre = devs['Hou']['T_Hou_Gre']
    T_Spreiz_Hou = devs['Hou']['T_Spreiz_Hou']
    T_Ref       = devs['Nature']['T_Ref']
    T_Hou_VL_min  = devs['Hou']['T_Hou_VL_min']


    # Set Heat Pump parameters
    m_flow_HP = devs['HP']['m_flow_HP']
    eta_HP = devs['HP']['eta_HP']  # [-] Gütegrad HP
    T_HP_VL_1 = devs['HP']['T_HP_VL_1']  # [K] Vorlauftemperatur der Wärmepumpe im Modus "1", = 70°C
    T_HP_VL_2 = devs['HP']['T_HP_VL_2']  # [K] Vorlauftemperatur der Wärmepumpe im Modus "2", = 35°C
    T_HP_VL_3 = devs['HP']['T_HP_VL_3']  # [K] Vorlauftemperatur im Modus "Off", = 20°C
    T_Spreiz_HP  = devs['HP']['T_Spreiz_HP']   # [K] Maximum Change of Temperature between Vorlauf and Rücklauf


    # Set Natural Parameters
    c_w_water = devs['Nature']['c_w_water']


    # Input Input-Data
    P_PV = time_series['P_PV']
    T_Input = time_series['T_Air'] + 273.15  # [K]  Außentemperatur
    P_EL_Dem = time_series['P_EL_Dem']
    Q_Hou_Input = time_series['Q_Hou_Dem']  # [W] Heat Demand of House
    c_grid = time_series['c_grid'] / 1000
    if options['Sto']['Type'] == 'Seperated':
        Q_TWW_Dem = time_series['Q_TWW_Dem']
    else:
        Q_TWW_Dem = np.zeros(8760)


    xp = np.arange(0.0, 8783, 1.0)
    xnew = np.arange(0.0, 8783, time_step)
    P_PV = np.interp(xnew, xp, P_PV)
    T_Input = np.interp(xnew, xp, T_Input)
    P_EL_Dem = np.interp(xnew, xp, P_EL_Dem)
    Q_Hou_Input = np.interp(xnew, xp, Q_Hou_Input)
    c_grid = np.interp(xnew, xp, c_grid)
    if options['Sto']['Type'] == 'Seperated':
        Q_TWW_Dem = np.interp(xnew,xp, Q_TWW_Dem)
    else:
        pass

    # Calculation of COP in each mode and in each time step
    Temp_COP = T_Input.tolist()
    COP_1 = []
    for i in range (start_time, int(start_time + (total_runtime/time_step))):
        COP_if = T_HP_VL_1 / ( T_HP_VL_1 - Temp_COP[i])
        if  COP_if <= 0:
            COP1 = 1
        else:
            COP1 = COP_if
        COP_1.append(COP1)

    COP_2 = []
    for i in range (start_time, int(start_time + total_runtime/time_step)):
        COP_if = T_HP_VL_2 / (T_HP_VL_2 - Temp_COP[i])
        if  COP_if <= 0:
            COP2 = 1
        else:
            COP2 = COP_if
        COP_2.append(COP2)

    for i in range(0, total_runtime, int(24/time_step)):
        start_index = start_time
        if start_time_hour % 24 != 0:
            start_index -= int((start_time_hour % 24) / time_step)
        T_Mean = sum(T_Input[start_index: start_index + int(24/time_step)]) / int(24/time_step)


    model = ConcreteModel()

#    model.P_PV = Var(time, within=NonNegativeReals , name = 'P_PV')
    model.Q_Hou         = Var(time, within= NonNegativeReals, name='Q_Hou')#, initialize=initials_test['Q_Hou'])
    model.Q_HP          = Var(time, within= NonNegativeReals, name='Q_HP',bounds=(0, 10000 * time_step))
    model.Q_HP_Unreal   = Var(time, within=NonNegativeReals, name='Q_HP_Unreal', bounds=(0, 10000))
    model.Q_Penalty     = Var(time, within=NonNegativeReals, name='Q_Penalty')
    model.Q_Sto_Power   = Var(time, within=NonNegativeReals, name='Q_Sto_Power')
    model.Q_Sto_Loss    = Var(time, within=Reals, name='Q_Sto_Loss')
    model.Q_Sto_Energy  = Var(time, within=Reals, name='Q_Sto_Energy')
    model.Q_Sto_Power_max=Var(time, within=Reals, name='Q_Sto_Power_max')#, bounds=(0,10000))
    model.Q_Hou_Dem     = Var(time, within=Reals, name='Q_Hou_Dem')
    model.Q_HP_1        = Var(time, within=NonNegativeReals, name='Q_HP_1')
    model.Q_HP_2        = Var(time, within=NonNegativeReals, name='Q_HP_2')
    model.P_EL_Dem      = Var(time, within=NonNegativeReals, name='P_EL_Dem')#, initialize=initials_test['P_EL_Dem'])
    model.T_Air         = Var(time, within=Reals, name='T_Air')#, initialize=initials_test['T_Air'])
    model.T_HP_VL       = Var(time, within=NonNegativeReals, name='T_HP_VL')
    model.T_HP_RL       = Var(time, within=NonNegativeReals, name='T_HP_RL')
    model.T_Sto         = Var(time, within=NonNegativeReals, bounds=(T_Sto_Env, T_Sto_max), name='T_Sto')
    model.T_Hou_VL      = Var(time, within=NonNegativeReals, name='T_Hou_VL')
    model.T_Hou_RL      = Var(time, within=NonNegativeReals, bounds=(283.15, 400), name='T_Hou_RL')
    model.P_EL_HP       = Var(time, within=NonNegativeReals, name='P_EL_HP', bounds=(0, 10000))
    model.P_EL          = Var(time, within=Reals, name='P_EL')
    model.P_PV          = Var(time, within=Reals, name='P_PV')
    model.P_HP_1        = Var(time, within=NonNegativeReals, name='P_HP_1')
    model.P_HP_2        = Var(time, within=NonNegativeReals, name='P_HP_2')
    model.P_HP_off      = Var(time, within=NonNegativeReals, name='P_HP_off')
    model.costs_total_ph= Var(      within=Reals, name='costs_total_ph', initialize=0)
    model.costs_total_ch= Var(      within=Reals, name='costs_total_ch', initialize=0)
    model.c_heat_power  = Var(time, within=Reals, name='c_heat_power')
    model.c_penalty     = Var(time, within=NonNegativeReals, name='c_penalty')
    model.c_revenue     = Var(time, within=NonPositiveReals, name='c_revenue')
    model.c_el_power    = Var(time, within=NonNegativeReals, name='c_el_power')
    model.c_el_cost_ch     = Var(   within=Reals,name='c_el_cost_ch')
    model.c_cost        = Var(time, within=Reals,name='c_cost')
    model.HP_off        = Var(time, within=Binary, name='HP_off')
    model.HP_mode1      = Var(time, within=Binary, name='HP_mode1')
    model.HP_mode2      = Var(time, within=Binary, name='HP_mode2')
    model.Mode          = Var(time, within=Reals, name='Mode')
    model.COP_Carnot    = Var(time, within=NonNegativeReals, name='COP_Carnot')
    model.COP_HP        = Var(time, within=NonNegativeReals, name='COP_HP')
    model.No_Feed_In    = Var(time, within=Binary, name='No_Feed_In')
    model.d_Temp_HP     = Var(time, within=Reals, name='d_Temp_HP', bounds=(0, T_Spreiz_HP))
    model.m_flow_Hou  = Var(time, within=NonNegativeReals, name='m_flow_Hou_1', bounds=(0, m_flow_Hou))
    model.d_Temp_Hou    = Var(time, within=Reals, name='d_Temp_Hou', bounds=(0, T_Spreiz_Hou))
    model.Q_TWW_Loss    = Var(time, within=NonNegativeReals, name='Q_TWW_Loss')
    model.T_TWW = Var(time, within=NonNegativeReals, name='T_TWW')
    model.Q_TWW_Dem = Var(time, within=NonNegativeReals, name='Q_TWW_Dem')
    model.HP_TWW = Var(time, within=Binary, name='HP_TWW')
    model.Q_TWW_Max = Var(time, within=NonNegativeReals, name='Q_TWW_Max')
    model.Sto_Penalty = Var(time, within=Binary, name='Sto_Penalty')
    model.B_Hou = Var(time, within=Binary, name='B_Hou')


####################---1. Read of Input Data and Set it to the corresponding Variable ---####################

    # Read Power Demand Data: [Wh]
    def Power_Demand_In_House(m, t):
        return(m.P_EL_Dem[t] == P_EL_Dem[t + start_time] * time_step)
    model.Power_Demand_In_House = Constraint(time, rule= Power_Demand_In_House, name= 'Power_Demand_In_House')

    # Read Outside Temperature: [K]
    def Temp_Outside(m, t):
        return(m.T_Air[t] == T_Input[t + start_time])
    model.Temp_Outside = Constraint(time, rule= Temp_Outside, name='Temp_Outside')

    # Read PV Data: [Wh]
    def PV_Import(m, t):
        return(m.P_PV[t] == P_PV[t + start_time] * time_step)
    model.PV_Import = Constraint(time, rule=PV_Import, name='PV_Import')

    # Read T-Mean for each time-step and Set Q-Hou_Dem = 0 wenn T_Mean> T_Heiz_Grenz
    # If T_Mean < T_Heiz_Grenz then read the Q_Hou_Dem Data: [Wh]
    def House_Demand(m, t):
        if T_Mean >= T_Hou_Gre:
            return(m.Q_Hou_Dem[t] == 0)
        else:
            return(m.Q_Hou_Dem[t] == Q_Hou_Input[t+start_time] * time_step)
    model.House_Demand = Constraint(time, rule=House_Demand, name='House_Demant')


    if T_Mean >= T_Hou_Gre:
        def Heat_House_Summer(m, t):
            return (m.Q_Hou[t] == 0)
        model.Heat_House_Summer = Constraint(time, rule=Heat_House_Summer, name='Heat_House_Summer')

        def House_Power_Binary(m, t):
            return (m.B_Hou[t] == 0)
        model.House_Power_Binary = Constraint(time, rule=House_Power_Binary, name='House_Power_Binary')

        def Sto_House_Summer(m, t):
            return (m.T_Sto[t] >= T_Sto_Env)
        model.Sto_House_Summer = Constraint(time, rule=Sto_House_Summer, name='Sto_House_Summer')
    else:
        def Sto_House_Summer(m, t):
            return (m.T_Sto[t] >= T_Sto_Ersatz)
        model.Sto_House_Summer = Constraint(time, rule=Sto_House_Summer, name='Sto_House_Summer')

        def House_Power_Binary(m, t):
            return(m.B_Hou[t] == 1)
        model.House_Power_Binary = Constraint(time, rule=House_Power_Binary, name='House_Power_Binary')


####################---2. Calculate the HP- Datas depending on Mode ---####################

    # Constraint to set minimum and maximum one mode: [-]
    def HP_Modes(m, t):
       return(m.HP_off[t] + m.HP_mode1[t] + m.HP_mode2[t] + m.HP_TWW[t] == 1)
    model.HP_Modes = Constraint(time, rule= HP_Modes, name='HP_Modes')

    # Calculation of actual T_HP_VL depending on mode: [K]
    def Operation_Temp(m, t):
        return (m.T_HP_VL[t] == (m.HP_mode1[t] * T_HP_VL_1) + ((m.HP_mode2[t] + m.HP_TWW[t]) * T_HP_VL_2) + (m.HP_off[t] * 0))
    model.Operation_Temp = Constraint(time, rule=Operation_Temp, name='Operation_Temp')

    # Calculation of actual Q_HP depending on mode: [W]
    def Actual_Q_HP(m, t):
        return(m.Q_HP[t] == (m.HP_mode1[t] + m.HP_mode2[t] + m.HP_TWW[t]) * m.Q_HP_Unreal[t] + (m.HP_off[t] * 0))
    model.Actual_Q_HP = Constraint(time, rule=Actual_Q_HP, name='Actual_Q_HP')

    def Limit_T_Sto1(m,t):
        return(m.HP_mode1[t] * m.T_Sto[t] <= T_HP_VL_1)
    model.Limit_T_Sto1 = Constraint(time, rule=Limit_T_Sto1, name='Limit_T_Sto1')

    def Limit_T_Sto2(m, t):
        return (m.HP_mode2[t] * m.T_Sto[t] <= T_HP_VL_2)
    model.Limit_T_Sto2 = Constraint(time, rule=Limit_T_Sto2, name='Limit_T_Sto')

    def Heat_Power_HP(m, t):
        return (m.Q_HP_Unreal[t] == m_flow_HP * c_w_water * m.d_Temp_HP[t] * time_step)
    model.Heat_Power_HP = Constraint(time, rule=Heat_Power_HP, name='Heat_Power_HP')

    def Limit_Temp_Change_HP(m, t):
        return(m.d_Temp_HP[t] <= T_Spreiz_HP)
    model.Limit_Temp_Change_HP = Constraint(time, rule=Limit_Temp_Change_HP, name='Limit_Temp_Change_HP')

    def Temp_Change_Not_Zero(m, t):
        return(m.d_Temp_HP[t] + m.HP_off[t] >= 0.01)
    model.Temp_Change_Not_Zero = Constraint(time, rule=Temp_Change_Not_Zero, name='Temp_Change_Not_Zero')

    # Constrain to Display the Mode: [-]
    def Display_HP_Mode(m,t):
        return (m.Mode[t] == (0 * m.HP_off[t]) + (1 * m.HP_mode1[t]) + (2 * m.HP_mode2[t]) + (3* m.HP_TWW[t]))
    model.Display_HP_Mode = Constraint(time, rule=Display_HP_Mode, name='Display_HP_Mode')

    # Demand of el. Power by HP depending on Mode: [W]
    def Power_from_HP(m, t):
        return (m.P_EL_HP[t] == (m.P_HP_1[t] * m.HP_mode1[t]) + (m.P_HP_2[t] * (m.HP_mode2[t] + m.HP_TWW[t])) + 0 * m.HP_off[t])
    model.Power_from_HP = Constraint(time, rule= Power_from_HP, name='Power_from_HP')

    # Calculation of theoretical el. Power demand from HP in Mode 1: [W]
    def Power_1(m,t):
        return (m.P_HP_1[t] == m.Q_HP[t] / (COP_1[t] * eta_HP))
    model.Power_1= Constraint(time, rule=Power_1, name='Power_1')

    # Calculation of theoretical el. Power demand from HP in Mode 2: [W]
    def Power_2(m, t):
        return(m.P_HP_2[t] == m.Q_HP[t] / (COP_2[t] * eta_HP))
    model.Power_2 = Constraint(time, rule=Power_2, name='Power_2')

    # Calculation of actual COP_Carnot: [-]
    def Cop_Carnot(m, t):
        return(m.COP_Carnot[t] == (1 - m.HP_off[t]) * (m.HP_mode1[t] * COP_1[t] + (m.HP_mode2[t] + m.HP_TWW[t]) * COP_2[t]))
    model.Cop_Carnot = Constraint(time, rule=Cop_Carnot, name='Cop_Carnot')

    # Calculation of actual COP: [-]
    def Cop_HP(m, t):
        return(m.COP_HP[t] == eta_HP *  ((1 - m.HP_off[t]) * (m.HP_mode1[t] * COP_1[t] + (m.HP_mode2[t] + m.HP_TWW[t]) * COP_2[t])))
    model.Cop_HP = Constraint(time, rule=Cop_HP, name='Cop_HP')


####################---3. Consumer System (Hou) ---####################

    def Set_Third_m_flow_Hou(m, t):
        return(m.m_flow_Hou[t] == m_flow_Hou * time_step)
    model.Set_Third_m_flow_Hou = Constraint(time, rule=Set_Third_m_flow_Hou, name='Set_Third_m_flow_Hou')

    def Limit_delta_Temp_Hou(m,t):
        return (m.d_Temp_Hou[t] <= T_Spreiz_Hou)
    model.Limit_delta_Temp_Hou = Constraint(time, rule=Limit_delta_Temp_Hou, name='Limit_delta_Temp_Hou')

    def Maximize_Q_Hou(m, t):
        return(m.Q_Hou[t] <= m.Q_Hou_Dem[t])
    model.Maximize_Q_Hou = Constraint(time, rule=Maximize_Q_Hou, name='Maximize_Q_Hou')

    def Maxmium_Heat_Flow_From_Storage(m ,t):
        return(m.Q_Hou[t]  <= m.Q_Sto_Power_max[t] * m.B_Hou[t])
    model.Maxmium_Heat_Flow_From_Storage = Constraint(time, rule=Maxmium_Heat_Flow_From_Storage, name='Maxmium_Heat_Flow_From_Storage')

    def Heat_Flow_back_to_Storage(m, t):
        return(m.Q_Hou[t] == m.m_flow_Hou[t] * c_w_water * m.d_Temp_Hou[t])
    model.Heat_Flow_back_to_Storage = Constraint(time, rule=Heat_Flow_back_to_Storage, name='Heat_Flow_back_to_Storage')

    def Penalty_Heat_Flow(m,t):
        return (m.Q_Hou[t] + m.Q_Penalty[t] == m.Q_Hou_Dem[t])
    model.Penalty_Heat_Flow = Constraint(time, rule=Penalty_Heat_Flow, name='Penalty_Heat_Flow')


####################---4. Storage System (Sto) ---####################

    # Calculation of Temperature in Storage in current time step: [K]
    def Temp_Sto(m, t):
        if t >= 1:
            return(((m.T_Sto[t] - m.T_Sto[t-1]) * m_Sto_water * c_w_water) * time_step / delta_t == ((m.Q_HP[t] * (1 - m.HP_TWW[t]))- m.Q_Hou[t] - m.Q_Sto_Loss[t]))
        else:
            if iter == 0:
                return(m.T_Sto[t] == T_Sto_Init)
            else:
                return(((m.T_Sto[t] - T_Sto_Init) * m_Sto_water * c_w_water) * time_step / delta_t == ((m.Q_HP[t] * (1 - m.HP_TWW[t]))- m.Q_Hou[t] - m.Q_Sto_Loss[t]))
    model.Temp_Sto = Constraint(time, rule=Temp_Sto, name='Temp_Sto')

    # Calculation of useable Energy in Storage [J] = [Ws] -> [Ws] * 3600 = [Wh]
    def Storage_Energy(m, t):
        return(m.Q_Sto_Energy[t] == m_Sto_water * c_w_water * (m.T_Sto[t] - T_Sto_Env) * time_step / 3600)
    model.Storage_Energy = Constraint(time, rule=Storage_Energy, name='Storage_Energy')

    # Calculation of Heat-Loss during storage time: [W]
    def Loss_Sto(m,t):
        return (m.Q_Sto_Loss[t] == U_Sto * A_Sto * (m.T_Sto[t] - T_Sto_Env) * time_step)
    model.Loss_Sto = Constraint(time, rule= Loss_Sto, name='Loss_Sto')

    # Maximum Power by Storage per hour: [Wh] ?
    def Maximum_Storage_Power(m, t):
        return(m.Q_Sto_Power_max[t] == m_Sto_water * c_w_water * (m.T_Sto[t] - (T_Sto_Ersatz- T_Spreiz_Hou)) * time_step / 3600)
    model.Maximum_Storage_Power = Constraint(time, rule=Maximum_Storage_Power, name='Maximum_Storage_Power')

#    def Storage_Power(m, t):
 #       return(m.Sto_Penalty[t] * (m.T_Sto[t] - (35 + 273.15)) == m.Q_Penalty[t] / (m_Sto_water * c_w_water))
  #  model.Storage_Power = Constraint(time, rule=Storage_Power, name='Storage_Power')

####################---5. Calculate HP_Mode depending on the TWW-Demand and Delivery Data---####################


    if options['Sto']['Type'] == 'Seperated':
    # Calculation of Heat-Loss in TWW-Storage: [W]
        def TWW_Loss(m, t):
            return (m.Q_TWW_Loss[t] == U_TWW * A_TWW * (m.T_TWW[t] - T_Sto_Env) * time_step)
        model.TWW_Loss = Constraint(time, rule=TWW_Loss, name='TWW_Loss')

        # Energy-Balance of TWW-Storage: [W]
        def TWW_Balance(m, t):
            if t >= 1:
                return ((m.T_TWW[t] - m.T_TWW[t - 1]) * m_TWW_water * c_w_water * time_step / delta_t == (m.Q_HP[t] * m.HP_TWW[t]) - m.Q_TWW_Dem[t] - m.Q_TWW_Loss[t])
            else:
                if iter == 0:
                    return (m.T_TWW[t] == T_TWW_Init)
                else:
                    return (((m.T_TWW[t] - T_TWW_Init) * m_Sto_water * c_w_water) * time_step / delta_t == (m.Q_HP[t] * m.HP_TWW[t]) - m.Q_TWW_Dem[t] - m.Q_TWW_Loss[t])
        model.TWW_Balance = Constraint(time, rule=TWW_Balance, name='TWW_Balance')

        # Energy in TWW-Storage [W]
        def Maximize_Flow_of_TWW(m, t):
            return (m_TWW_water * c_w_water * (m.T_TWW[t] - T_TWW_Min) * time_step/ (delta_t) == m.Q_TWW_Max[t])
        model.Maximize_Flow_of_TWW = Constraint(time, rule=Maximize_Flow_of_TWW, name='Maximize_Flow_of_TWW')

        # Energy in TWW-Storage always higher than Demand [W]
        def Demand_Smaller_Than_TWW_Energy(m, t):
            return (m.Q_TWW_Dem[t] <= m.Q_TWW_Max[t])
        model.Demand_Smaller_Than_TWW_Energy = Constraint(time, rule=Demand_Smaller_Than_TWW_Energy, name='Demand_Smaller_Than_TWW_Energy')

        # Temeperature in TWW-Storage never below T_TWW_min: [K]
        def Minimize_T_TWW(m, t):
            return (m.T_TWW[t] >= T_TWW_Min)
        model.Minimize_T_TWW = Constraint(time, rule=Minimize_T_TWW, name='Minimize_T_TWW')

        # Temeperature in TWW-Storage never above T_TWW_min: [K]
        def Maximize_T_TWW(m, t):
            return (m.T_TWW[t] <= T_HP_VL_2)
        model.Maximize_T_TWW = Constraint(time, rule=Maximize_T_TWW, name='Maximize_T_TWW')

        # Import TWW- Demand
        def TWW_Demand_Import(m, t):
            return (m.Q_TWW_Dem[t] == Q_TWW_Dem[t + start_time] * time_step)
        model.TWW_Demand_Import = Constraint(time, rule=TWW_Demand_Import, name='TWW_Demand_Import')

    else:
        def TWW_Balance(m, t):
                return (m.T_TWW[t] == T_TWW_Init)
        model.TWW_Balance = Constraint(time, rule=TWW_Balance, name='TWW_Balance')

        def TWW_Loss(m, t):
            return (m.Q_TWW_Loss[t] == 0)
        model.TWW_Loss = Constraint(time, rule=TWW_Loss, name='TWW_Loss')

        def HP_TWW_off(m, t):
            return(m.HP_TWW[t] == 0)
        model.HP_TWW_off = Constraint(time, rule=HP_TWW_off, name='HP_TWW_off')

        def Smth_for_Q_Max(m,t):
            return(m.Q_TWW_Max[t] == 50)
        model.Smth_for_Q_Max = Constraint(time, rule=Smth_for_Q_Max, name='Smth_for_Q_Max')

        # Import TWW- Demand
        def TWW_Demand_Import(m, t):
            return (m.Q_TWW_Dem[t] == 0)

        model.TWW_Demand_Import = Constraint(time, rule=TWW_Demand_Import, name='TWW_Demand_Import')







####################---6. Linking of all Systems ---####################

    def power_balance(m, t):
        return(m.P_EL[t] == (m.P_EL_Dem[t] + m.P_EL_HP[t] - m.P_PV[t]))
    model.power_balance = Constraint(time, rule = power_balance, name = 'Power_balance')

    def Define_Feed_Binary(m, t):
        return (m.P_EL[t] * m.No_Feed_In[t] >= 0)
    model.Define_Feed_Binary = Constraint(time, rule= Define_Feed_Binary, name='Define_Feed_Binary')

####################---7. Calculation of Costs ---####################

    # Calculation of Cost for Power: [€]
    def Cost_for_Power(m, t):
        return (m.c_el_power[t] == m.No_Feed_In[t] * c_grid[t + start_time] * m.P_EL_Dem[t] )
    model.Cost_for_Power = Constraint(time, rule= Cost_for_Power, name= 'Cost_for_Power')

    def Cost_for_HP_Power(m, t):
        return(m.c_heat_power[t] == c_grid[t + start_time] * m.P_EL_HP[t])
    model.Cost_for_HP_Power = Constraint(time, rule=Cost_for_HP_Power, name='Cost_for_HP_Power')

    def Real_Power_Cost(m, t):
        return(m.c_el_cost_ch == sum(m.c_heat_power[t] + m.c_el_power[t] - m.c_revenue[t] for t in sum_control))
    model.Real_Power_Cost = Constraint(time, rule=Real_Power_Cost, name='Real_Power_Cost')

    # Calculation of Revenue for PV-Power: [€]
    def Revenue_for_Power(m, t):
        return (m.c_revenue[t] == (1 - m.No_Feed_In[t]) * c_payment * m.P_EL[t])
    model.Revenue_for_Power = Constraint(time, rule=Revenue_for_Power, name='Revenue_for_Power')

    # Calculation of Penatly-Costs due to Discomfort: [€]
    def Costs_of_Penalty(m, t):
        return (m.c_penalty[t] == m.Q_Penalty[t] * c_comfort)
    model.Costs_of_Penalty = Constraint(time, rule=Costs_of_Penalty, name='Costs_of_Penalty')

    def Costs_in_timestep(m,t):
        return (m.c_cost[t] == m.c_el_power[t] + m.c_revenue[t] + m.c_penalty[t] + m.c_heat_power[t])
    model.Costs_in_timestep = Constraint(time, rule=Costs_in_timestep, name='Costs_in_timestep')

    # Calculation of sum of all costs per control-horizon: [€]
    def Cost_in_Prediction_horizon(m, t):
        return (m.costs_total_ph == sum(m.c_el_power[t] + m.c_heat_power[t] + m.c_revenue[t] + m.c_penalty[t] for t in time))
    model.Cost_in_Prediction_horizon = Constraint(time, rule=Cost_in_Prediction_horizon, name ='Cost_in_Prediction_horizon')

    def Unreal_Cost_in_Control_horizon(m, t):
        return(m.costs_total_ch == sum(m.c_el_power[t] + m.c_heat_power[t] + m.c_revenue[t] + m.c_penalty[t] for t in sum_control))
    model.Unreal_Cost_in_Control_horizon = Constraint(time, rule=Unreal_Cost_in_Control_horizon, name='Unreal_Cost_in_Control_horizon')

####################---8. Zielfunktion ---####################

    def objective_rule(m):
        return (m.costs_total_ph)
    model.total_costs = Objective(rule = objective_rule, sense = minimize, name = 'Minimize total costs')

####################--- 8. Set Up of Solver ---####################

    solver = SolverFactory('gurobi')
    solver.options['Presolve'] = 1
    solver.options['mipgap'] = options['Solve']['MIP_gap']
    solver.options['TimeLimit'] = options['Solve']['TimeLimit']
    solver.options['DualReductions'] = 0

    resultate = solver.solve(model)

    if (resultate.solver.status==SolverStatus.ok) and (resultate.solver.termination_condition==TerminationCondition.optimal):
        model.display()
    elif (resultate.solver.termination_condition==TerminationCondition.infeasible or resultate.solver.termination_condition==TerminationCondition.other):
        print('Model is infeasible. Check Constraints')
    else:
        print('Solver status is :',resultate.solver.status)
        print('TerminationCondition is:', resultate.solver.termination_condition)


    res_control_horizon = {
        'Q_Sto'             : [],
        'Q_HP'              : [],
        'Q_Hou_Input'       : [],
        'Q_Hou_Dem'         : [],
        'Q_Hou'             : [],
        'Q_Sto_Loss'        : [],
        'Q_Penalty'         : [],
        'Q_Sto_Energy'      : [],
        'Q_Sto_Power'       : [],
        'Q_Sto_Power_max'   : [],
        'Q_HP_Unreal'       : [],
        'P_EL'              : [],
        'P_EL_HP'           : [],
        'P_EL_Dem'          : [],
        'P_PV'              : [],
        'P_HP_1'            : [],
        'P_HP_2'            : [],
        'T_Air_Input'       : [],
        'T_Air'             : [],
        'T_Sto'             : [],
        'T_HP_VL'           : [],
        'T_HP_RL'           : [],
        'T_Hou_VL'          : [],
        'T_Hou_RL'          : [],
        'T_Mean'            : [],
        'T_Sto_Init'        : [],
        'total_costs_ph'    : [],
        'c_grid'            : [],
        'c_el_power'        : [],
        'c_heat_power'      : [],
        'c_penalty'         : [],
        'c_revenue'         : [],
        'c_cost'            : [],
        'c_el_cost_ch'      : [],
        'total_costs_ch'    : [],
        'HP_off'            : [],
        'HP_mode1'          : [],
        'HP_mode2'          : [],
        'HP_TWW'            : [],
        'Mode'              : [],
        'No_Feed_In'        : [],
        'COP_Carnot'        : [],
        'COP_HP'            : [],
        'COP_1'             : [],
        'COP_2'             : [],
        'd_Temp_HP'         : [],
        'd_Temp_Hou'        : [],
        'T_TWW'             : [],
        'Q_TWW_Max'         : [],
        'Q_TWW_Dem'         : [],
        'Q_TWW_Loss'        : [],
        }

    status = 'feasible'
    results_horizon = int((params['control_horizon'] / params['time_step']))
    print('Results_Horizont ist:',  results_horizon)
    for t in range(results_horizon):
        if status == 'infeasible':
            for res in res_control_horizon:
                res_control_horizon[res].append(0)


#        res_control_horizon['solving_time'].append(opti_end_time)
        res_control_horizon['Q_HP'].append(round(value(model.Q_HP[t]), 1))
        res_control_horizon['Q_Hou_Input'].append(round(Q_Hou_Input[t+start_time], 2))
        res_control_horizon['Q_Hou_Dem'].append(round(value(model.Q_Hou_Dem[t]), 2))
        res_control_horizon['Q_Hou'].append(round(value(model.Q_Hou[t]), 2))
        res_control_horizon['Q_Penalty'].append(round(value(model.Q_Penalty[t]), 2))
        res_control_horizon['Q_Sto_Loss'].append(round(value(model.Q_Sto_Loss[t]), 2))
        res_control_horizon['Q_Sto_Energy'].append(round(value(model.Q_Sto_Energy[t]), 2))
        res_control_horizon['Q_HP_Unreal'].append(round(value(model.Q_HP_Unreal[t]), 2))
        res_control_horizon['Q_Sto_Power_max'].append(round(value(model.Q_Sto_Power_max[t]), 2))
        res_control_horizon['P_EL'].append(round(value(model.P_EL[t]), 2))
        res_control_horizon['P_EL_HP'].append(round(value(model.P_EL_HP[t]), 2))
        res_control_horizon['P_EL_Dem'].append(round(value(model.P_EL_Dem[t]), 2))
        res_control_horizon['P_PV'].append(round(value(model.P_PV[t]), 2))
        res_control_horizon['P_HP_1'].append(round(value(model.P_HP_1[t]), 2))
        res_control_horizon['P_HP_2'].append(round(value(model.P_HP_2[t]), 2))
        res_control_horizon['T_Air_Input'].append(round(T_Input[t], 2))
        res_control_horizon['T_Air'].append(round(value(model.T_Air[t]), 2))
        res_control_horizon['T_Sto'].append(round(value(model.T_Sto[t]), 2))
        res_control_horizon['T_HP_VL'].append(round(value(model.T_HP_VL[t]), 2))
        res_control_horizon['T_Mean'].append(round(T_Mean, 2))
        res_control_horizon['total_costs_ph'].append(round(value(model.costs_total_ph)  ,4))
        res_control_horizon['total_costs_ch'].append(round(value(model.costs_total_ch)  ,4))
        res_control_horizon['c_el_power'].append(round(value(model.c_el_power[t]), 4))
        res_control_horizon['c_heat_power'].append(round(value(model.c_heat_power[t]), 4))
        res_control_horizon['c_penalty'].append(round(value(model.c_penalty[t]), 4))
        res_control_horizon['c_revenue'].append(round(value(model.c_revenue[t]), 4))
        res_control_horizon['c_grid'].append(c_grid[t] * 1000)
        res_control_horizon['c_cost'].append(round(value(model.c_cost[t]), 2))
        res_control_horizon['HP_off'].append(int(value(model.HP_off[t])))
        res_control_horizon['HP_mode1'].append(int(value(model.HP_mode1[t])))
        res_control_horizon['HP_mode2'].append(int(value(model.HP_mode2[t])))
        res_control_horizon['HP_TWW'].append(int(value(model.HP_TWW[t])))
        res_control_horizon['Mode'].append(round(value(model.Mode[t])))
        res_control_horizon['No_Feed_In'].append(int(value(model.No_Feed_In[t])))
        res_control_horizon['COP_Carnot'].append(round(value(model.COP_Carnot[t]), 3))
        res_control_horizon['COP_HP'].append(round(value(model.COP_HP[t]), 3))
        res_control_horizon['COP_1'].append(round(COP_1[t], 3))
        res_control_horizon['COP_2'].append(round(value(COP_2[t]), 3))
        res_control_horizon['d_Temp_HP'].append(round(value(model.d_Temp_HP[t]), 1))
        res_control_horizon['d_Temp_Hou'].append(round(value(model.d_Temp_Hou[t]), 1))
        res_control_horizon['c_el_cost_ch'].append(round(value(model.c_el_cost_ch), 2))
        res_control_horizon['T_TWW'].append(round(value(model.T_TWW[t]), 2))
        res_control_horizon['Q_TWW_Max'].append(round(value(model.Q_TWW_Max[t]), 2))
        res_control_horizon['Q_TWW_Dem'].append(int(value(model.Q_TWW_Dem[t])))
        res_control_horizon['Q_TWW_Loss'].append(int(value(model.Q_TWW_Loss[t])))



#    model.display
    model.pprint()

    return res_control_horizon