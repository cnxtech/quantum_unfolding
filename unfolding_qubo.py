#!/usr/bin/env python3
import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt
from decimal2binary import *
import dimod

np.set_printoptions(precision=1, linewidth=200, suppress=True)

# truth-level:
x = [5, 10, 3]

# response matrix:
R = [[3, 1, 0], [1, 3, 1], [0, 1, 2]]

# pseudo-data:
d = [32, 40, 15]

# convert to numpy arrays
x = np.array(x, dtype='int8')
R = np.array(R, dtype='int8')
b = np.array(d, dtype='int8')

# closure test
b = np.dot(R, x)

n = 4
N = x.shape[0]

print("INFO: N bins:", N)
print("INFO: n-bits encoding:", n)

lmbd = 0.  # regularization strength
D = laplacian(N)

# convert to bits
x_b = discretize_vector(x, n)
b_b = discretize_vector(b, n)
R_b = discretize_matrix(R, n)
D_b = discretize_matrix(D, n)

print("INFO: Truth-level x:")
print(x, x_b)
print("INFO: pseudo-data b:")
print(b, b_b)
print("INFO: Response matrix:")
print(R)
print(R_b)
print("INFO: Laplacian operator:")
print(D)
print(D_b)

# Create QUBO operator

# linear constraints
h = {}
for j in range(n*N):
    idx = (j)
    h[idx] = 0
    for i in range(N):
        h[idx] += (R_b[i][j]*R_b[i][j] -
                   2*R_b[i][j] * b[i] +
                   lmbd*D_b[i][j]*D_b[i][j])
    #print("h", idx, ":", h[idx])

# quadratic constraints
J = {}
for j in range(n*N):
    for k in range(j+1, n*N):
        idx = (j, k)
        J[idx] = 0
        for i in range(N):
            J[idx] += 2*(R_b[i][j]*R_b[i][k] + lmbd*D_b[i][j]*D_b[i][k])
        #print("J", idx, ":", J[idx])

# QUBO
bqm = dimod.BinaryQuadraticModel(linear=h,
                                 quadratic=J,
                                 offset=0.0,
                                 vartype=dimod.BINARY)
print("INFO: solving the QUBO model...")
result = dimod.ExactSolver().sample(bqm)
print("INFO: ...done.")

energy_min = 1e15
q = None
for sample, energy in result.data(['sample', 'energy']):
    #print(sample, energy)

    if energy > energy_min:
        continue
    energy_min = energy
    q = list(sample.values())

q = np.array(q)
y = compact_vector(q, n)
print("INFO: best-fit:   ", q, "::", y, ":: E =", energy_min)
print("INFO: truth value:", x_b, "::", x)
