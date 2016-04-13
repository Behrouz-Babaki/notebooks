import theano
import theano.tensor as T
import numpy as np

x = T.dscalar('x')
m = T.dscalar('mu')
s = T.dscalar('s')

sigma = T.exp(s)
first = 1 / (sigma * T.sqrt(2 * np.pi))
second = T.exp(-T.sqr(x-m)/(2 * T.sqr(sigma)))

f0 = first * second
f_x0 = T.grad(f0, x)
f_m0 = T.grad(f0, m)
f_s0 = T.grad(f0, s)

# compilation
f_noraml = theano.function([x,m,s], f0)
fprime_noraml_x = theano.function([x,m,s], f_x0)
fprime_normal_m = theano.function([x,m,s], f_m0)
fprime_normal_s = theano.function([x,m,s], f_s0)