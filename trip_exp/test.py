#!/usr/bin/env python

from scipy.optimize import minimize
import pickle
from trip_rules import *
from trip_definitions import obj_func
from learn_ll import rule_likelihood, plain_likelihood, learn_params


def max_loglikelihood(data, rule_funcs):
    first_guess = [0.001]*8
    bounds = [(0, None)]*8 #lambdas should be non-negative
    res = minimize(obj_func(data, rule_funcs), first_guess, bounds=bounds, method='L-BFGS-B')
    return res.x

infile = open('/home/behrouz/temp/test_notebooks/simulated_days.pkl')
data = pickle.load(infile)

values, rains = data
num_days = len(values)
num_train = num_days * 1/20

train_data = (values[:num_train], rains[:num_train])
test_data = (values[num_train:], rains[num_train:])

rule_funcs = [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8]

learned_core_params = max_loglikelihood(train_data, rule_funcs)
test_log_likelihood = rule_likelihood(test_data, rule_funcs, learned_core_params)
print test_log_likelihood

lp = learn_params(train_data)
lp2 = learn_params(train_data, with_rain=False)
print plain_likelihood(test_data, lp)
print plain_likelihood(test_data, lp2, with_rain=False)

orig_core_params = [0.001, 0.001, 0.002, 0.0015, 0.003, 0.025, 0.005, 0.04]
print rule_likelihood(test_data, rule_funcs, orig_core_params)
