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


def run_MPC(params, options, eco, time_series, devs):
    time                =   range(int(params['prediction_horizon'] * 1/ params['time_step']))
    P_PV                =   time_series['P_PV']

    P_EL_Dem            =   time_series['P_EL_Dem']
#    m_flow_Hou          =   devs['Hou']['m_flow_Hou']
    Q_Hou_Dem           =   time_series['Q_Hou_Dem']

    T_Air               =   time_series['T_Air'] + 273.15



    # Initialize model
    model = ConcreteModel()


    model.P_EL          = Var(time, within = Reals,             name = 'P_EL', initialize = P_EL_Dem[0])
    model.T_HP_VL = Var(time, within=NonNegativeReals, name='T_HP_VL')
    model.P_EL_HP       = Var(time, within = NonNegativeReals,  name = 'P_EL_HP', initialize = 0)
    model.P_PV_Import          = Var(time, within = NonNegativeReals,  name = 'P_PV_Import')#, initialize= P_PV[0])
    model.P_EL_D      = Var(time, within = Reals,             name = 'P_EL_D', initialize=P_EL_Dem[0])
    model.Q_Hou         = Var(time, within = Reals,             name = 'Q_Hou', initialize= Q_Hou_Dem[0])
    model.P_EL_Sum = Var(within=Reals, name='P_EL_Sum')
    model.T_Outside = Var(time, within=Reals, name='T_Outside', initialize=T_Air[0])

    def Import_PV(m, t):
        return (m.P_PV_Import[t] == (P_PV[t]))
    model.Import_PV = Constraint(time, rule=Import_PV, name='Import_PV')

    def Cost_sum(m):
        return (m.P_EL_Sum == sum(m.P_EL[t]+ m.P_PV_Import[t] for t in time))
    model.Cost_sum = Constraint(rule= Cost_sum, name = 'Cost_sum')



    def objective_rule(m):
        return (m.P_EL_Sum)

    #        return (m.c_revenue + m.c_cost_sum)
    model.total_costs = Objective(rule=objective_rule, sense=minimize, name='Minimize total costs')

    results = SolverFactory('gurobi').solve(model, tee=True, logfile='my_log_file.log')
    if options['Solve']['type'] == 'gurobi':
        solver = SolverFactory('gurobi')
        solver.options['Presolve'] = 2
        solver.options['mipgap'] = options['Solve']['MIP_gap']
        solver.options['TimeLimit'] = options['Solve']['TimeLimit']
        solver.options['DualReductions'] = 0

    elif options['Solve']['type'] == 'glpk':
        solver = SolverFactory('glpk')
        #    solver.options['Presolve'] = 2
        solver.options['mipgap'] = options['Solve']['MIP_gap']
        solver.options['TimeLimit'] = options['Solve']['TimeLimit']

    try:
        opti_start_time = read_time.time()
        results = solver.solve(model, report_timing=True, tee=True, logfile='log_file_upper.log')
        log_infeasible_constraints(model)
        print('TerminationCondition', results.solver.termination_condition)
        # Get solving time
        opti_end_time = read_time.time() - opti_start_time
        print("Optimization done. (%f seconds.)" % (opti_end_time))

    except:
        print('Error:', sys.exc_info())
        try:
            # Try to get a solution within a longer solving time
            opti_start_time = read_time.time()
            solver.options['TimeLimit'] = options['Solve']['TimeLimit'] * 2
            results = solver.solve(model, report_timing=True, tee=True, logfile='log_file_upper.log')
            print('TerminationCondition', results.solver.termination_condition)
            opti_end_time = read_time.time() - opti_start_time
            print("Optimization done. (%f seconds.)" % (opti_end_time))
        except:
            # Try to get a solution within max defined solving time
            print('Error:', sys.exc_info())
            opti_start_time = read_time.time()
            solver.options['TimeLimit'] = options['Solve']['TimeLimitMax']
            results = solver.solve(model, report_timing=True, tee=True, logfile='log_file_upper.log')
            print('TerminationCondition', results.solver.termination_condition)
            opti_end_time = read_time.time() - opti_start_time
            print("Optimization done. (%f seconds.)" % (opti_end_time))

    status = 'feasible'

    if results.solver.termination_condition == TerminationCondition.infeasibleOrUnbounded or \
            results.solver.termination_condition == TerminationCondition.infeasible:
        solver_parameters = "ResultFile=model.ilp"  # write an ILP file to print the IIS
        results = solver.solve(model, tee=True, logfile='log_file_lower.log', options_string=solver_parameters)
        print('model infeasible, solver status', results.solver.termination_condition)
        print(log_infeasible_constraints(model))

    res_control_horizon = {
        'solving_time' : [],
        'P_EL'  : [],
        'P_PV_Import' : [],
        'P_EL_D'    : [],
        'Q_Hou' :[],
        'T_Outside' : [],
    }

    results_horizon = int((params['control_horizon'] / params['time_step']))
    for t in range(results_horizon):
   #       if status == 'infeasible':
  #           for res in res_control_horizon:
 #               res_control_horizon[res].append()

        res_control_horizon['solving_time'].append(opti_end_time)
        res_control_horizon['P_EL'].append(value(model.P_EL[t]))
        res_control_horizon['P_PV_Import'].append(value(model.P_PV_Import[t]))
        res_control_horizon['P_EL_D'].append(model.P_EL_D[t])
        res_control_horizon['Q_Hou'].append(value(model.Q_Hou[t]))
        res_control_horizon['T_Outside'].append(value(model.T_Outside[t]))
    model.pprint()
    return(res_control_horizon)