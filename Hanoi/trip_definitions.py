#!/usr/bin/env python

from collections import namedtuple
import numpy as np

PlanningDay = namedtuple('Day', ['weekday', 'periods'])
PlanningPeriod = namedtuple('Period', ['number','rain', 'parameters','values'])
PlanningRegion = namedtuple('Region', ['name', 
                                       'coordinates', 
                                       'population', 
                                       'job_density', 
                                       'service_density',
                                       'fun_density'])

names = ['downtown', 'beach', 'cultural', 'res1', 'res2']

coordinates = [[374, 787],
               [489, 497],
               [260, 440],
               [197, 800],
               [440,685]]
populations = [i*1000 for i in [10, 4, 20, 50, 70]]
job_densities = [7, 2, 5, 1, 1]
service_densities = [3, 2, 5, 1, 1]
fun_densities = [2, 6, 4, 1, 1]

regions = [PlanningRegion(names[i],
                          coordinates[i],
                          populations[i],
                          job_densities[i],
                          service_densities[i],
                          fun_densities[i]) for i in range(5)]

def get_params(day, period, rule_funcs, core_params):
    params = [[sum([rule(reg1, reg2, day, period, core_param) 
                    for (rule, core_param) in zip(rule_funcs, core_params)]) 
                  for reg1 in regions]for reg2 in regions]
    return np.array(params)

def obj_func(data, rule_funcs):
    def loglikelihood(core_params):
        (values, rains) = data
        res = 0
        num_regions = len(values[0][0])
        for d in range(len(rains)):
            vals = values[d]
            rns = rains[d]
            today = PlanningDay(weekday = d%7, periods=None)
            for i in range(3):
                is_raining = rns[i]
                current_period = PlanningPeriod(number=i, rain=is_raining, parameters=None, values=None)
                params = get_params(today, current_period,rule_funcs, core_params)
                res += sum([(vals[i][m,n]*np.log(params[m,n])-params[m,n]) 
                            for m in range(num_regions) 
                            for n in range(num_regions) if params[m,n] > 0])
        return -res
    return loglikelihood
