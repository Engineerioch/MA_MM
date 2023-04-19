#
#
#
#
###############Parkplatz für evtl mal benötigten Code###########################
## Origin: Optimiziation
#######################################Storage System in a System with 4 Layers##################################
#
#    def Storage_Temperature(m, t, l):
#        if m.Q_HP[t]      > 0 :
#            if m.Q_Hou[t] > 0 :
#                # l=1 und l=2 mittlere Schichten
#                for l in range [1,2]:
#                    m.Q_Conv[t, l] = m.m_flow_Hou[t] * m.c_w_water * (m.T_Sto[t, l+1 ] - m.T_Sto[t, l] ) -              \
#                                     m.m_flow_Hou[t] * m.c_w_water * (m.T_Sto[t, l+1] - m.T_Sto[t. l]) +                     \
#                                     (m.m_flow_HP[t] - m.m_flow_Hou[t] ) * m.c_w_water * (m.T_Sto[t, l-1] - m.T_Sto[t, l])
#                    m.Q_Conn[t, l] = 0
#
#                # l= 0 Oberste Schicht
#                for l = 0:
#                    m.Q_Conv[t, l] = m.m_flow_Hou[t] * m.c_w_water * m.T_Sto[t, l+1] -                                  \
#                                     m.m_flow_Hou[t] * m.c_w_water * m.T_Sto[t, l+1] -                                  \
#                                     (m.m_flow_HP[t]  - m.m_flow_Hou[t] ) * m.c_w_water * m.T_Sto[t, l]
#                    m.Q_Conn[t, l] = - m.m_flow_Hou[t] * m.c_w_water * m.T_Sto[t,l] +                                   \
#                                     m.m_flow_HP[t] * m.c_w_water * m.T_HP_VL[t]
#                # L =3 unterste Schicht
#                for l = 3:
#                    m.Q_Conv[t, l] = - m.m_flow_Hou[t] * m.c_w_water * m.T_Sto[t, l] +                                  \
#                                     m.m_flow_Hou[t] * m.c_w_water * m.T_Sto[t, l] +                                    \
#                                     (m.m_flow_HP[t] - m.m_flow_Hou[t]) * m.c_w_water * m.T_Sto[t, l-1]
#                    m.Q_Conn[t, l] = m.m_flow_Hou[t] * m.c_w_water * m.T_Hou_RL[t] -                                    \
#                                     m.m_flow_HP[t] * m.c_w_water * m.T_Sto[t, l]
#            else:
#                for l in range [1,2]:
#                    m.Q_Conv[t, l] = m.m_flow_HP[t] * m.c_w_water * (m.T_Sto[t, l-1] - m.T_Sto[t, l])
#                    m.Q_Conn[t, l] = 0
#                    # l= 0 Oberste Schicht
#                for l = 0:
#                    m.Q_Conv[t, l] =  - m.m_flow_HP[t] * m.c_w_water * m.T_Sto[t, l]
#                    m.Q_Conn[t, l] = m.m_flow_HP[t] * m.c_w_water * m.T_HP_VL[t]
#                    # L =3 unterste Schicht
#                for l = 3:
#                    m.Q_Conv[t, l] = m.m_flow_HP[t] * m.c_w_water * m.T_Sto[t, l-1]
#                    m.Q_Conn[t, l] = - m.m_flow_HP[t] * m.c_w_water * m.T_Sto[t, l]
#        else:
#            if m.Q_Hou[t] > 0:
#                for l in range [1,2]:
#                    m.Q_Conv[t ,l] = m.m_flow_Hou[t] * m.c_w_water * (m.T_Sto[t, l+1] - m.T_Sto[t, l])
#                    m.Q_Conn[t, l] = 0
#                for l = 0:
#                    m.Q_Conv[t, l] =  m.m_flow_Hou[t] * m.c_w_water * m.T_Sto[t, l+1]
#                    m.Q_Conn[t, l] = - m.m_flow_Hou[t] * m.c_w_water * m.T_Sto[t, l]
#                for l = 3:
#                    m.Q_Conv[t, l] = - m.m_flow_Hou[t] * m.c_w_water * m.T_Sto[t, l]
#                    m.Q_Conn[t,l] = m.m_flow_Hou[t] * m.c_w_water * m.T_Hou_RL[t]
#            else:
#                for l in range [1,2]:
#                    m.Q_Conv[t, l] = 0
#                    m.Q_Conn[t, l] = 0
#                for l = 0:
#                    m.Q_Conv[t, l] = 0
#                    m.Q_Conn[t, l] = 0
#                for l = 3:
#                    m.Q_Conv[t, l] = 0
#                    m.Q_Conn[t, l] = 0
#
#        if l in range [1,2]:
#            m.Q_Lam[t, l] = m.lambda_Sto * m.A_CS[t] * (m.T_Sto[t, l+1] - 2 * m.T_Sto[t, l] + m.T_Sto[t, l-1] / m.delta_z)
#        elif l = 0:
#            m.Q_Lam[t, l] = m.lambda_Sto * m.A_CS[t] * (m.T_Sto[t, l+1] - m.T_Sto[t, l] / m.delta_z)
#        elif l = 3:
#            m.Q_Lam[t, l] = m.lambda_Sto * m.A_CS[t] * (m.T_Sto[t, l-1] - m.T_Sto[t, l] / m.delta_z)
#        m.Q_Loss[t, l] = m.k_Sto * m.A_Sto[t, l] * (m.T_Sto[t, l] - m.T_Env)
#
#        m.Q_Sto_Loss[t] = m.Q_Conv[t, l] + m.Q_Conn[t, l] + m.Q_Lam[t, l] -
#        return(m.Q_Conv[t, l], m.Q_Conn[t, l], m.Q_Lam[t, l], m.Q_Loss[t, l])
#
#    def layer_storage_balance(m, t, l):
#        return(m.T_Sto[t, l] == (((m.Q_Conv[t, l] + m.Q_Conn[t, l] + m.Q_Lam[t, l] - m.Q_Loss[t, l])* m.dt ) /(m.m_Sto[t] * m.c_w_water)) + m.T_Sto[t-1, l] )
#    model.layer_storage_balance = Constraint(time, rule = layer_storage_balance, name= 'layer_storage_balance')
#
#    ##############################################
#
## 5. Temperature in Storage for an easy storage system with 1 layer and homogeneous Temperature
#def easy_storage_balance(m, t):
#    return (m.T_Sto[t] - m.T_Sto[t - 1] == (
#                m.Q_HP[t] - m.Q_Hou[t] - (m.k_Sto * m.A_Sto * (T_Sto[t] - T_Sto_Env))) * m.dt / (
#                        m.m_Sto[t] * m.c_w_water))
#
#
#model.easy_storage_balance = Constraint(time, rule=easy_storage_balance, name='easy_storage_balance')
#
#
#
########################---Formeln aus Opti, die nicht verwendet wurden---###############################
#
#            # 14. Maximum Power generated by the PV_System
#    def Maximum_PV_Power_rule(m, t):
#        return(P_PV[t][0] <= P_PV_Max)
#    model.Maximum_PV_Power = Constraint(time, rule = Maximum_PV_Power_rule, name = 'Maximum_PV_Power')
#
#            # 15. Minimum Power generated by the PV-System
#    def Minimum_PV_Power_rule(m, t):
#        return(m.P_PV[t][0] >= P_PV_Min)
#    model.Minimum_PV_Power = Constraint(time, rule = Minimum_PV_Power_rule, name = 'Minimum_PV_Power')
#
#
## 23. Define which Temperatures are equal; conservative interpretation
## Annahme für schönere Rechnungen: Wenn die Temperatur im Speicher größer, als die
## zurückgeführte Temperatur aus dem Haus ist wird der Mittelwert aus beiden gebildet
## Ist die zurückgeführte Temperatur größer, wird die Speichertemperatur als HP-Rücklauftemperatur genommen
#    def Equal_Temperatures(m, t):
#        if value(m.T_Sto[t]) >= value(m.T_Hou_RL[t]):
#            return(m.T_HP_RL[t] == (m.T_Sto[t] + m.T_Hou_RL[t]) / 2 )
#        else:                                                   #if value(m.T_Sto[t] < value(m.T_Hou_RL[t]))
#            return(m.T_HP_RL[t] == value(m.T_Sto[t]))
#    model.Equal_Temperature = Constraint(time, rule = Equal_Temperatures, name = 'Equal_Temperatures')
#
#
#       # 27. Total Costs for Power and Revenue for Feed in (Sum)
#    def total_power_cost(m, t):
#        return(m.c_cost_sum == (sum(m.c_cost[t])) for t in time_range)                                          # [€]   If Value is positive, costs are positive, if value is negative, the system will return money
#    model.total_power_cost = Constraint(rule=total_power_cost, name = 'totaL_power_cost')
#
#        # 28. Total Revenue for PV-Production Feed in (Sum)
#    def total_power_revenue(m, t):
#        return(m.c_revenue == (sum(m.c_earning[t]) for t in time))
#    model.total_power_revenue = Constraint(time, rule = total_power_revenue, name = 'total_power_revenue')
#
#
#
#    #######################OPtimization before Test#########################
#
#
#
#from typing import Union, Any
#
## Optimization of ExtractingRuleStudy
#from pyomo.environ import *
#from pyomo.util.infeasible import log_infeasible_constraints
#from pyomo.opt import UnknownSolver
#from pyomo.opt.base.solvers import SolverFactoryClass
#import time as read_time
#import sys
#import copy
#import time as read_time
#
#
#def run_MPC(params, options, eco, time_series, devs):
#    # Set parameter
#    dt = params['time_step']
#    start_time = params['start_time']
#    prediction_horizon = params['prediction_horizon']
#    time_range = range(int(params['prediction_horizon'] * (1 / params['time_step'])) + 1)
#    time = range(int(params['prediction_horizon'] * 1 / params['time_step']))
#    delta_t = params['time_step'] * 3600  # time Step in seconds
#
#    # Set economic parameter - set in parameter.py -> eco
#    #    c_grid_var          =   time_series['c_grid_var']                # [Euro/kWh]   Variable grid charges Stromnetze Berlin
#    #    c_grid              =   eco['costs']['c_grid_dem']                  # [Euro/kWh]   Grid charges with fix Price Berlin
#    c_payment = eco['costs']['c_payment']  # [Euro/kWh]    Feed in tariff
#
#    if options['Tariff']['Variable']:
#        c_grid = time_series['c_grid_var']
#    else:
#        c_grid = eco['costs']['c_grid_dem']
#
#    # Set PV profile
#    P_PV = time_series['P_PV']
#    P_PV_Max = devs['PV']['n_mod'] * devs['PV']['P_PV_Module']  # [kW] maximum Sum Power of all PV-Modules
#    P_PV_Min = devs['PV']['P_PV_Min']
#
#    # Set Heat storage parameters
#    T_Sto_max = devs['Sto']['T_Sto_max']
#    T_Sto_min = devs['Sto']['T_Sto_min']
#    m_Sto_water = devs['Sto']['Volume'] * devs['Nature']['Roh_water']
#    T_Sto_Env = devs['Sto']['T_Sto_Env']
#    U_Sto = devs['Sto']['U_Sto']
#    Cap_Sto = devs['Sto']['Volume'] * devs['Nature']['c_w_water']
#    T_Kalt = devs['Sto']['T_Kalt']
#    A_Sto = devs['Sto']['A_Sto']
#
#    # Set Consumer parameter
#    T_Hou_delta_max = devs['Hou']['T_Hou_delta_max']
#    P_EL_Dem = time_series['P_EL_Dem']
#    m_flow_Hou = devs['Hou']['m_flow_Hou']
#    Q_Hou_Dem = time_series['Q_Hou_Dem']  # [W] Heat Demand of House
#
#    # Set Heat Pump parameters
#    m_flow_HP = devs['HP']['m_flow_HP']
#    eta_HP = devs['HP']['eta_HP']  # [-] Gütegrad HP
#    Q_HP_Max = devs['HP']['Q_HP_Max']  # [kW] Maximum Power of Heat Pump
#    Q_HP_Min = devs['HP']['Q_HP_Min']  # [kW] Minimum Power of Heat Pump
#    T_HP_VL_1 = devs['HP']['T_HP_VL_1']
#    T_HP_VL_2 = devs['HP']['T_HP_VL_2']
#
#    # Set Natural Parameters
#    c_w_water = devs['Nature']['c_w_water']
#    T_Air = time_series['T_Air'] + 273.15  # [K]  Außentemperatur
#
#    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#    # Übergeben der Variablen an das Model
#    # Initialize model
#    model = ConcreteModel()
#
#    # Grid Interaction
#    model.P_EL = Var(time, within=Reals, name='P_EL', initialize=P_EL_Dem[0])
#    model.P_EL_HP = Var(time, within=NonNegativeReals, name='P_EL_HP', initialize=0)
#    model.P_PV = Var(time, within=NonNegativeReals, name='P_PV', initialize=P_PV[0])
#    model.P_EL_Dem = Var(time, within=Reals, name='P_EL_Dem', initialize=P_EL_Dem[0])
#    model.P_EL_Grid = Var(time, within=Reals, name='P_EL_Grid')  # initialize=)
#    model.P_PV_Grid = Var(time, within=NonNegativeReals, name='P_PV_Grid')  # , initialize=0)
#    #    model.Q_Hou_Dem     = Param(time, within = Reals, name = 'Q_Hou_Dem'),
#    model.Q_Sto = Var(time, within=Reals, name='Q_Sto', initialize=0)
#    model.Q_HP_Out = Var(time, within=NonNegativeReals, name='Q_HP_Out', initialize=0)
#    model.Q_HP_In = Var(time, within=NonNegativeReals, name='Q_HP_In', initialize=0)
#    model.Q_Hou_In = Var(time, within=NonNegativeReals, name='Q_Hou_In', initialize=0)
#    model.Q_Hou_Out = Var(time, within=NonNegativeReals, name='Q_Hou_Out', initialize=0)
#    model.Q_Sto_Loss = Var(time, within=Reals, name='Q_Sto_Loss', initialize=0)
#    model.Q_Hou = Var(time, within=Reals, name='Q_Hou', initialize=Q_Hou_Dem[0])
#    model.Q_HP = Var(time, within=NonNegativeReals, name='Q_HP', initialize=0)
#    model.T_HP_VL = Var(time, within=NonNegativeReals, name='T_HP_VL', initialize=0)
#    model.T_HP_RL = Var(time, within=NonNegativeReals, name='T_HP_RL', initialize=0)
#    model.T_Hou_delta = Var(time, within=Reals, name='T_Hou_delta', initialize=0)
#    model.T_Hou_VL = Var(time, within=NonNegativeReals, name='T_Hou_VL', initialize=0)
#    model.T_Hou_RL = Var(time, within=NonNegativeReals, name='T_Hou_RL', initialize=0)
#    model.COP_HP = Var(time, within=NonNegativeReals, name='COP_HP', initialize=1)
#    model.COP_Carnot = Var(time, within=NonNegativeReals, name='COP_Carnot', initialize=0)
#    model.T_Sto = Var(time, within=NonNegativeReals, name='T_Sto', initialize=35 + 273.15)
#    model.Cap_Sto = Var(time, within=NonNegativeReals, name='Cap_Sto', initialize=0)
#    model.c_earning = Var(time, within=Reals, name='c_earning', initialize=0)  # Einspeisevergütung pro Zeitschritt
#    model.c_cost = Var(time, within=Reals, name='c_cost')  # Stromkosten pro Zeitschritt
#    #    model.c_grid        = Var(time, within = Reals,             name = 'c_grid', initialize = )
#    #    model.c_total       = Var(time, within = Reals,             name = 'c_total', initialize =)
#    model.c_revenue = Var(time, within=Reals, name='c_revenue')  # Stromvergütung gesamt (reine Vergütung)
#    model.c_cost_sum = Var(time, within=NonNegativeReals, name='c_cost_sum',
#                           initialize=0)  # Stromkosten gesamt (reine Kosten)
#    model.costs_total = Var(within=Reals, name='costs_total')
#    model.Feed_In = Var(time, within=Boolean, name='Feed_In', initialize=False)
#
#    ##### Entscheidungsvariablen: Auswahl des Modus
#    model.HP_off = Var(time, within=Binary, name='HP_off', initialize=1)  # HP an oder aus; HP_off = 1 -> HP ist aus
#    model.HP_hot = Var(time, within=Binary, name='HP_hot', initialize=0)  # HP on, T_VL = 70 °C
#    model.HP_cold = Var(time, within=Binary, name='HP_cold', initialize=0)  # HP on, T_VL = 35°C
#    model.x_m_flow_HP = Var(time, within=Binary, name='x-m_flow_HP',
#                            initialize=0)  # Wenn HP an -> Massenstrom HP ungleich 0
#    model.x_m_flow_Hou = Var(time, within=Binary, name='x_m_flow_Hou',
#                             initialize=1)  # Wenn 'Heizung' an -> Massenstrom Hou ungleich 0
#
#    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#    # Einführen der Nebenbedingungen
#    # Add Constraints to model
#    #######################---Balances of Power and Heat---#######################
#    # todo Einheiten überprüfen
#
#    #######################---Import of PV- and Q_Hou_Dem Data and write that Data in Model Variables---#######################
#
#    def P_PV_Model(m, t):
#        return (m.P_PV[t] == P_PV[t])
#
#    model.P_PV_Model = Constraint(time, rule=P_PV_Model, name='P_PV_Model')
#
#    # Constraint that Heat to House is always equal to the Heat demand
#    def Heat_to_House_equals_Demand(m, t):
#        return (m.Q_Hou[t] == Q_Hou_Dem[t])
#
#    model.Heat_to_House_equals_Demand = Constraint(time, rule=Heat_to_House_equals_Demand,
#                                                   name=Heat_to_House_equals_Demand)
#
#    def Power_Demand_In_House(m, t):
#        return (m.P_EL_Dem[t] == P_EL_Dem[t])
#
#    model.Power_Demand_In_House = Constraint(time, rule=Power_Demand_In_House, name='Power_Demand_In_House')
#
#    def Q_Content_Sto(m, t):
#        return (m.Q_Sto[t] == m_Sto_water * c_w_water * (m.T_Sto[t] - T_Kalt))
#
#    model.Q_Content_Sto = Constraint(time, rule=Q_Content_Sto, name='Q_Content_Sto')
#
#    #   def Temp_Outside(m, t)
#    #      return(m.T_Air == T_Air[t][0])
#
#    # 1. Power Balance total
#    # PV-Power Production vs. Power Demand
#    def power_balance(m, t):
#        return (m.P_EL[t] == m.P_EL_Dem[t] + m.P_EL_HP[t] - m.P_PV[t])
#
#    model.power_balance = Constraint(time, rule=power_balance, name='Power_balance')
#
#    # 2. Storage Heat Balance
#    # Wärme die vom Speicher an die Wärmepumpe (RL) zurückfließt und an das Haus abgegeben wird als Minus, Wärme die von der Wärmepumpe und aus dem Haus an den Speicher fließt als plus
#    def storage_balance(m, t):
#        return (m.Q_Sto[t] == m.Q_HP_Out[t] - m.Q_HP_In[t] - m.Q_Hou_In[t] + m.Q_Hou_Out[t] - m.Q_Sto_Loss[t])
#
#    model.storage_balance = Constraint(time, rule=storage_balance, name='storage_balance')
#
#    #######################---Equations to describe the combined System---#######################
#
#    # 3. Constraints for Binary Variables to descide if T_HP_VL = 35°C or 70°C -> during HP_on
#    def HP_Mode_rule(m, t):
#        return (m.HP_off[t] + m.HP_hot[t] + m.HP_cold[t] == 1.0)
#
#    model.HP_Mode_rule = Constraint(time, rule=HP_Mode_rule, name='HP_Mode_rule')
#
#    # 4. Set T_HP_VL for the two different "on" Modes
#    def HP_Operation_rule(m, t):
#        if value(m.HP_off[t]) > value(m.HP_hot[t]) and value(m.HP_off[t]) < value(m.HP_cold[t]):
#            return (m.x_m_flow_HP[t] == 0.0, m.T_HP_VL[t] == 0.0)
#        else:
#            if value(m.HP_hot[t]) > value(m.HP_cold[t]):
#                return (m.T_HP_VL[
#                            t] == T_HP_VL_2)  # Wenn der Modus HP_hot ausgewählt wird, wird die Vorlauftemperatur auf 70 °C gesetzt
#            elif value(m.HP_cold[t]) < value(m.HP_cold[t]):
#                return (m.T_HP_VL[t] == T_HP_VL_1)
#            else:
#                return (m.T_HP_VL[t] == 0.0)
#
#    model.HP_Operation_rule = Constraint(time, rule=HP_Operation_rule, name='HP_Operation_rule')
#
#    def Bin_m_flow_House(m, t):
#        if value(m.Q_Hou[t]) == 0.0:
#            return (m.x_m_flow_Hou[t] == 0.0)
#        else:
#            return (m.x_m_flow_Hou[t] == 1.0)
#
#    model.Bin_m_flow_House = Constraint(time, rule=Bin_m_flow_House, name='Bin_m_flow_House')
#
#    # 5. Heat used by the House
#    # Balance of heat which flows from Storage to House and back to the Storage -> Equals Heat flow from storage to house
#    def heat_use_House(m, t):
#        return (m.T_Hou_VL[t] - (m.Q_Hou[t] / (m_flow_Hou * c_w_water)) == m.T_Hou_RL[t])
#
#    #        return((m.T_Hou_VL[t] - m.T_Hou_RL[t]) == m.Q_Hou[t] /  (m.x_m_flow_Hou[t] * m_flow_Hou * c_w_water))
#    model.heat_use_House = Constraint(time, rule=heat_use_House, name='heat_use_House')
#
#    # 6. Heat balance of Heat Pump
#    # Equation for Heat flow from Storage to HP and from HP to Storage for two different modes
#    # Modes are taking into account by x_m_flow_HP and T_HP_VL
#    def heat_from_HP(m, t):
#        return (m.Q_HP[t] == m.x_m_flow_HP[t] * m_flow_HP * c_w_water * (m.T_HP_VL[t] - m.T_HP_RL[t]))
#
#    model.heat_from_HP = Constraint(time, rule=heat_from_HP, name='heat_from_HP')
#
#    # 7. Temperature change of Heater Fluid during heating of the House
#    ##    def Temperature_Change_Hou(m, t):
#    ##       return(m.T_Hou_delta[t] == m.T_Hou_VL[t] - m.T_Hou_RL[t])
#    ##   model.Temperature_Change_House = Constraint(time, rule = Temperature_Change_Hou, name = 'Temperature_Change_Hou')
#
#    # 8. Heat flow from Storage to House
#    def total_Heat_to_House(m, t):
#        return (m.Q_Hou_In[t] == m.x_m_flow_Hou[t] * m_flow_Hou * c_w_water * m.T_Hou_VL[t])
#
#    model.Total_Heat_to_House = Constraint(time, rule=total_Heat_to_House, name='Total_Heat_to_House')
#
#    # 9. Heat flow back from House to Storage
#    def total_Heat_from_House(m, t):
#        return (m.Q_Hou_Out[t] == m.x_m_flow_Hou[t] * m_flow_Hou * c_w_water * m.T_Hou_RL[t])
#
#    model.Total_Heat_from_House = Constraint(time, rule=total_Heat_from_House, name='Total_Heat_from_House')
#
#    # Todo
#
#
#
#    #######################---Maximum and Minimum Power by PV- or HP System---#######################
#
#    # 16. Maximum Power of Heat Pump
#    def Maximum_HP_Power_rule(m, t):
#        return (m.Q_HP[t] <= Q_HP_Max)
#
#    model.Maximum_HP_Power = Constraint(time, rule=Maximum_HP_Power_rule, name='Maximum_HP_Power')
#
#    #######################---Easy Storage---#######################
#
#    # 18. Temperature of easy Storage model
#    ##    def easy_storage(m, t):
#    ##        if t == 0:
#    ##            return(m.T_Sto[t] == 20)
#    ##        else:
#    ##            return(m.T_Sto[t] - (m.Q_HP[t] + m.Q_Hou[t] + U_Sto * (T_Sto_Env - m.T_Sto[t] )  / (m_Sto_water * c_w_water) )== m.T_Sto[t-1])
#    ##    model.easy_storage = Constraint(time, rule = easy_storage, name = 'easy_storage')
#
#    def easy_storage_test(m, t):
#        if t == 0:
#            return (m.T_Sto[t] == 35 + 273.15)
#        else:
#            return (m.T_Sto[t] == ((m.Q_HP[t] - m.Q_Hou[t]) * delta_t + m_Sto_water * c_w_water * m.T_Sto[
#                t - 1] + U_Sto * T_Sto_Env * delta_t) / (m_Sto_water * c_w_water + U_Sto * delta_t))
#
#    model.easy_storage_test = Constraint(time, rule=easy_storage_test, name='easy_storage_test')
#
#    # 19. Heat flow from/ to Storage
#    def Storage_Power_Change(m, t):
#        if t > 0:
#            return (m.Q_Sto[t] == (m_Sto_water * c_w_water * (m.T_Sto[t] - m.T_Sto[t - 1])) / delta_t)
#        else:
#            return (m.Q_Sto[t] == m_Sto_water * c_w_water * m.T_Sto[t])
#
#    model.Storage_Power_Change = Constraint(time, rule=Storage_Power_Change, name='Storage_Power_Change')
#
#    #    def Q_Sto_Temp (m, t):
#    #        if t >= 1:
#    #            return(m.Q_Sto[t] == m_Sto_water * c_w_water * (m.T_Sto[t] - m.T_Sto[t-1]) * delta_t)
#    #        else:
#    #            return(m.Q_Sto[t] == 0)
#    #    model.Q_Sto_Temp = Constraint(time, rule = Q_Sto_Temp, name = 'Q_Sto_Temp')
#
#    # xx. Loss of Storage to Environment in House (No Heating Power resuls from this)
#    def Storage_Loss(m, t):
#        return (m.Q_Sto_Loss[t] == U_Sto * A_Sto * (m.T_Sto[t] - T_Sto_Env))
#
#    model.Storage_Loss = Constraint(time, rule=Storage_Loss, name='Storage_Loss')
#
#    # 20. Decharging Power from House
#    def Q_Hou_sum(m, t):
#        return (m.Q_Hou[t] == m.Q_Hou_In[t] - m.Q_Hou_Out[t])
#
#    model.Q_Hou_sum = Constraint(time, rule=Q_Hou_sum, name='Q_Hou_sum')
#
#    # 21. Fixed Temperature Difference between top of the Storage and Buttom
#    # vlt die Logarithmus Formel aus einer der vielen MAs?
#    # oder für den Anfang sagen dass die T_Hou_RL= T_HP_RL
#
#    # 22. Get T_Hou_RL for an easy ideal consumer model
#    #    def T_House_to_Storage(m, t):
#    #        return(m.T_Hou_RL[t] == m.T_Hou_VL[t] - (((m.Q_Hou_Out[t] - m.Q_Hou_In[t] ) / ( m_flow_Hou * c_w_water ) * dt ) ))
#    #    model.T_House_to_Storage = Constraint(time, rule = T_House_to_Storage, name = 'T_House_to_Storage')
#
#    # 23. Define which Temperatures are equal; conservative interpretation
#    # Annahme für schönere Rechnungen: Wenn die Temperatur im Speicher größer, als die
#    # zurückgeführte Temperatur aus dem Haus ist wird der Mittelwert aus beiden gebildet
#    # Ist die zurückgeführte Temperatur größer, wird die Speichertemperatur als HP-Rücklauftemperatur genommen
#
#    def Back_to_HP(m, t):
#        return (m.T_HP_RL[t] == m.T_Sto[t] - 2)
#
#    model.Back_to_HP = Constraint(time, rule=Back_to_HP, name='Back_to_HP')
#
#    def Temperature_to_House(m, t):
#        return (m.T_Hou_VL[t] == m.T_Sto[t] + 2)
#
#    model.Temperature_to_House = Constraint(time, rule=Temperature_to_House, name='Temperature_to_House')
#
#    # 24. Q_HP_In -> Wärmestrom, der der HP zugeführt wird
#    def Q_to_HP(m, t):
#        if value(m.HP_off[t]) != 0:
#            return (m.Q_HP_In[t] == m_flow_HP * c_w_water * m.T_HP_RL[t])
#        else:
#            return (m.Q_HP_In[t] == 0)
#
#    model.Q_to_HP = Constraint(time, rule=Q_to_HP, name='Q_to_HP')
#
#    # 25. Q_HP_Out -> Wärmestrom, der von der HP abgegeben wird
#    def Q_from_HP(m, t):
#        if value(m.HP_off[t]) != 0:
#            return (m.Q_HP_Out[t] == m_flow_HP * c_w_water * m.T_HP_VL[t])
#        else:
#            return (m.Q_HP_Out[t] == 0)
#    model.Q_from_HP = Constraint(time, rule=Q_from_HP, name='Q_from_HP')
#
#    def Q_HP_sum(m, t):
#        return (m.Q_HP[t] == m.Q_HP_Out[t] - m.Q_HP_In[t])
#    model.Q_HP_sum = Constraint(time, rule=Q_HP_sum, name='Q_HP_sum')
#
#    def Power_Demand(m, t):
#        if value(m.P_EL[t]) > 0:
#            return (m.Feed_In[t] == False)
#        else:
#            return (m.Feed_In[t] == True)
#    model.Power_Demand = Constraint(time, rule=Power_Demand, name='Power_Demand')
#
#    #######################---Costs---#######################
#
#    def Cost_for_Power(m, t):
#        if value(m.Feed_In[t]):
#            m.c_earning[t] == m.P_EL[t] * c_payment
#            m.c_cost[t] == 0
#            return (m.c_cost[t], m.c_earning[t])
#        else:
#            m.c_earning[t] == 0
#            if options['Tariff']['Variable']:
#                m.c_cost[t] == m.P_EL[t] * c_grid[t]
#                return (m.c_cost[t], m.c_earning[t])
#            else:
#                m.c_cost[t] == m.P_EL[t] * c_grid
#                return (m.c_cost[t], m.c_earning[t])
#    model.Cost_for_Power = Constraint(time, rule=Cost_for_Power, name='Cost_for_Power')
#
#    def Cost_sum(m, t):
#        return (m.costs_total == sum(m.c_cost[t] + m.c_earning[t] for t in time))
#    model.Cost_sum = Constraint(time, rule=Cost_sum, name='Cost_sum')
#
#
#    #######################---Objective Function---#######################
#
#    def objective_rule(m):
#        return (m.costs_total)
#    model.total_costs = Objective(rule=objective_rule, sense=minimize, name='Minimize total costs')
#
#    #######################---Objective Function---#######################
#
#    ############################ Gleichsetzen von Variablen, die mehrere Bezeichnungen haben, aber das Gleiche sind####################
#
#    #    T_Sto[t, l = 0] = T_Hou_VL[t]
#    #   T_Sto[t, l = 3] = T_HP_RL[t]
#
#    #######################---Solve Model---#######################
#
#    results = SolverFactory('gurobi').solve(model, tee=True, logfile='my_log_file.log')
#    if options['Solve']['type'] == 'gurobi':
#        solver = SolverFactory('gurobi')
#        solver.options['Presolve'] = 2
#        solver.options['mipgap'] = options['Solve']['MIP_gap']
#        solver.options['TimeLimit'] = options['Solve']['TimeLimit']
#        solver.options['DualReductions'] = 0
#
#    elif options['Solve']['type'] == 'glpk':
#        solver = SolverFactory('glpk')
#        #    solver.options['Presolve'] = 2
#        solver.options['mipgap'] = options['Solve']['MIP_gap']
#        solver.options['TimeLimit'] = options['Solve']['TimeLimit']
#
#    try:
#        opti_start_time = read_time.time()
#        results = solver.solve(model, report_timing=True, tee=True, logfile='log_file_upper.log')
#        log_infeasible_constraints(model)
#        print('TerminationCondition', results.solver.termination_condition)
#        # Get solving time
#        opti_end_time = read_time.time() - opti_start_time
#        print("Optimization done. (%f seconds.)" % (opti_end_time))
#
#    except:
#        print('Error:', sys.exc_info())
#        try:
#            # Try to get a solution within a longer solving time
#            opti_start_time = read_time.time()
#            solver.options['TimeLimit'] = options['Solve']['TimeLimit'] * 2
#            results = solver.solve(model, report_timing=True, tee=True, logfile='log_file_upper.log')
#            print('TerminationCondition', results.solver.termination_condition)
#            opti_end_time = read_time.time() - opti_start_time
#            print("Optimization done. (%f seconds.)" % (opti_end_time))
#        except:
#            # Try to get a solution within max defined solving time
#            print('Error:', sys.exc_info())
#            opti_start_time = read_time.time()
#            solver.options['TimeLimit'] = options['Solve']['TimeLimitMax']
#            results = solver.solve(model, report_timing=True, tee=True, logfile='log_file_upper.log')
#            print('TerminationCondition', results.solver.termination_condition)
#            opti_end_time = read_time.time() - opti_start_time
#            print("Optimization done. (%f seconds.)" % (opti_end_time))
#
#    status = 'feasible'
#
#    if results.solver.termination_condition == TerminationCondition.infeasibleOrUnbounded or \
#            results.solver.termination_condition == TerminationCondition.infeasible:
#        solver_parameters = "ResultFile=model.ilp"  # write an ILP file to print the IIS
#        results = solver.solve(model, tee=True, logfile='log_file_lower.log', options_string=solver_parameters)
#        print('model infeasible, solver status', results.solver.termination_condition)
#        print(log_infeasible_constraints(model))
#
#    res_control_horizon = {
#        'solving_time': [],
#        'Mode 0': [],
#        'Mode 1': [],
#        'Mode 2': [],
#        'Q_Sto': [],
#        'Q_HP': [],
#        'Q_Hou_Dem': [],
#        'Q_Hou': [],
#        'Q_Sto_Loss': [],
#        'P_EL': [],
#        'P_EL_HP': [],
#        'P_EL_Dem': [],
#        'P_EL_Grid': [],
#        'P_PV_Grid': [],
#        'P_PV_Use': [],
#        'P_PV': [],
#        'COP_Carnot': [],
#        'COP_HP': [],
#        'T_Outside': [],
#        'T_Sto': [],
#        'T_HP_VL': [],
#        'T_HP_RL': [],
#        'T_Hou_VL': [],
#        'T_Hou_RL': [],
#        'c_total': [],
#        'c_revenue': [],
#        'total_costs': [],
#        # 'm_Sto_water'             : [],
#
#    }
#
#    results_horizon = int((params['control_horizon'] / params['time_step']))
#    for t in range(results_horizon):
#        #  if status == 'infeasible':
#        #     for res in res_control_horizon:
#        #        res_control_horizon[res].append()
#
#        res_control_horizon['solving_time'].append(opti_end_time)
#        res_control_horizon['Mode 0'].append(value(model.HP_off[t]))
#        res_control_horizon['Mode 1'].append(value(model.HP_hot[t]))
#        res_control_horizon['Mode 2'].append(model.HP_cold[t])
#        res_control_horizon['Q_Sto'].append(value(model.Q_Sto[t]))
#        res_control_horizon['Q_HP'].append(value(model.Q_HP[t]))
#        res_control_horizon['Q_Hou_Dem'].append(Q_Hou_Dem[t])
#        res_control_horizon['Q_Hou'].append(value(model.Q_Hou[t]))
#        res_control_horizon['Q_Sto_Loss'].append(value(model.Q_Sto_Loss[t]))
#        res_control_horizon['P_EL'].append(value(model.P_EL[t]))
#        res_control_horizon['P_EL_HP'].append(value(model.P_EL_HP[t]))
#        res_control_horizon['P_EL_Dem'].append(P_EL_Dem[t])
#        res_control_horizon['P_PV'].append(value(model.P_PV[t]))
#        #        res_control_horizon['P_PV_Use'].append(model.P_PV_Use[t])
#        res_control_horizon['P_PV_Grid'].append(model.P_PV_Grid[t])
#        res_control_horizon['P_EL_Grid'].append(model.P_EL_Grid[t])
#        res_control_horizon['COP_Carnot'].append(value(model.COP_Carnot[t]))
#        res_control_horizon['COP_HP'].append(value(model.COP_HP[t]))
#        res_control_horizon['T_Outside'].append(T_Air[t])
#        res_control_horizon['T_Sto'].append(value(model.T_Sto[t]))
#        res_control_horizon['T_HP_VL'].append(value(model.T_HP_VL[t]))
#        res_control_horizon['T_HP_RL'].append(value(model.T_HP_RL[t]))
#        res_control_horizon['T_Hou_VL'].append(value(model.T_Hou_VL[t]))
#        res_control_horizon['T_Hou_RL'].append(value(model.T_Hou_RL[t]))
#        #        res_control_horizon['c_total'].append(value(model.c_cost_sum))
#        res_control_horizon['c_revenue'].append(model.c_revenue)
#        res_control_horizon['total_costs'].append(model.total_costs)
#    #    model.pprint()
#    #    print(res_control_horizon['P_EL'])
#    return res_control_horizon
#
#
#
#
## Idee für Kosten
#
#    def Cost_for_Power(m, t):
#        if value(m.Feed_In[t]):
#            return(m.c_cost[t] == 0)
#        else:
#            if options['Tariff']['Variable']:
#                return(m.c_cost[t] == m.P_EL[t] * c_grid[t])
#            else:
#                return(m.c_cost[t] == m.P_EL[t] * c_grid)
#    model.Cost_for_Power = Constraint(time, rule= Cost_for_Power, name= 'Cost_for_Power')
#
#    def Return_for_Feed_in(m,t):
#        if value(m.Feed_In[t]) != 0:
#            return (m.c_earning[t] == m.P_EL[t] * c_payment)
#        else:
#            return (m.c_earning[t] == 0)
#    model.Return_for_Feed_in = Constraint(time, rule= Return_for_Feed_in, name='Return_for_Feed_in')
#
#'Idee Ende'
#
#
#def check_float_list(lst):
#    for i in lst:
#        if not isinstance(i, float):
#            return False
#    return True
#print(check_float_list(time_series['T_Air']))


import csv
import pandas as pd
import numpy as np
import pickle



dT = pd.read_csv('input_data/Opti_Input/Temperature_Berlin.csv', skiprows=0)
T_Air = (dT.iloc[:, 1] + 273.15)
dQ = pd.read_csv('input_data/Opti_Input/Q_Dem/Q_Heat_Dem_lnorma.csv')
dQ = dQ.iloc[:,1]
Q_Hou_Dem    = dQ.sum(axis=1)

P_PV_list = pd.read_csv('input_data/Opti_Input/P_PV/P_PV_TRY_normal.csv')
P_PV_list = P_PV_list.values.tolist()
P_PV = [item for sublist in P_PV_list for item in sublist]

P_EL_Dem = np.loadtxt('input_data/Opti_Input/ELHour.txt')

TWW = pd.read_csv('input_data/ClusteredYear/ClusteredYear_normal_fix.csv')


QTWW = TWW.iloc[:,4]
fTWW = TWW.iloc[:,7]
TpTWW =TWW.iloc[:,5]

dW = pd.read_csv('input_data/Opti_Input/Wind_Speed_Berlin.csv', skiprows=0)
Win_Speed= dW.iloc[:, 1]

dH = pd.read_csv('input_data/Opti_Input/Global_Radiation_Berlin.csv', skiprows=0)
HGloHor= dH.iloc[:, 1]

xp = np.arange(0.0, 8784, 1.0)
xnew = np.arange(0.0, 8784, 0.25)

Liste1 = T_Air.tolist()
T_Input = np.interp(xnew, xp, Liste1)

Liste2 = Q_Hou_Dem
Q_Hou = np.interp(xnew, xp, Liste2)

Liste3 = P_PV
PV = np.interp(xnew, xp, Liste3)

Liste4 = P_EL_Dem
PEL = np.interp(xnew, xp, Liste4)


#list(zip(T_Air, Q_Hou_Dem, P_PV, P_EL_Dem, QTWW, TpTWW, fTWW, Win_Speed, HGloHor))

Data = list(zip(T_Input, Q_Hou, PV, PEL, QTWW, TpTWW, fTWW))
print(list(zip(T_Input, Q_Hou, PV, PEL)))
with open(f"InputYear_normal.csv", "w", newline="") as f:
    writer = csv.writer(f)
#    for values in zip(T_Air, Q_Hou_Dem, P_PV, P_EL_Dem, QTWW, TpTWW, fTWW, Win_Speed, HGloHor):
    for values in Data:
        writer.writerow(values)




