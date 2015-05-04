#!/usr/bin/env python 

from scipy.stats import poisson
import pickle
from trip_rules import *
from trip_definitions import *
rule_funcs = [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8]

def rule_likelihood(test_data, rule_funcs, core_params):
    (values, rains) = test_data
    res = 0
    num_regions = len(values[0][0])
    for d in range(len(rains)):
        vals = values[d]
        rns = rains[d]
        today = PlanningDay(weekday = d%5, periods=None)
        for i in range(3):
            is_raining = rns[i]
            current_period = PlanningPeriod(number=i, rain=is_raining, parameters=None, values=None)
            params = get_params(today, current_period, rule_funcs, core_params)
            res += sum([np.log(poisson.pmf(vals[i][m,n], params[m,n]))
                        for m in range(num_regions) 
                        for n in range(num_regions) if m!=n])
    return res

def plain_likelihood(data, learned_params, with_rain=True):
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
            if with_rain:
                params = learned_params[is_raining, i]
            else:
                params = learned_params[i]
            res += sum([np.log(poisson.pmf(vals[i][m,n], params[m,n]))
                        for m in range(num_regions) 
                        for n in range(num_regions) if m!=n])
    return res

def learn_params(train_data, with_rain=True):
    values, rains = train_data
    values = np.array(values)
    rains = np.array(rains)
    if with_rain:
    	rain_options = [False, True]
    	params = np.zeros_like([values[0]]*len(rain_options), dtype='float64')
    	for rain in range(len(rain_options)):
        	for period in range(3):
        	    vals = values[:,period,:,:][rains[:,period]==rain_options[rain]]
        	    params[rain, period] = np.ma.average(vals, axis = 0)
    else:
	    params = np.zeros_like(values[0], dtype='float64')
	    for period in range(3):
	        vals = values[:,period,:,:]
	        params[period] = np.ma.average(vals, axis = 0)
    return params


