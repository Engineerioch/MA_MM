from typing import Union, Any

# Optimization of ExtractingRuleStudy
from pyomo.environ import *
from pyomo.util.infeasible import log_infeasible_constraints
from pyomo.opt import UnknownSolver
from pyomo.opt.base.solvers import SolverFactoryClass
import time as read_time
import sys
import copy
import time as read_time


def run_MPC(params, options, eco, time_series, devs, end):

# Set parameter
    dt                  =   params['time_step']
    start_time          =   params['start_time']
    prediction_horizon  =   params['prediction_horizon']
    time_range          =   range(int(params['prediction_horizon'] * (1/params['time_step'])) +1)
    time                =   range(int(params['prediction_horizon'] / params['time_step']))
    delta_t             =   params['time_step'] * 3600                                        # time Step in seconds

# Set economic parameter - set in parameter.py -> eco
#    c_grid_var          =   time_series['c_grid_var']                # [Euro/kWh]   Variable grid charges Stromnetze Berlin
#    c_grid              =   eco['costs']['c_grid_dem']                  # [Euro/kWh]   Grid charges with fix Price Berlin
    c_payment           =   eco['costs']['c_payment']                   # [Euro/kWh]    Feed in tariff

    if options['Tariff']['Variable']:
        c_grid        =   time_series['c_grid_var']
    else:
        c_grid        =   eco['costs']['c_grid_dem']




# Set PV profile
    P_PV                =   time_series['P_PV']
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
    P_EL_Dem            =   time_series['P_EL_Dem']
    m_flow_Hou          =   devs['Hou']['m_flow_Hou']
    Q_Hou_Dem           =   time_series['Q_Hou_Dem']                    # [W] Heat Demand of House


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
    T_Input             =   time_series['T_Air']  + 273.15            # [K]  Außentemperatur
#Test BigM
    BigM                = 1000


#######################---Set initial values---#######################
# Todo: inits für jeden Fall; hier nur wenn die WP am Anfang aus ist -> Eigentlich sollte es ja so sein, \
# Todo: dass alle 3 Modi am Anfang einer Optimierung möglich sein können.
    initials = {
        'P_EL'      : P_EL_Dem[params['start_time']] - P_PV[params['start_time']],
        'P_EL_HP'   : 0,
        'P_EL_Dem'  : P_EL_Dem[start_time],
        'P_PV'      : P_PV[start_time],
        'Q_Sto'     : m_Sto_water * c_w_water * T_Sto_Init,
        'Q_HP'      : 0,
        'Q_HP_Out'  : 0,
        'Q_HP_In'   : 0,
        'Q_Hou_In'  : m_flow_Hou * c_w_water * (T_Sto_Init + 2.0),
        'Q_Hou_Out' : m_flow_Hou * c_w_water * (T_Sto_Init + 2.0) - Q_Hou_Dem[params['start_time']],
        'Q_Sto_Loss': U_Sto * A_Sto * (T_Sto_Init - T_Sto_Env),
        'Q_Hou'     : Q_Hou_Dem[start_time],
        'T_HP_VL'   : T_HP_VL_Init,
        'T_HP_RL'   : 33.0 + 273.15,
        'T_Hou_VL'  : T_Sto_Init + 2.0,
        'T_Hou_RL'  : (T_Sto_Init + 2.0) - Q_Hou_Dem[params['start_time']] / (m_flow_Hou * c_w_water * 1000),
        'T_Air'     : T_Input[start_time],
        'COP_HP'    : T_HP_VL_1 / (T_HP_VL_1 - (273.15 - 20)) * eta_HP,     # Minimum values as Inits as the corresponding formulas don't take these values
        'COP_Carnot': T_HP_VL_1 / (T_HP_VL_1 - (273.15 - 20)),              # Minimum values as Inits as the corresponding formulas don't take these valuesy
        'T_Sto'     : T_Sto_Init,
        'c_earning' : 0,
        'c_cost'    : P_EL_Dem[params['start_time'] * c_grid],  #Todo: If Bedingung für den Variablen Stromtarif
#        'c_revenue' : 0,
        'Feed_In'   : 0,
        'HP_off'    : 1,
        'HP_mode1'  : 0,
        'HP_mode2'  : 0,
    }

    bounds_low = {
        'COP_Carnot'    : T_HP_VL_1 / (T_HP_VL_1 - (273.15 - 20)),              # Minimaler Carnot-COP bei maximaler Vorlauftemperatur und minimaler Außentemperatur (min in Wetterdaten =-17.2 -> deshalb -20 als Minimaltemperatur gewählt
        'COP_HP'        : T_HP_VL_1 / (T_HP_VL_1 - (273.15 - 20)) * eta_HP,     # Minimaler Carnot-COP mal Gütezahl ergbit HP-COP
        'P_EL'          : -float('inf'),
        'P_EL_HP'       : 0.0,
        'Q_HP'          : 0.0,
        'Q_HP_Out'      : 0, #m_flow_HP * c_w_water * T_HP_VL_2,
        'Q_HP_In'       : 0, #m_flow_HP * c_w_water * (T_Sto_min - 2),
        'Q_Hou_In'      : m_flow_Hou * c_w_water * (T_Sto_min + 2),
        'Q_Hou_Out'     : m_flow_Hou * c_w_water * T_Sto_Env,
        'Q_Sto'         : m_Sto_water * c_w_water * T_Kalt,
        'Q_Sto_Loss'    : 0.0,                                            # Minimaler Verlustwärmestrom ist 0. wenn die Speichertemperatur gleich der Umgebungstemperatur ist
        'Q_Hou'         : 0.0,
        'T_HP_RL'       : T_Sto_min - 2,
        'T_HP_VL'       : 0,
        'T_Hou_RL'      : T_Kalt,
        'T_Hou_VL'      : T_Sto_min + 2,
        'T_Sto'         : T_Sto_min,
        'c_cost'        : 0,
        'c_earning'     : - float('inf'),
    }

    bounds_up = {
        'COP_Carnot': T_HP_VL_2 / (T_HP_VL_2 - (40 + 273.15)),          # Maximaler Carnot-COP bei minimaler Vorlauftemperatur und maximaler Außentemperatur (max in Wetterdaten = 37 -> deshalb 40°C als Maximaltemperatur gewählt
        'COP_HP'    : T_HP_VL_2 / (T_HP_VL_2 - (40 + 273.15)) * eta_HP,
        'P_EL'      : float('inf'),
        'P_EL_HP'   : float('inf'),
        'Q_HP'      : 10000.0,                                            #Von Modell vorgegeben
        'Q_HP_In'   : m_flow_HP * c_w_water * (T_Sto_max -2),
        'Q_HP_Out'  : m_flow_HP * c_w_water * (T_HP_VL_1),
        'Q_Hou_In'  : m_flow_Hou * c_w_water * (T_Sto_max + 2),
        'Q_Hou_Out' : m_flow_Hou * c_w_water * (T_Sto_max + 2),
        'Q_Sto'     : m_Sto_water * c_w_water * T_Sto_max,
        'Q_Sto_Loss': U_Sto * c_w_water * (T_Sto_max - T_Kalt),         # Maximaler Verlustwärmestrom wenn die Temperaturdifferenz maximal ist
        'Q_Hou'     : 10000.0,                                          # Wird von Q_Hou_Dem eingelesen und als Soft-Constraint behandelt Annahme Q_Hou_Max = 10000 ,weil 9000W die maximale Q_Hou_Dem ist.
        'T_HP_RL'   : T_Sto_max - 2,
        'T_HP_VL'   : T_HP_VL_1,
        'T_Hou_RL'  : T_Sto_max + 2,
        'T_Hou_VL'  : T_Sto_max + 2,
        'T_Sto'     : T_Sto_max,
        'c_cost'    : float('inf'),
        'c_earning' : 0,
    }






#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Übergeben der Variablen an das Model
# Initialize model
#    model = AbstractModel()
    model = ConcreteModel()

    # Grid Interaction
    model.P_EL          = Var(time, within = Reals,             name = 'P_EL' ,         initialize = initials['P_EL'],      bounds=(bounds_low['P_EL'],bounds_up['P_EL']))
    model.P_EL_HP       = Var(time, within = NonNegativeReals,  name = 'P_EL_HP',       initialize = initials['P_EL_HP'],   bounds=(bounds_low['P_EL_HP'],bounds_up['P_EL_HP']))
    model.P_PV          = Var(time, within = Reals,             name = 'P_PV',          initialize = initials['P_PV'])#,      bounds=(bounds_low[''],bounds_up['']))
    model.P_EL_Dem      = Var(time, within = Reals,             name = 'P_EL_Dem',      initialize = initials['P_EL_Dem'])#,  bounds=(bounds_low[''],bounds_up['']))

#    model.Q_Hou_Dem     = Param(time, within = Reals, name = 'Q_Hou_Dem'),
    model.Q_Sto         = Var(time, within = Reals,             name = 'Q_Sto',         initialize = initials['Q_Sto'],     bounds=(bounds_low['Q_Sto'],bounds_up['Q_Sto'])) # initialize=m_Sto_water*c_w_water*(35 + 273.15))
    model.Q_HP_Out      = Var(time, within = NonNegativeReals,  name = 'Q_HP_Out',      initialize = initials['Q_HP_Out'],  bounds=(bounds_low['Q_HP_Out'],bounds_up['Q_HP_Out']))
    model.Q_HP_In       = Var(time, within = NonNegativeReals,  name = 'Q_HP_In',       initialize = initials['Q_HP_In'],   bounds=(bounds_low['Q_HP_In'],bounds_up['Q_HP_In']))
    model.Q_Hou_In      = Var(time, within = NonNegativeReals,  name = 'Q_Hou_In',      initialize = initials['Q_Hou_In'],  bounds=(bounds_low['Q_Hou_In'],bounds_up['Q_Hou_In']))
    model.Q_Hou_Out     = Var(time, within = NonNegativeReals,  name = 'Q_Hou_Out',     initialize = initials['Q_Hou_Out'], bounds=(bounds_low['Q_Hou_Out'],bounds_up['Q_Hou_Out']))
    model.Q_Sto_Loss    = Var(time, within = Reals,             name = 'Q_Sto_Loss',    initialize = initials['Q_Sto_Loss'],bounds=(bounds_low['Q_Sto_Loss'],bounds_up['Q_Sto_Loss']))
    model.Q_Hou         = Var(time, within = Reals,             name = 'Q_Hou',         initialize = initials['Q_Hou'],     bounds=(bounds_low['Q_Hou'],bounds_up['Q_HP_In']))
    model.Q_HP          = Var(time, within = NonNegativeReals,  name = 'Q_HP',          initialize = initials['Q_HP'],      bounds=(bounds_low['Q_HP'],bounds_up['Q_HP']))
#    model.Q_mode1       = Var(time, within = NonNegativeReals,  name = 'Q_mode1',       initialize = 0, bounds=(0.0, 10000))
#    model.Q_mode2       = Var(time, within = NonNegativeReals,  name = 'Q_mode2',       initialize = 0,                bounds=(0.0, 10000))
    model.T_HP_VL       = Var(time, within = NonNegativeReals,  name = 'T_HP_VL',       initialize = initials['T_HP_VL'],   bounds=(bounds_low['T_HP_VL'],bounds_up['T_HP_VL']))
    model.T_HP_RL       = Var(time, within = NonNegativeReals,  name = 'T_HP_RL',       initialize = initials['T_HP_RL'],   bounds=(bounds_low['T_HP_RL'],bounds_up['T_HP_RL']))
    model.T_Hou_VL      = Var(time, within = NonNegativeReals,  name = 'T_Hou_VL',      initialize = initials['T_Hou_VL'],  bounds=(bounds_low['T_Hou_VL'],bounds_up['T_Hou_VL'])) #bounds=(293.15, 343.15))
    model.T_Hou_RL      = Var(time, within = NonNegativeReals,  name = 'T_Hou_RL',      initialize = initials['T_Hou_RL'],  bounds=(bounds_low['T_Hou_RL'],bounds_up['T_Hou_RL'])) #bounds=(293.15, 343.15))
    model.T_Air         = Var(time, within = Reals,             name = 'T_Air',         initialize = initials['T_Air']) #,     bounds=(bounds_low[''],bounds_up['']))
    model.COP_HP        = Var(time, within = NonNegativeReals,  name = 'COP_HP',        initialize = initials['COP_HP'],    bounds=(bounds_low['COP_HP'],bounds_up['COP_HP']))
    model.COP_Carnot    = Var(time, within = NonNegativeReals,  name = 'COP_Carnot',    initialize = initials['COP_Carnot'],bounds=(bounds_low['COP_Carnot'],bounds_up['COP_Carnot']))
    model.T_Sto         = Var(time, within = NonNegativeReals,  name = 'T_Sto',         initialize = initials['T_Sto'],     bounds=(bounds_low['T_Sto'],bounds_up['T_Sto']))
    model.c_earning     = Var(time, within = NonPositiveReals,  name = 'c_earning',     initialize = initials['c_earning'], bounds=(bounds_low['c_earning'],bounds_up['c_earning'])) # Epeisevergütung pro Zeitschritt
    model.c_cost        = Var(time, within = NonNegativeReals,  name = 'c_cost',        initialize = initials['c_cost'],    bounds=(bounds_low['c_cost'],bounds_up['c_cost']))     # Stromkosten pro Zeitschritt
#    model.c_grid        = Var(time, within = Reals,             name = 'c_grid', initialize = )
#    model.c_total       = Var(time, within = Reals,             name = 'c_total', initialize =)
#    model.c_revenue     = Var(time, within = Reals,             name = 'c_revenue', initialize = initials['c_revenue'])   # Stromvergütung gesamt (reine Vergütung)
    model.costs_total   = Var(      within = Reals,             name = 'costs_total',   initialize=0)
    model.Feed_In       = Var(time, within=  Boolean,           name = 'Feed_In',       initialize= initials['Feed_In'])

    ##### Entscheidungsvariablen: Auswahl des Modus
    model.HP_off        = Var(time, within = Binary,            name = 'HP_off', initialize = 1)        # HP an oder aus; HP_off = 1 -> HP ist aus
    model.HP_mode1      = Var(time, within = Binary,          name = 'HP_mode1', initialize = 0)        # HP on, T_VL = 70 °C
    model.HP_mode2      = Var(time, within = Binary,           name = 'HP_mode2', initialize = 0)       # HP on, T_VL = 35°C
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Einführen der Nebenbedingungen
# Add Constraints to model
#######################---1. Import of PV- and Q_Hou_Dem Data and write that Data in Model Variables---#######################
###     1.1 Import of PV-Data -> [W]
    def Import_PV(m, t):
        return (m.P_PV[t] == P_PV[t + end])
    model.Import_PV = Constraint(time, rule=Import_PV, name='Import_PV')

###     1.2 Import of House Heat Demand -> [W]
    def Heat_to_House_equals_Demand(m, t):
        return (m.Q_Hou[t] >= Q_Hou_Dem[t + end])
    model.Heat_to_House_equals_Demand = Constraint(time, rule=Heat_to_House_equals_Demand, name=Heat_to_House_equals_Demand)

###     1.3 Import of Electrical Power Demand of House Power -> [W]
    def Power_Demand_In_House(m, t):
        return(m.P_EL_Dem[t] == P_EL_Dem[t + end])
    model.Power_Demand_In_House = Constraint(time, rule= Power_Demand_In_House, name= 'Power_Demand_In_House')

###     1.4 Import of Outside Temperature -> [K]
    def Temp_Outside(m, t):
        return(m.T_Air[t] == T_Input[t + end])
    model.Temp_Outside = Constraint(time, rule= Temp_Outside, name='Temp_Outside')

#####################################################################################################
#######################---2. Equations to describe the storage-system (Sto)---#######################
###     2.1 Content of Heat-Energy in the storage -> [W] == [kg] * [Ws/kgK] * [K] * [s]
    def Q_Content_Sto(m,t):
        return(m.Q_Sto[t] == m_Sto_water * c_w_water * (m.T_Sto[t] - T_Kalt) / delta_t)
    model.Q_Content_Sto = Constraint(time, rule= Q_Content_Sto, name= 'Q_Content_Sto')

###     2.2 Storage Heat Balance -> [W] = ([W] - [W] - [W] + [W] - [W])
            # Wärme die vom Speicher an die Wärmepumpe (RL) zurückfließt und an das Haus abgegeben wird als Minus, Wärme die von der Wärmepumpe und aus dem Haus an den Speicher fließt als plus
    def storage_balance(m,t):
        return(value(m.Q_Sto[t]) == (m.Q_HP_Out[t] - m.Q_HP_In[t] - m.Q_Hou_In[t] + m.Q_Hou_Out[t] - m.Q_Sto_Loss[t]))
    model.storage_balance = Constraint(time, rule = storage_balance, name = 'storage_balance')

###     2.3 Temperature in Storage -> [K] = [W] * [s] + [kg] * [Ws/kgK] * [K] + [W/m²K] * [m²] * [K] * [s] / [kg] * [Ws/kgK] + [W/m²K] * [m²] [s]
#[K] = [Ws] / [Ws/K] -> [K]
 #   def easy_storage_test(m, t):
 #       if t == 0:
 #           return (m.T_Sto[t] == 35 + 273.15)
 #       else:
 #           return (m.T_Sto[t] == ((m.Q_HP[t] - m.Q_Hou[t]) * delta_t + m_Sto_water * c_w_water * m.T_Sto[
 #               t - 1] + U_Sto * A_Sto * T_Sto_Env * delta_t) / (m_Sto_water * c_w_water + U_Sto * A_Sto * delta_t))
 #   model.easy_storage_test = Constraint(time, rule=easy_storage_test, name='easy_storage_test')

###     2.4 Definition of Storagetemperature -> [W] = [kg] * [Ws/kgK] * [K]
    def Q_Sto_Temp (m, t):
        if t >= 1:
            return(m.Q_Sto[t] == m_Sto_water * c_w_water * (value(m.T_Sto[t]) - value(m.T_Sto[t-1])) / delta_t)
        else:
            return(m.Q_Sto[t] == 0)
    model.Q_Sto_Temp = Constraint(time, rule = Q_Sto_Temp, name = 'Q_Sto_Temp')

###    2.5 Loss of Storage to Environment in House (No Heating Power resuls from this) -> [W] = [W/m²K] * [m²] * [K]
    def Storage_Loss(m, t):
        return (m.Q_Sto_Loss[t] == U_Sto * A_Sto * (value(m.T_Sto[t]) - T_Sto_Env))
    model.Storage_Loss = Constraint(time, rule=Storage_Loss, name='Storage_Loss')

######################################################################################################
#######################---3. Equations to describe the Heat Pump-System (HP)---#######################

###     3.1 Heat balance of Heat Pump depending on the Current mode -> [W] = [kg/s] * [Ws/kgK] * [K]
    def heat_from_HP(m, t):
        if value(m.HP_off[t]) == 1.0:
            return (m.Q_HP[t] == 0)                     # Power = 0 because Heat pump is off in Mode HP_off
        else:
            return(m.Q_HP[t] == m_flow_HP * c_w_water * (m.T_HP_VL[t] - m.T_HP_RL[t]))
    model.heat_from_HP = Constraint(time, rule = heat_from_HP, name = 'heat_from_HP')

###     3.2 Constraints for Binary Variables to descide if T_HP_VL = 70°C in Mode 1 or 35°C in Mode 2 or HP off -> [-]
    def HP_Mode_rule(m, t):
        return (m.HP_off[t] + m.HP_mode1[t] + m.HP_mode2[t] == 1.0)
    model.HP_Mode_rule = Constraint(time, rule=HP_Mode_rule, name='HP_Mode_rule')

###     3.3 Temperature from HP to Storage -> [K]
    def Temp_VL_HP(m, t):
        return (m.T_HP_VL[t] == T_HP_VL_1 * m.HP_mode1[t] + T_HP_VL_2 * m.HP_mode2[t] + 0 * m.HP_off[t])
    model.Temp_VL_HP = Constraint(time, rule=Temp_VL_HP, name='Temp_VL_HP')

###     3.4 Power demand of HP -> [W]
    def Power_for_HP(m, t):
        if value(m.HP_off[t]) != 0.0:
            return(m.P_EL_HP[t] == m.Q_HP[t] / 1) #m.COP_HP[t]) #todo COP_HP reinbekommen
        else:
            return(m.P_EL_HP[t] == 0.0)
    model.Power_for_HP = Constraint(time, rule = Power_for_HP, name = 'Power_for_HP')

###     3.5 Coefficient of Performance of HP -> [-]
    def CoP_HP(m, t):
        return(m.COP_HP[t]  == m.COP_Carnot[t] * eta_HP)
    model.CoP_HP = Constraint(time, rule = CoP_HP, name = 'CoP_HP')

###     3.6 Coefficient of Performance Carnot -> [-]
    def CoP_Carnot(m, t):
        if value(m.HP_off[t]) == 1:
            return (m.COP_Carnot[t] == 1)
        else:
            return(m.COP_Carnot[t] == m.T_HP_VL[t] / (m.T_HP_VL[t] - m.T_Air[t]))
    model.CoP_Carnot = Constraint(time, rule = CoP_Carnot, name = 'CoP_Carnot')

###     3.7 Modell temperature from Storage to HP -> [K]
    def Back_to_HP(m, t):
        return(m.T_HP_RL[t] == m.T_Sto[t] - 2)
    model.Back_to_HP = Constraint(time, rule = Back_to_HP, name = 'Back_to_HP')

###     3.8 Wärmestrom, der der HP vom Speicher zugeführt wird -> [W] = [kg/s] * [Ws/kgK] * [K]
    def Q_to_HP(m, t):
        if value(m.HP_off[t]) != 0:
            return(m.Q_HP_In[t] == m_flow_HP * c_w_water * value(m.T_HP_RL[t]))
        else:
            return(m.Q_HP_In[t] == 0)
    model.Q_to_HP = Constraint(time, rule = Q_to_HP, name = 'Q_to_HP')

###     3.9 Wärmestrom, der von der HP an den Speicher abgegeben wird -> [W] = [kg/s] * [Ws/kgK] * [K]
    def Q_from_HP(m, t):
        if value(m.HP_off[t]) != 0:
            return(m.Q_HP_Out[t] == m_flow_HP * c_w_water * value(m.T_HP_VL[t]))
        else:
            return(m.Q_HP_Out[t] == 0)
    model.Q_from_HP = Constraint(time, rule = Q_from_HP, name = 'Q_from_HP')

###     3.10 Wärmestrombilanz HP -> [W]
    def Q_HP_sum(m, t):
        return(m.Q_HP[t] >= value(m.Q_HP_Out[t]) - value(m.Q_HP_In[t]))
    model.Q_HP_sum  = Constraint(time, rule = Q_HP_sum, name = 'Q_HP_sum')

######################################################################################################
#######################---4. Equations to describe the Consumer-System (Hou)---#######################

###     4.1 Return temperature of Heating Fluid -> [K] = [K] - ([W] / [kg/s] * [Ws/kgK])
    def heat_use_House(m, t):
        return (m.T_Hou_VL[t] - (m.Q_Hou[t] / (m_flow_Hou * c_w_water)) >= m.T_Hou_RL[t])
#        return((m.T_Hou_VL[t] - m.T_Hou_RL[t]) == m.Q_Hou[t] /  (m.x_m_flow_Hou[t] * m_flow_Hou * c_w_water))
    model.heat_use_House = Constraint(time, rule = heat_use_House, name ='heat_use_House')

###     4.2 Heat flow from Storage to House -> [W] = [kg/s] * [Ws/kgK] * [K]
    def total_Heat_to_House(m, t):
        return(m.Q_Hou_In[t] == m_flow_Hou * c_w_water * m.T_Hou_VL[t])
    model.Total_Heat_to_House = Constraint(time, rule = total_Heat_to_House, name = 'Total_Heat_to_House')

###     4.3 Heat flow back from House to Storage -> [W] = [kg/s] * [Ws/kgK] * [K]
    def total_Heat_from_House(m, t):
        return(m.Q_Hou_Out[t] <= m_flow_Hou * c_w_water * m.T_Hou_RL[t])
    model.Total_Heat_from_House = Constraint(time, rule = total_Heat_from_House, name = 'Total_Heat_from_House')

###     4.4 Decharging Power from House -> [W]
    def Q_Hou_sum(m, t):
        return (m.Q_Hou[t] >= m.Q_Hou_In[t] - m.Q_Hou_Out[t])
    model.Q_Hou_sum = Constraint(time, rule=Q_Hou_sum, name='Q_Hou_sum')


###     4.5 Modell temperature from Storage to House -> [K]
    def Temperature_to_House(m, t):
        return(m.T_Hou_VL[t] == m.T_Sto[t] + 2)
    model.Temperature_to_House = Constraint(time, rule= Temperature_to_House, name = 'Temperature_to_House')



#######################---5. Power balance---#######################

###     5.1 Power Balance - PV-Power Production vs. Power Demand -> [W]
    def power_balance(m, t):
        return(m.P_EL[t] >= m.P_EL_Dem[t] + m.P_EL_HP[t] - m.P_PV[t])
    model.power_balance = Constraint(time, rule = power_balance, name = 'Power_balance')

###     5.2 Ermitteln, ob Strom ins Netz eingespeist oder bezogen [-]
    def Power_Demand(m, t):
        if value(m.P_EL[t]) > 0:
            return (m.Feed_In[t] == False)
        else:
            return(m.Feed_In[t] == True)
    model.Power_Demand = Constraint(time, rule=Power_Demand, name = 'Power_Demand')

#######################---6. Costs---#######################

###     6.1 Ermitteln der Kosten für Strom und für Einnahmen mit eingespeistem Strom pro Zeitschritt -> [€]
    def Cost_for_Power(m, t):
        if value(m.Feed_In[t]):
            return(m.c_cost[t] == 0.0)
        else:
            if options['Tariff']['Variable']:
                m.c_cost[t] == m.P_EL[t] * c_grid[t]
                return(m.c_cost[t] == value(m.P_EL[t]) * c_grid[t])
            else:
                return (m.c_cost[t] == value(m.P_EL[t]) * c_grid)
    model.Cost_for_Power = Constraint(time, rule= Cost_for_Power, name= 'Cost_for_Power')

###     6.2 Return money in case of Feed-In -> [€]
    def Return_for_Power(m, t):
        if value(m.Feed_In):
            return(m.c_earning[t] == value(m.P_EL[t]) * c_payment)
        else:
            return(m.c_earning[t] == 0.0)
        model.Return_for_Power = Constraint(time, rule=Return_for_Power, name= 'Return_for_Power')

###     6.2 Ermitteln der Gesamtausgaben für Strom abzüglich Einnahmen -> [€]
    def Cost_sum(m, t):
        return (m.costs_total == sum(m.c_cost[t] + m.c_earning[t] for t in time))
    model.Cost_sum = Constraint(time, rule= Cost_sum, name = 'Cost_sum')

#######################---Objective Function---#######################
## Idee: P_EL erstmal minimieren:
#    def Sum_PEL(m, t):
#        return (m.PEL == sum(m.P_EL_Dem[t]) for t in time)
#    model.Sum_PEL = Constraint(rule= Sum_PEL, name= 'Sum_PEL')

    def objective_rule(m):
        return (m.costs_total)
    model.total_costs = Objective(rule = objective_rule, sense = minimize, name = 'Minimize total costs')


#################################(ABFALL)#####################################
## 19. Heat flow from/ to Storage
 #   def Storage_Power_Change(m, t):
 #       if t > 0:
 #           return(m.Q_Sto[t] == (m_Sto_water * c_w_water * (m.T_Sto[t] - m.T_Sto[t-1])) / delta_t)
 #       else:
 #           return(m.Q_Sto[t] == m_Sto_water * c_w_water * m.T_Sto[t])
 #   model.Storage_Power_Change = Constraint(time, rule=Storage_Power_Change, name ='Storage_Power_Change')


            # 22. Get T_Hou_RL for an easy ideal consumer model
 #   def T_House_to_Storage(m, t):
 #       return(m.T_Hou_RL[t] == m.T_Hou_VL[t] - (((m.Q_Hou_Out[t] - m.Q_Hou_In[t] ) / ( m_flow_Hou * c_w_water ) * dt ) ))
 #   model.T_House_to_Storage = Constraint(time, rule = T_House_to_Storage, name = 'T_House_to_Storage')

            # 18. Temperature of easy Storage model
##    def easy_storage(m, t):
##        if t == 0:
##            return(m.T_Sto[t] == 20)
##        else:
##            return(m.T_Sto[t] - (m.Q_HP[t] + m.Q_Hou[t] + U_Sto * (T_Sto_Env - m.T_Sto[t] )  / (m_Sto_water * c_w_water) )== m.T_Sto[t-1])
##    model.easy_storage = Constraint(time, rule = easy_storage, name = 'easy_storage')

#    def HP_Q_mode(m, t):
#        return (m.Q_HP[t] == m.Q_mode1[t] * m.HP_mode1[t] + m.Q_mode2[t] * m.HP_mode2[t] + 0.0 * m.HP_off[t])
#    model.Heat_Q_mode = Constraint(time, rule=HP_Q_mode, name='HP_Q_mode')

# 23. Define which Temperatures are equal; conservative interpretation
# Annahme für schönere Rechnungen: Wenn die Temperatur im Speicher größer, als die
# zurückgeführte Temperatur aus dem Haus ist wird der Mittelwert aus beiden gebildet
# Ist die zurückgeführte Temperatur größer, wird die Speichertemperatur als HP-Rücklauftemperatur genommen


#######################---Solve Model---#######################

    solver = SolverFactory('gurobi')
    solver.options['Presolve'] = 1
    solver.options['mipgap'] = options['Solve']['MIP_gap']
    solver.options['TimeLimit'] = options['Solve']['TimeLimit']
    solver.options['DualReductions'] = 0

    try:
        opti_start_time = read_time.time()
        results = solver.solve(model, report_timing=True, tee=True, logfile='log_file_upper.log')
        log_infeasible_constraints(model)
        print('TerminationCondition', results.solver.termination_condition)
        # Get solving time
        opti_end_time = read_time.time() - opti_start_time
        print("Optimization done1. (%f seconds.)" % (opti_end_time))
        print(log_infeasible_constraints(model)) #->  None???

    except:
        print('Error:', sys.exc_info())
        try:
        # Try to get a solution within a longer solving time
            opti_start_time = read_time.time()
            solver.options['TimeLimit'] = options['Solve']['TimeLimit'] * 2
            results = solver.solve(model, report_timing=True, tee=True, logfile='log_file_upper.log')
            print('TerminationCondition', results.solver.termination_condition)
            opti_end_time = read_time.time() - opti_start_time
            print("Optimization done2. (%f seconds.)" % (opti_end_time))
        except:
            # Try to get a solution within max defined solving time
            print('Error:', sys.exc_info())
            opti_start_time = read_time.time()
            solver.options['TimeLimit'] = options['Solve']['TimeLimitMax']
            results = solver.solve(model, report_timing=True, tee=True, logfile='log_file_upper.log')
            print('TerminationCondition', results.solver.termination_condition)
            opti_end_time = read_time.time() - opti_start_time
            print("Optimization done3. (%f seconds.)" % (opti_end_time))

    status = 'feasible'

    if results.solver.termination_condition == TerminationCondition.infeasibleOrUnbounded or \
         results.solver.termination_condition == TerminationCondition.infeasible:

        solver_parameters = "ResultFile=model.ilp"  # write an ILP file to print the IIS
        results = solver.solve(model, tee=True, logfile='log_file_lower.log', options_string=solver_parameters)
        print('model infeasible, solver status', results.solver.termination_condition)
#        status = 'infeasible'



    res_control_horizon = {
        'solving_time'      : [],
        'Mode 0'            : [],
        'Mode 1'            : [],
        'Mode 2'            : [],
        'Q_Sto'             : [],
        'Q_HP'              : [],
        'Q_Hou_Dem'         : [],
        'Q_Hou'             : [],
        'Q_Sto_Loss'        : [],
        'P_EL'              : [],
        'P_EL_HP'           : [],
        'P_EL_Dem'          : [],
        'P_PV_Grid'         : [],
        'P_PV_Use'          : [],
        'P_PV'              : [],
        'COP_Carnot'        : [],
        'COP_HP'            : [],
        'T_Air_Input'       : [],
        'T_Air'             : [],
        'T_Sto'             : [],
        'T_HP_VL'           : [],
        'T_HP_RL'           : [],
        'T_Hou_VL'          : [],
        'T_Hou_RL'          : [],
        'c_total'           : [],
#        'c_revenue'         : [],
        'total_costs'       : [],
        'PEL'               : [],
        #'m_Sto_water'             : [],

    }
    results_horizon = int((params['control_horizon'] / params['time_step']))
    print('Results_Horizont ist:',  results_horizon)
    for t in range(results_horizon):
        if status == 'infeasible':
            for res in res_control_horizon:
                res_control_horizon[res].append(0)


        res_control_horizon['solving_time'].append(opti_end_time)
        res_control_horizon['Mode 0'].append(value(model.HP_off[t]))
        res_control_horizon['Mode 1'].append(value(model.HP_mode1[t]))
        res_control_horizon['Mode 2'].append(model.HP_mode2[t])
        res_control_horizon['Q_Sto'].append(value(model.Q_Sto[t]))
        res_control_horizon['Q_HP'].append(value(model.Q_HP[t]))
        res_control_horizon['Q_Hou_Dem'].append(Q_Hou_Dem[t])
        res_control_horizon['Q_Hou'].append(value(model.Q_Hou[t]))
        res_control_horizon['Q_Sto_Loss'].append(value(model.Q_Sto_Loss[t]))
        res_control_horizon['P_EL'].append(value(model.P_EL[t]))
        res_control_horizon['P_EL_HP'].append(value(model.P_EL_HP[t]))
        res_control_horizon['P_EL_Dem'].append(value(model.P_EL_Dem[t]))
        res_control_horizon['P_PV'].append(value(model.P_PV[t]))
        res_control_horizon['COP_Carnot'].append(value(model.COP_Carnot[t]))
        res_control_horizon['COP_HP'].append(value(model.COP_HP[t]))
        res_control_horizon['T_Air_Input'].append(T_Input[t])
        res_control_horizon['T_Air'].append(value(model.T_Air[t]))
        res_control_horizon['T_Sto'].append(value(model.T_Sto[t]))
        res_control_horizon['T_HP_VL'].append(value(model.T_HP_VL[t]))
        res_control_horizon['T_HP_RL'].append(value(model.T_HP_RL[t]))
        res_control_horizon['T_Hou_VL'].append(value(model.T_Hou_VL[t]))
        res_control_horizon['T_Hou_RL'].append(value(model.T_Hou_RL[t]))
        res_control_horizon['c_total'].append(value(model.costs_total))
#        res_control_horizon['c_revenue'].append(model.c_revenue)
        res_control_horizon['total_costs'].append(model.total_costs)
#        res_control_horizon['PEL'].append(model.PEL)

    model.pprint()
#    print(res_control_horizon['P_EL'])
    return res_control_horizon



