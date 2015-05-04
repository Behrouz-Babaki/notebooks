#!/usr/bin/env python

from scipy.optimize import minimize
import pickle
from trip_rules import *
from trip_definitions import obj_func
from learn_ll import rule_likelihood, plain_likelihood, learn_params
import sys


def max_loglikelihood(data, rule_funcs):
    first_guess = [0.001]*8
    bounds = [(0, None)]*8 #lambdas should be non-negative
    res = minimize(obj_func(data, rule_funcs), first_guess, bounds=bounds, method='L-BFGS-B')
    return res.x

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print 'usage: %s [train_file] [test_file] [out_file]' % sys.argv[0]
        exit(1)

    rule_funcs = [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8]
    orig_core_params = [0.001, 0.001, 0.002, 0.0015, 0.003, 0.025, 0.005, 0.04]
    trainfile = open(sys.argv[1])
    data = pickle.load(trainfile)
    values, rains = data
    test_data = pickle.load(open(sys.argv[2]))

    results = []
    nt = [20, 50, 100, 200, 500]
    for num_train in nt:
        num_days = len(values)
        train_data = (values[:num_train], rains[:num_train])

        learned_core_params = max_loglikelihood(train_data, rule_funcs)
        lp = learn_params(train_data)
        lp_norain = learn_params(train_data, with_rain=False)
        
        result = dict()
        result['num_train'] = num_train
        result['orig_ll'] = rule_likelihood(test_data, rule_funcs, orig_core_params)
        result['rule_ll'] = rule_likelihood(test_data, rule_funcs, learned_core_params)
        result['plain_ll'] =  plain_likelihood(test_data, lp)
        result['plian_ll_norain'] = plain_likelihood(test_data, lp_norain, with_rain=False)
        results.append(result)
    
    pickle.dump(results, open(sys.argv[3], 'w'))
