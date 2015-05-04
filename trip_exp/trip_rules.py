#!/usr/bin/env python

from math import sqrt

def rain_factor(period):
    if period.rain:
        return 1.2
    return 1

def dist_factor(reg1, reg2):
    dist = 0
    for i in range(2):
        dist += (reg1.coordinates[i]-reg2.coordinates[i])**2
    dist = sqrt(dist)
    return 1/dist

def rule1(reg1, reg2, day, period, core_param):
    if(period.number != 0 or 
        reg1.name == reg2.name or 
        day.weekday > 4):
        return 0
    return core_param * reg1.population * reg2.job_density * rain_factor(period)

def rule2(reg1, reg2, day, period, core_param):
    if(period.number != 1 or
       reg1.name == reg2.name or
       day.weekday >4):
        return 0
    return core_param * reg1.job_density * reg2.population * rain_factor(period)

def rule3(reg1, reg2, day, period, core_param):
    if (period.number != 0 or
        reg1.name == reg2.name or
        day.weekday > 4):
        return 0
    return core_param * reg1.population * reg2.service_density * dist_factor(reg1, reg2) * rain_factor(period)

def rule4(reg1, reg2, day, period, core_param):
    if(period.number != 1  or
       reg1.name == reg2.name or
       day.weekday > 4):
        return 0
    return core_param * reg1.service_density * reg2.population * dist_factor(reg1, reg2) * rain_factor(period)

def rule5(reg1, reg2, day, period, core_param):
    if(period.number != 1 or
       reg1.name == reg2.name or
       day.weekday > 4):
        return 0
    return core_param * reg1.population * reg2.service_density * dist_factor(reg1, reg2) * rain_factor(period)

def rule6(reg1, reg2, day, period, core_param):
    if(period.number != 2 or
       reg1.name == reg2.name or
       day.weekday > 4):
        return 0
    return core_param * reg1.service_density * reg2.population * dist_factor(reg1, reg2) * rain_factor(period)

def rule7(reg1, reg2, day, period, core_param):
    if(period.number != 1 or
       reg1.name == reg2.name or
       day.weekday > 4):
        return 0
    return core_param * reg1.population * reg2.fun_density * dist_factor(reg1, reg2) * rain_factor(period)

def rule8(reg1, reg2, day, period, core_param):
    if(period.number != 2 or
       reg1.name == reg2.name or
       day.weekday > 4):
        return 0
    return core_param * reg1.fun_density * reg2.population * dist_factor(reg1, reg2) * rain_factor(period)
