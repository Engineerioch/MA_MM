from __future__ import division
import gurobipy as gp
import math

# Set parameters
def runGPMPC(params, options, eco, time_series, devs, end):

#################### I: Set Parameters #######################

    res = params['time_step']       # Timesteps per Hour: 1 -> 1h is the range of one time-step
    time = [i for i in range(0, params['prediction_horizon'] * res)]    #Todo: Beschreiben
    init = [-1]
    init_time = init + time

# Load Input Data from parameters -> time_series
    T_Air       = [time_series['T_Air'][math.ceil(params['start_time'] + ( t + 1 - res) / res)] for t in time]
    P_EL_Dem    = [time_series['P_EL_Dem'][math.ceil(params['start_time'] + ( t + 1 - res) / res)] for t in time]
    Q_Hou_Dem   = [time_series['Q_Hou_Dem'][math.ceil(params['start_time'] + ( t + 1 - res) / res)] for t in time]
    P_PV        = [time_series['P_PV'][math.ceil(params['start_time'] + ( t + 1 - res) / res)] for t in time]


# Set economic parameter - set in parameter.py -> eco
#    c_grid_var          =   time_series['c_grid_var']                # [Euro/kWh]   Variable grid charges Stromnetze Berlin
#    c_grid              =   eco['costs']['c_grid_dem']                  # [Euro/kWh]   Grid charges with fix Price Berlin
    c_payment           =   eco['costs']['c_payment']                   # [Euro/kWh]    Feed in tariff

    if options['Tariff']['Variable']:
        c_grid        =   time_series['c_grid_var']
    else:
        c_grid        =   eco['costs']['c_grid_dem']




# Set PV profile
    P_PV_Max            =   devs['PV']['n_mod'] * devs['PV']['P_PV_Module']  # [kW] maximum Sum Power of all PV-Modules
    P_PV_Min            =   devs['PV']['P_PV_Min']



# Set Heat storage parameters
    T_Sto_max           =   devs['Sto']['T_Sto_max']
    T_Sto_min           =   devs['Sto']['T_Sto_min']
    m_Sto_water         =   devs['Sto']['Volume'] * devs['Nature']['Roh_water']
    T_Sto_Env           =   devs['Sto']['T_Sto_Env']
    U_Sto               =   devs['Sto']['U_Sto']
    Cap_Sto             =   devs['Sto']['Volume'] * devs['Nature']['c_w_water']
    T_Kalt              =   devs['Sto']['T_Kalt']
    A_Sto               =   devs['Sto']['A_Sto']
    T_Sto_Init          =   devs['Sto']['T_Sto_Init']
    Q_Sto_min           =   m_Sto_water * devs['Nature']['c_w_water'] * T_Sto_min
    Q_Sto_max           =   m_Sto_water * devs['Nature']['c_w_water'] * T_Sto_max


# Set Consumer parameter
    T_Hou_delta_max     =   devs['Hou']['T_Hou_delta_max']
    m_flow_Hou          =   devs['Hou']['m_flow_Hou']


# Set Heat Pump parameters
    m_flow_HP           =   devs['HP']['m_flow_HP']
    eta_HP              =   devs['HP']['eta_HP']                        # [-] Gütegrad HP
    Q_HP_Max            =   devs['HP']['Q_HP_Max']                      # [W] Maximum Power of Heat Pump
    Q_HP_Min            =   devs['HP']['Q_HP_Min']                      # [W] Minimum Power of Heat Pump
    T_HP_VL_1           =   devs['HP']['T_HP_VL_1']                     # [K] Vorlauftemperatur der Wärmepumpe im Modus 1, = 70°C
    T_HP_VL_2           =   devs['HP']['T_HP_VL_2']                     # [K] VOrlauftemperatur der Wärmepumpe im Modus 2, = 35°C
    T_HP_VL_Init        =   options['Initial']['T_HP_VL_Init']


# Set Natural Parameters
    c_w_water           =   devs['Nature']['c_w_water']


################### II: Set upper and lower bounds


bounds_low = {
    'COP_Carnot': T_HP_VL_1 / (T_HP_VL_1 - (273.15 - 20)),
    # Minimaler Carnot-COP bei maximaler Vorlauftemperatur und minimaler Außentemperatur (min in Wetterdaten =-17.2 -> deshalb -20 als Minimaltemperatur gewählt
    'COP_HP': T_HP_VL_1 / (T_HP_VL_1 - (273.15 - 20)) * eta_HP,  # Minimaler Carnot-COP mal Gütezahl ergbit HP-COP
    'P_EL': -float('inf'),
    'P_EL_HP': 0.0,
    'Q_HP': 0.0,
    'Q_HP_Out': 0,  # m_flow_HP * c_w_water * T_HP_VL_2,
    'Q_HP_In': 0,  # m_flow_HP * c_w_water * (T_Sto_min - 2),
    'Q_Hou_In': m_flow_Hou * c_w_water * (T_Sto_min + 2),
    'Q_Hou_Out': m_flow_Hou * c_w_water * T_Sto_Env,
    'Q_Sto': m_Sto_water * c_w_water * T_Kalt,
    'Q_Sto_Loss': 0.0,
    # Minimaler Verlustwärmestrom ist 0. wenn die Speichertemperatur gleich der Umgebungstemperatur ist
    'Q_Hou': 0.0,
    'T_HP_RL': T_Sto_min - 2,
    'T_HP_VL': 0,
    'T_Hou_RL': T_Kalt,
    'T_Hou_VL': T_Sto_min + 2,
    'T_Sto': T_Sto_min,
    'c_cost': 0,
    'c_earning': - float('inf'),
}

bounds_up = {
    'COP_Carnot': T_HP_VL_2 / (T_HP_VL_2 - (40 + 273.15)),
    # Maximaler Carnot-COP bei minimaler Vorlauftemperatur und maximaler Außentemperatur (max in Wetterdaten = 37 -> deshalb 40°C als Maximaltemperatur gewählt
    'COP_HP': T_HP_VL_2 / (T_HP_VL_2 - (40 + 273.15)) * eta_HP,
    'P_EL': float('inf'),
    'P_EL_HP': float('inf'),
    'Q_HP': 10000.0,  # Von Modell vorgegeben
    'Q_HP_In': m_flow_HP * c_w_water * (T_Sto_max - 2),
    'Q_HP_Out': m_flow_HP * c_w_water * (T_HP_VL_1),
    'Q_Hou_In': m_flow_Hou * c_w_water * (T_Sto_max + 2),
    'Q_Hou_Out': m_flow_Hou * c_w_water * (T_Sto_max + 2),
    'Q_Sto': m_Sto_water * c_w_water * T_Sto_max,
    'Q_Sto_Loss': U_Sto * c_w_water * (T_Sto_max - T_Kalt),
    # Maximaler Verlustwärmestrom wenn die Temperaturdifferenz maximal ist
    'Q_Hou': 10000.0,
    # Wird von Q_Hou_Dem eingelesen und als Soft-Constraint behandelt Annahme Q_Hou_Max = 10000 ,weil 9000W die maximale Q_Hou_Dem ist.
    'T_HP_RL': T_Sto_max - 2,
    'T_HP_VL': T_HP_VL_1,
    'T_Hou_RL': T_Sto_max + 2,
    'T_Hou_VL': T_Sto_max + 2,
    'T_Sto': T_Sto_max,
    'c_cost': float('inf'),
    'c_earning': 0,
}


################### II: Initialize Model


    model = gp.Model("Optimierung")
    model.update()

    P_EL        = model.addVars(time, vtype = "C", lb = bounds_low['P_EL'], ub= bounds_up['P_EL'],          name = "P_EL")
    P_EL_HP     = model.addVars(time, vtype="C", lb = bounds_low['P_EL_HP'], ub= bounds_up['P_EL_HP'],      name = "P_EL_HP")
    Q_Sto       = model.addVars(time, vtype="C", lb = bounds_low['Q_Sto'], ub= bounds_up['Q_Sto'],          name = "Q_Sto")
    Q_HP_Out    = model.addVars(time, vtype="C", lb = bounds_low['Q_HP_Out'], ub= bounds_up['Q_HP_Out'],    name = "Q_HP_Out")
    Q_HP_In     = model.addVars(time, vtype="C", lb = bounds_low['Q_HP_In'], ub= bounds_up['Q_HP_In'],      name = "Q_HP_In")
    Q_Hou_Out   = model.addVars(time, vtype="C", lb = bounds_low['Q_Hou_Out'], ub= bounds_up['Q_Hou_Out'],  name = "Q_Hou_Out")
    Q_Hou_In    = model.addVars(time, vtype="C", lb = bounds_low['Q_Hou_In'], ub= bounds_up['Q_Hou_In'],    name = "Q_Hou_In")
    Q_Sto_Loss  = model.addVars(time, vtype="C", lb = bounds_low['Q_Sto_Loss'], ub= bounds_up['Q_Sto_Loss'],name = "Q_Sto_Loss")
    Q_Hou       = model.addVars(time, vtype="C", lb = bounds_low['Q_Hou'], ub= bounds_up['Q_Hou'],          name = "Q_Hou")
    Q_HP        = model.addVars(time, vtype="C", lb = bounds_low['Q_HP'], ub= bounds_up['Q_HP'],            name = "Q_HP")
    T_HP_VL     = model.addVars(time, vtype="C", lb = bounds_low['T_HP_VL'], ub= bounds_up['T_HP_VL'],      name = "T_HP_VL")
    T_HP_RL     = model.addVars(time, vtype="C", lb = bounds_low['T_HP_RL'], ub= bounds_up['T_HP_RL'],      name = "T_HP_RL")
    T_Hou_VL    = model.addVars(time, vtype="C", lb = bounds_low['T_Hou_VL'], ub= bounds_up['T_Hou_VL'],    name = "T_Hou_VL")
    T_Hou_RL    = model.addVars(time, vtype="C", lb = bounds_low['T_Hou_RL'], ub= bounds_up['T_Hou_RL'],    name = "T_Hou_RL")
    COP_HP      = model.addVars(time, vtype="C", lb = bounds_low['COP_HP'], ub= bounds_up['COP_HP'],        name = "COP_HP")
    COP_Carnot  = model.addVars(time, vtype="C", lb = bounds_low['COP_Carnot'], ub= bounds_up['COP_Carnot'],name = "COP_Carnot")
    T_Sto       = model.addVars(time, vtype="C", lb = bounds_low['T_Sto'], ub= bounds_up['T_Sto'],          name = "T_Sto")
    c_earning   = model.addVars(time, vtype="C", lb = bounds_low['c_earning'], ub= bounds_up['c_earning'],  name = "c_earning")
    c_cost      = model.addVars(time, vtype="C", lb = bounds_low['c_cost'], ub= bounds_up['c_cost'],        name = "c_cost")
    Feed_In     = model.addVars(time, vtype="B", name = "Feed_In")

    HP_off      = model.addVars(time, vtype= = "B", lb = 0.0, ub = 1.0, name = "HP_off")
    HP_mode1    = model.addVars(time, vtype= = "B", lb = 0.0, ub = 1.0, name = "HP_mode1")
    HP_mode2    = model.addVars(time, vtype= = "B", lb = 0.0, ub = 1.0, name = "HP_mode2")

    costs_total = model.addVar()

    model.setObjective(costs_total, gp.GRB.MINIMIZE)


    model.addConstr((P_EL[t] == P_EL_HP[t] + P_PV[t] + P_EL_Dem[t] for t in time), name = "Power_Balance")

    model.addConstr((Q_Sto[t] == m_Sto_water * c_w_water * T_), name ="Q_Content_Sto")
    model.addConstr((), name="storage_balance")
    model.addConstr((), name="Q_Sto_Temp")
    model.addConstr((), name="Storage_Loss")
    model.addConstr((), name="heat_from_HP")
    model.addConstr((), name="HP_mode_rule")
    model.addConstr((), name="Temp_VL_HP")
    model.addConstr((), name="Power_for_HP")
    model.addConstr((), name="CoP_HP")
    model.addConstr((), name="CoP_Carnot")
    model.addConstr((), name="Back_to_HP")
    model.addConstr((), name="Q_to_HP")
    model.addConstr((), name="Q_from_HP")
    model.addConstr((), name="Q_HP_sum")
    model.addConstr((), name="heat_use_House")
    model.addConstr((), name="total_Heat_to_House")
    model.addConstr((), name="total_Heat_from_House")
    model.addConstr((), name="Q_Hou_sum")
    model.addConstr((), name="Temperature_to_House")
    model.addConstr((), name="Power_Demand")
    model.addConstr((), name="Cost_for_Power")
    model.addConstr((), name="Return_for_Power")
    model.addConstr((), name="Cost_sum")


model.optimize()









#################### I: Set Parameters #######################
#################### I: Set Parameters #######################
#################### I: Set Parameters #######################
#################### I: Set Parameters #######################
#################### I: Set Parameters #######################
#################### I: Set Parameters #######################
#################### I: Set Parameters #######################
#################### I: Set Parameters #######################
