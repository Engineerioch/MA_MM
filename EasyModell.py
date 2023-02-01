from pyomo.environ import *
from pyomo.util.infeasible import log_infeasible_constraints
from pyomo.opt import UnknownSolver
from pyomo.opt.base.solvers import SolverFactoryClass
from pyomo.gdp import *
from pyomo.opt import SolverStatus, TerminationCondition
import time as read_time
import sys
import copy
import time as read_time






def runeasyModell(params, options, eco, time_series, devs, end):
    # Set parameter
    dt = params['time_step']  # time Step in hours
    start_time = params['start_time']
    prediction_horizon = params['prediction_horizon']
    time_range = range(int(prediction_horizon * (1 / params['time_step'])) + 1)
    time = range(int(prediction_horizon / params['time_step']))
    delta_t = params['time_step'] * 3600  # time Step in seconds

    # Set economic parameter - set in parameter.py -> eco
    #    c_grid_var          =   time_series['c_grid_var']                # [Euro/kWh]   Variable grid charges Stromnetze Berlin
    #    c_grid              =   eco['costs']['c_grid_dem']                  # [Euro/kWh]   Grid charges with fix Price Berlin
    c_payment = eco['costs']['c_payment']  # [Euro/kWh]    Feed in tariff
    c_grid = time_series['c_grid']
    c_comfort = eco['costs']['c_comfort']

    # Set PV profile
    P_PV = time_series['P_PV']
    P_PV_Max = devs['PV']['n_mod'] * devs['PV']['P_PV_Module']  # [kW] maximum Sum Power of all PV-Modules
    P_PV_Min = devs['PV']['P_PV_Min']

    # Set Heat storage parameters
    T_Sto_max = devs['Sto']['T_Sto_max']
    T_Sto_min = devs['Sto']['T_Sto_min']
    m_Sto_water = devs['Sto']['Volume'] * devs['Nature']['Roh_water']
    T_Sto_Env = devs['Sto']['T_Sto_Env']
    U_Sto = devs['Sto']['U_Sto']
    Cap_Sto = devs['Sto']['Volume'] * devs['Nature']['c_w_water']
    T_Kalt = devs['Sto']['T_Kalt']
    #    A_Sto               =   devs['Sto']['A_Sto']
    T_Sto_Init = devs['Sto']['T_Sto_Init']
    Q_Sto_min = m_Sto_water * devs['Nature']['c_w_water'] * T_Sto_min
    Q_Sto_max = m_Sto_water * devs['Nature']['c_w_water'] * T_Sto_max

    # Set Consumer parameter
    T_Hou_delta_max = devs['Hou']['T_Hou_delta_max']
    P_EL_Dem = time_series['P_EL_Dem']
    m_flow_Hou = devs['Hou']['m_flow_Hou']
    Q_Hou_Dem = time_series['Q_Hou_Dem']  # [W] Heat Demand of House

    # Set Heat Pump parameters
    m_flow_HP = devs['HP']['m_flow_HP']
    eta_HP = devs['HP']['eta_HP']  # [-] Gütegrad HP
    Q_HP_Max = devs['HP']['Q_HP_Max']  # [W] Maximum Power of Heat Pump
    Q_HP_Min = devs['HP']['Q_HP_Min']  # [W] Minimum Power of Heat Pump
    T_HP_VL_1 = devs['HP']['T_HP_VL_1']  # [K] Vorlauftemperatur der Wärmepumpe im Modus "1", = 70°C
    T_HP_VL_2 = devs['HP']['T_HP_VL_2']  # [K] Vorlauftemperatur der Wärmepumpe im Modus "2", = 35°C
    T_HP_VL_3 = devs['HP']['T_HP_VL_3']  # [K] Vorlauftemperatur im Modus "Off", = 20°C
    T_HP_VL_Init = options['Initial']['T_HP_VL_Init']

    # Set Natural Parameters
    c_w_water = devs['Nature']['c_w_water']
    T_Input = time_series['T_Air'] + 273.15  # [K]  Außentemperatur
    # Test BigM
    BigM = 1000
    T_HP_RL_Init = T_Sto_Init - 2

    initials_test = {
        'Q_Sto' : (T_Sto_Init - T_Sto_Env) * m_Sto_water * c_w_water,
        'T_Sto' : T_Sto_Init,
#        'Q_HP'  : m_flow_HP * c_w_water * (T_HP_VL_Init - T_HP_RL_Init),
#        'T_HP_VL': T_HP_VL_Init,
#        'T_HP_RL' : T_HP_RL_Init,
#        'P_EL_HP' : m_flow_HP * c_w_water * (T_HP_VL_Init - T_HP_RL_Init) / 2,
        'P_EL_Dem': P_EL_Dem[start_time],
        'T_Hou_VL' : T_Sto_Init + 2,
        'Q_Hou' : Q_Hou_Dem[start_time],
        'T_Air' : T_Input[start_time],
        'T_Hou_RL': (T_Sto_Init + 2) - (Q_Hou_Dem[start_time] / (m_flow_Hou * c_w_water)),
    }


    model = ConcreteModel()

#    model.P_PV = Var(time, within=NonNegativeReals , name = 'P_PV')
    model.Q_Hou = Var(time, within= NonNegativeReals, name='Q_Hou', initialize=initials_test['Q_Hou'])
    model.P_EL_Dem = Var(time, within=NonNegativeReals, name='P_EL_Dem', initialize=initials_test['P_EL_Dem'])
    model.T_Air = Var(time, within=Reals, name='T_Air', initialize=initials_test['T_Air'])
    model.T_HP_VL = Var(time, within=NonNegativeReals, name='T_HP_VL')#, initialize=initials_test['T_HP_VL'])
    model.T_HP_RL = Var(time, within=NonNegativeReals, name='T_HP_RL')#, initialize=initials_test['T_HP_RL'])
    model.P_EL_HP = Var(time, within=NonNegativeReals, name='P_EL_HP')#, bounds=(0, 5000), initialize=initials_test['P_EL_HP'])
    model.Q_HP = Var(time,within=NonNegativeReals, name='Q_HP', bounds= (0, 10000))#, initialize=initials_test['Q_HP'])
    model.Q_Sto = Var(time, within=NonNegativeReals, name='Q_Sto', initialize=initials_test['Q_Sto'])
    model.T_Sto = Var(time, within=NonNegativeReals, name='T_Sto', initialize=T_Sto_Init)
#    model.Q_Sto_Change = Var(time, within=Reals, name= 'Q_Sto_Change', initialize=initials_test['Q_HP'] - initials_test['Q_Hou'])
    model.T_Hou_VL = Var(time, within=NonNegativeReals, name='T_Hou_VL', initialize=initials_test['T_Hou_VL'])
    model.T_Hou_RL = Var(time, within=NonNegativeReals, name='T_Hou_RL', initialize=initials_test['T_Hou_RL'])
    model.P_EL = Var(time, within=Reals, name='P_EL')#, initialize=initials_test['P_EL_Dem'] - initials_test['P_EL_HP'])
    model.P_PV = Var(time, within=Reals, name='P_PV')
    model.c_cost = Var(     within=NonNegativeReals, name='c_cost', initialize=0)
    model.costs_total = Var(within=Reals, name='costs_total', initialize=0)
    model.Q_Penalty = Var(time, within=NonNegativeReals, name='Q_Penalty')
    model.c_power = Var(time, within=Reals, name='c_power')
    model.c_penalty = Var(time, within=NonNegativeReals, name='c_penalty')
    model.No_Feed_In = Var(time, within=Binary, name='No_Feed_In')
    model.HP_off = Var(time, within=Binary, name='HP_off')
    model.HP_mode1 = Var(time, within=Binary, name='HP_mode1')
    model.HP_mode2 = Var(time, within=Binary, name='HP_mode2')
    model.Mode = Var(time, within=Reals, name='Mode')
    model.c_revenue = Var(time, within=NonPositiveReals, name='c_revenue')
    model.COP_HP = Var(time, within=NonNegativeReals, name='COP_HP')
    model.COP_Carnot = Var(time, within=NonNegativeReals, name='COP_Carnot')




    def Heat_to_House_equals_Demand(m, t):
        return (m.Q_Hou[t] >= Q_Hou_Dem[t + start_time])
    model.Heat_to_House_equals_Demand = Constraint(time, rule=Heat_to_House_equals_Demand, name=Heat_to_House_equals_Demand)

    def Power_Demand_In_House(m, t):
        return(m.P_EL_Dem[t] == P_EL_Dem[t + start_time])
    model.Power_Demand_In_House = Constraint(time, rule= Power_Demand_In_House, name= 'Power_Demand_In_House')

    def Temp_Outside(m, t):
        return(m.T_Air[t] == T_Input[t + start_time])
    model.Temp_Outside = Constraint(time, rule= Temp_Outside, name='Temp_Outside')

    def PV_Import(m, t):
        return(m.P_PV[t] == P_PV[t + start_time])
    model.PV_Import = Constraint(time, rule=PV_Import, name='PV_Import')

###################################################################################
    def Heat_Sum(m, t):
        return(m.Q_Hou[t] <= m.Q_HP[t] + m.Q_Penalty[t])
    model.Heat_Sum = Constraint(time, rule=Heat_Sum, name='Heat_Sum')

    def HP_Modes(m, t):
        return(m.HP_off[t] + m.HP_mode1[t] + m.HP_mode2[t] == 1)
    model.HP_Modes = Constraint(time, rule= HP_Modes, name='HP_Modes')

#    def HP_off(disj, t):
#        m= disj.model()
#        disj.hp_1 = Constraint(expr=m.HP_off[t] == 1)
#        disj.hp_2 = Constraint(expr=m.Q_HP[t] == 0)
#        disj.hp_3 = Constraint(expr=m.T_HP_VL[t] == 293.15)
#    model.HP_off = Disjunct(time, rule=HP_off)

#    def HP_mode1(disj, t):
#        m= disj.model()
#        disj.hp_1 = Constraint(expr=m.HP_mode1[t] == 1)
#        disj.hp_2 = Constraint(expr=m.Q_HP[t] >= 0)
#        disj.hp_3 = Constraint(expr=m.T_HP_VL[t] == T_HP_VL_1)
#    model.HP_mode1 = Disjunct(time, rule=HP_mode1)

#    def HP_mode2(disj, t):
#        m = disj.model()
#        disj.hp_1 = Constraint(expr=m.HP_mode2[t] == 1)
#        disj.hp_2 = Constraint(expr=m.Q_HP[t] >= 0)
#        disj.hp_3 = Constraint(expr=m.T_HP_VL[t] == T_HP_VL_2)
#    model.HP_mode2 = Disjunct(time, rule=HP_mode2)

#    def HP_modes(m, t):
#        return[m.HP_off[t], m.HP_mode1[t], m.HP_mode2[t]]
#    model.HP_modes = Disjunction(time, rule=HP_modes)


    def Operation_Temp(m, t):
        return (m.T_HP_VL[t] == m.HP_mode1[t] * T_HP_VL_1 + m.HP_mode2[t] * T_HP_VL_2 + m.HP_off[t] * T_HP_VL_3)
    model.Operation_Temp = Constraint(time, rule=Operation_Temp, name='Operation_Temp')

    def Heat_Power_HP(m, t):
        return (m.Q_HP[t] == m_flow_HP * c_w_water * (m.T_HP_VL[t] - 293.15)) # T_HP_RL_[t])
    model.Heat_Power_HP = Constraint(time, rule=Heat_Power_HP, name='Heat_Power_HP')

    def Display_HP_Mode(m,t):
        return (m.Mode[t] == 0 * m.HP_off[t] + 1 * m.HP_mode1[t] + 2 * m.HP_mode2[t])
    model.Display_HP_Mode = Constraint(time, rule=Display_HP_Mode, name='Display_HP_Mode')

    def power_balance(m, t):
        return(m.P_EL[t] == m.P_EL_Dem[t] + m.P_EL_HP[t] - m.P_PV[t])
    model.power_balance = Constraint(time, rule = power_balance, name = 'Power_balance')

    def Cost_for_Power(m, t):
        return (m.c_power[t] == m.No_Feed_In[t] * c_grid[t] * m.P_EL[t])
    model.Cost_for_Power = Constraint(time, rule= Cost_for_Power, name= 'Cost_for_Power')

    def Revenue_for_Power(m, t):
        return (m.c_revenue[t] == (1 - m.No_Feed_In[t]) * c_payment * m.P_EL[t])
    model.Revenue_for_Power = Constraint(time, rule=Revenue_for_Power, name='Revenue_for_Power')
    def Define_Feed_Binary(m, t):
        return (m.P_EL[t] * m.No_Feed_In[t] >= 0)
    model.Define_Feed_Binary = Constraint(time, rule= Define_Feed_Binary, name='Define_Feed_Binary')

    def Power_from_HP(m, t):
        return (m.P_EL_HP[t] == m.Q_HP[t] / 2 )
    model.Power_from_HP = Constraint(time, rule= Power_from_HP, name='Power_from_HP')

 #   def CoP_HP(m, t):
#        return(m.COP_HP[t] == m.COP_Carnot[t] * eta_HP)
#    model.CoP_HP = Constraint(time, rule=CoP_HP, name='CoP_HP')

#    def CoP_Carnot(m, t):
#        return(m.COP_Carnot[t] == m.T_HP_VL[t] / (m.T_HP_VL[t] - m.T_Air[t]))
#    model.CoP_Carnot = Constraint(time, rule=CoP_Carnot, name='CoP_Carnot')


    def Costs_of_Penalty(m, t):
        return (m.c_penalty[t] == m.Q_Penalty[t] * c_comfort)
    model.Costs_of_Penalty = Constraint(time, rule=Costs_of_Penalty, name='Costs_of_Penalty')

    def PHP(m, t):
        return (m.costs_total == sum(m.c_power[t] + m.c_revenue[t] + m.c_penalty[t] for t in time))
    model.PHP = Constraint(time, rule=PHP, name ='PHP')

    def objective_rule(m):
        return (m.costs_total)
    model.total_costs = Objective(rule = objective_rule, sense = minimize, name = 'Minimize total costs')

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
        #'solving_time'      : [],
        #'Mode 0'            : [],
       # 'Mode 1'            : [],
      #  'Mode 2'            : [],
        'Q_Sto'             : [],
        'Q_HP'              : [],
        'Q_Hou_Dem'         : [],
        'Q_Hou'             : [],
     #   'Q_Sto_Loss'        : [],
        'P_EL'              : [],
        'P_EL_HP'           : [],
        'P_EL_Dem'          : [],
        'Q_Penalty'         : [],

        'P_PV'              : [],
 #       'COP_Carnot'        : [],
#        'COP_HP'            : [],
        'T_Air_Input'       : [],
        'T_Air'             : [],
        'T_Sto'             : [],
        'T_HP_VL'           : [],
        'T_HP_RL'           : [],
        'T_Hou_VL'          : [],
        'T_Hou_RL'          : [],
        'c_total'           : [],

        'total_costs'       : [],
        'c_grid'            : [],
        'HP_off'            : [],
        'HP_mode1'          : [],
        'HP_mode2'          : [],
        'Mode'              : [],
#        'PEL'               : [],
        #'m_Sto_water'       : [],

    }
    status = 'feasible'
    results_horizon = int((params['control_horizon'] / params['time_step']))
    print('Results_Horizont ist:',  results_horizon)
    for t in range(results_horizon):
        if status == 'infeasible':
            for res in res_control_horizon:
                res_control_horizon[res].append(0)


#        res_control_horizon['solving_time'].append(opti_end_time)
    #    res_control_horizon['Mode 0'].append(value(model.HP_off[t]))
   #     res_control_horizon['Mode 1'].append(value(model.HP_mode1[t]))
  #      res_control_horizon['Mode 2'].append(model.HP_mode2[t])
        res_control_horizon['Q_Sto'].append(value(model.Q_Sto[t]))
        res_control_horizon['Q_HP'].append(value(model.Q_HP[t]))
        res_control_horizon['Q_Hou_Dem'].append(Q_Hou_Dem[t])
        res_control_horizon['Q_Hou'].append(value(model.Q_Hou[t]))
  #      res_control_horizon['Q_Sto_Loss'].append(value(model.Q_Sto_Loss[t]))
        res_control_horizon['P_EL'].append(value(model.P_EL[t]))
        res_control_horizon['P_EL_HP'].append(value(model.P_EL_HP[t]))
        res_control_horizon['P_EL_Dem'].append(value(model.P_EL_Dem[t]))
        res_control_horizon['Q_Penalty'].append(value(model.Q_Penalty[t]))
        res_control_horizon['P_PV'].append(value(model.P_PV[t]))
  #      res_control_horizon['COP_Carnot'].append(value(model.COP_Carnot[t]))
  #      res_control_horizon['COP_HP'].append(value(model.COP_HP[t]))
        res_control_horizon['T_Air_Input'].append(T_Input[t])
        res_control_horizon['T_Air'].append(value(model.T_Air[t]))
        res_control_horizon['T_Sto'].append(value(model.T_Sto[t]))
        res_control_horizon['T_HP_VL'].append(value(model.T_HP_VL[t]))
#        res_control_horizon['T_HP_RL'].append(value(model.T_HP_RL[t]))
        res_control_horizon['T_Hou_VL'].append(value(model.T_Hou_VL[t]))
        res_control_horizon['T_Hou_RL'].append(value(model.T_Hou_RL[t]))
        res_control_horizon['c_total'].append(value(model.costs_total))
        res_control_horizon['HP_off'].append(value(model.HP_off[t]))
        res_control_horizon['HP_mode1'].append(value(model.HP_mode1[t]))
        res_control_horizon['HP_mode2'].append(value(model.HP_mode2[t]))
        res_control_horizon['Mode'].append(value(model.Mode[t]))
 #       res_control_horizon['total_costs'].append(model.total_costs)
    model.pprint()
#    print(res_control_horizon['P_EL'])
    return res_control_horizon