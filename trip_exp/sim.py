#!/usr/bin/env python

from trip_rules import *
from trip_definitions import *
import pickle
import sys

def sim_days(name, num):
	core_params = [0.001, 0.001, 0.002, 0.0015, 0.003, 0.025, 0.005, 0.04]
	rule_funcs = [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8]

	simulated_days = []
	wd= 0
	for num_days in range(num):
	    wd = (wd+1)%5 
	    today = PlanningDay(weekday = wd, periods=None)
	    prds = []
	    for i in range(3):
	        is_raining = (np.random.rand() > 0.9)
        	current_period = PlanningPeriod(number=i, rain=is_raining, parameters=None, values=None)
        	params = get_params(today, current_period,rule_funcs, core_params)
        	vals = np.random.poisson(lam=params)
        	current_period = current_period._replace(parameters=params, values=vals)
        	prds.append(current_period)
	    today = today._replace(periods=prds)
	    simulated_days.append(today)

    
	out_values = [[period.values for period in day.periods] for day in simulated_days]
	out_rain = [[period.rain for period in day.periods] for day in simulated_days]
	out = (out_values, out_rain)

	outfile = open(name, 'w')
	pickle.dump(out, outfile)
	outfile.close()

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print 'usage: %s [trainfile] [testfile]' %(sys.argv[0])
		exit(1)
	else:
		sim_days(sys.argv[1], 500)
		sim_days(sys.argv[2], 500)
