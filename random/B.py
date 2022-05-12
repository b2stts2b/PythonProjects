import sys
import numpy as np

def T_tr(d_x):
	return np.array([[1, d_x], [0, 1]])
def T_br(f):
	return np.array([[1, 0], [-1/f,1]])

f1, f2, L, a = list(map(int, sys.argv[1:5]))

# Matrices
T_a = T_tr(a)
T_L = T_tr(L)
T_br1 = T_br(f1)
T_br2 = T_br(f2)

# Tsys and f_eff
T_sys = T_br2.dot(T_L.dot(T_br1))
f_eff = -1/T_sys[1,0]

# Calc b 
T_sys_a = T_sys.dot(T_a)
b = -T_sys_a[0,1]/T_sys_a[1,1]
T_b = np.array([[1, b], [0, 1]])

# 
T_sys_x = T_b.dot(T_sys_a)
M = T_sys_x[0,0]

print(f"Tsys: A:{T_sys[0,0]}, B:{T_sys[0,1]} , C:{T_sys[1,0]} , D:{T_sys[1,1]} ")
print(f"feff: {f_eff}, b: {b}, M: {M}")
print(f"TsysX: A:{T_sys_x[0,0]}, B:{T_sys_x[0,1]} , C:{T_sys_x[1,0]} , D:{T_sys_x[1,1]} ")