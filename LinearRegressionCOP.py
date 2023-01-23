# -*- coding: utf-8 -*-
"""
Developed by:  Dominik Pell
               E.ON Energy Research Center,
               Institute for Energy Efficient Buildings and Indoor Climate,
               RWTH Aachen University,
               Germany
Developed in:  2021/2022

Third level file - Linear regression of COP in given
temperature range and with given Carnot efficiency
Separate regression for heating & cooling application necessary,
as COP_Carnot equation is used
"""
import numpy as np
import pwlf
import parameter as parameters
import matplotlib.pyplot as plt
"""

def LinReg_cool(f_c, T_supply_min, T_supply_max, T_air_min, T_air_max):
    # 10 data points in given range
    x = [i for i in np.linspace(T_air_min - 273.15, T_air_max - 273.15, 10)]  # Hot Side
    y = [j for j in np.linspace(T_supply_min - 273.15, T_supply_max - 273.15, 10)]  # Cold Side

    # Empty Data Matrix for COP_Carnot
    dat = np.zeros((len(x), len(y)))
    for i in range(0, len(x)):
        for j in range(0, len(y)):
            dat[i, j] = f_c * (273.15 + y[j]) / (x[i] - y[j])

    T_supply_points = np.zeros((len(x), 1))
    COP_points = np.zeros((len(x), 1))

    for i in range(0, len(x)):
        model = pwlf.PiecewiseLinFit(y, dat[i, :])
        breakpoints = model.fit(2)  # 2 lineare sections

        T_supply_points[i, 0]  = 35 + 273.15
        T_supply_points[i, 1]  = 70 + 273.15

#        T_supply_points[i, 0] = x[i] + 273.15
#        T_supply_points[i, 1] = breakpoints[0] + 273.15
#        T_supply_points[i, 2] = breakpoints[1] + 273.15
#        T_supply_points[i, 3] = breakpoints[2] + 273.15
        COP_points[i, 0] = x[i] + 273.15
        COP_points[i, 1] = model.beta[0]
        COP_points[i, 2] = model.beta[0] + model.slopes[0] * (breakpoints[1] - breakpoints[0])
        COP_points[i, 3] = COP_points[i, 2] + model.slopes[1] * (breakpoints[2] - breakpoints[1])
    return T_supply_points, COP_points
"""

def LinReg_heat(f_c, T_supply_min, T_supply_max, T_air_min, T_air_max):
    x = [i for i in np.linspace(T_supply_min - 273.15, T_supply_max - 273.15, 10)]  # Hot Side
    y = [j for j in np.linspace(T_air_min - 273.15, T_air_max - 273.15, 10)]  # Cold Side
    # Empty Data Matrix for COP_Carnot
    dat = np.zeros((len(x), len(y)))
    for i in range(0, len(x)):
        for j in range(0, len(y)):
            dat[i, j] = f_c * (273.15 + x[i]) / (x[i] - y[j])

    T_supply_points = np.zeros((len(y), 4))
    COP_points = np.zeros((len(y), 4))

    for j in range(0, len(y)):
        model = pwlf.PiecewiseLinFit(x, dat[:, j])
        breakpoints = model.fit(2)  # 2 lineare Abschnitte

        T_supply_points[j, 0] = y[j] + 273.15
        T_supply_points[j, 1] = breakpoints[0] + 273.15
        T_supply_points[j, 2] = breakpoints[1] + 273.15
        T_supply_points[j, 3] = breakpoints[2] + 273.15
        COP_points[j, 0] = y[j] + 273.15
        COP_points[j, 1] = model.beta[0]
        COP_points[j, 2] = model.beta[0] + model.slopes[0] * (breakpoints[1] - breakpoints[0])
        COP_points[j, 3] = COP_points[j, 2] + model.slopes[1] * (breakpoints[2] - breakpoints[1])
##        COP_points[j, 3] = (model.beta[0] + model.slopes[0] * (breakpoints[1] - breakpoints[0])) + (model.slopes[1] * (breakpoints[2] - breakpoints[1]))

    return T_supply_points, COP_points

# FOR TESTING
if __name__ == "__main__":
    eco, devs, year = parameters.load_params()
    f_c = devs['HP']['eta_HP']
    T_supply_min = devs['HP']['T_HP_VL_1'] + 273.15
    T_supply_max = devs['HP']['T_HP_VL_2'] + 273.15
    T_air_min = -20 + 273.15
    T_air_max = 15 + 273.15

    T_supply_points_heat, COP_points_heat = LinReg_heat(f_c, T_supply_min, T_supply_max, T_air_min, T_air_max)
    print(T_supply_points_heat)
    print(COP_points_heat)
 #   T_supply_min = 15 + 273.15
 #   T_supply_max = 25 + 273.15
 #   T_air_min = 27 + 273.15
 #   T_air_max = 45 + 273.15

 #   T_supply_points_cool, COP_points_cool = LinReg_cool(f_c, T_supply_min, T_supply_max, T_air_min, T_air_max)
 #   print(T_supply_points_cool)
 #   print(COP_points_cool)