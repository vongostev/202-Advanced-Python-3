import numpy as np
from numba import njit, float64, types, prange
from numba.extending import typeof_impl, type_callable, models, register_model, make_attribute_wrapper, lower_builtin, unbox, NativeValue, box
from numba.core import cgutils
from numba.experimental import jitclass
import math
from dataclasses import dataclass
from matplotlib import pyplot as plt
import unittest
from material import Material

eps = 1e-4
pi = 3.141592653589793

#Usadel и SolveUsadel - функции для решения дифференциального уравнения Узаделя методом прогонки
@njit(fastmath=True, cache=True)
def Usadel(iN, delta, w, G, sconductor, ferro):
    N_S = sconductor.N
    N_F = ferro.H
    N = int(N_S + N_F)
    if iN < sconductor.N:
        wm = complex(w, sconductor.H)
        Ksi = sconductor.Ksi
        h = sconductor.L/(N_S-1)
    else:
        wm = complex(w, ferro.H)
        Ksi = ferro.Ksi
        h = ferro.L/(N_F-1)

    Gb_FS = sconductor.Gb_FS
    D = 2*pi*Ksi**2
    if iN == 0:
        a = 0
        b = 1
        c = 1
        d = 0
    
    if iN > 0 and iN < N-1:
        dG = (G[iN+1]*G[iN+1] - G[iN-1]*G[iN-1])/4/G[iN]/G[iN]
        a = 1 - dG
        b = 2 + 2*wm*h*h/D/G[iN]
        c = 1 + dG
        d = 2*wm*h*h*delta/D/G[iN]
        
    
    if iN == N_S-1:
        ro_F = ferro.Ro
        Ksi_F = ferro.Ksi
        ro_S = sconductor.Ro
        Ksi_S = sconductor.Ksi
        Gb_SF = Gb_FS *ro_F* Ksi_F/ ro_S/ Ksi_S
                
        w1 = complex(w, sconductor.H)
        w2 = complex(w, ferro.H)
        a=-Gb_SF*Ksi
        b=-(Gb_SF*Ksi + G[iN+1]/G[iN]*h)
        c=-G[iN+1]/G[iN]*h *w1/w2
        d=0
    if iN == N_S:
        w1 = complex(w, sconductor.H)
        w2 = complex(w, ferro.H)
        a = G[iN-1]/G[iN]*h *w2/w1
        b = Gb_FS*Ksi + G[iN-1]/G[iN]*h
        c = Gb_FS*Ksi
        d = 0
    
    if iN == N-1:
        a = 1
        b = 1
        c = 0
        d = 0
    coeff = np.array([a, b, c, d], dtype = 'complex_')
    return coeff

# a*F(n-1) - b*F(n) + c* F(n+1) = d
@njit(fastmath=True, cache=True)
def SolveUsadel(delta, w, G, sconductor, ferro):
    N = int(sconductor.N + ferro.N)
    p = np.zeros(N+1, dtype='complex_')
    q = np.zeros(N+1, dtype='complex_')
    Fi = np.zeros(N, dtype='complex_')
    for i in range(N):
        a, b, c, d = Usadel(i, delta[i], w, G, sconductor, ferro)
        p[i+1] = c/(b - a*p[i])
        q[i+1] = (a*q[i] + d)/(b - a*p[i])
    
    Fi[N-1] = q[N]
    for i in range(N-2, -1, -1):
        Fi[i] = p[i+1]* Fi[i+1]+q[i+1]
    return Fi

#Вычисление функции Грина
@njit(fastmath=True, cache=True)
def Gcalc(Fi, Fi1, w, sconductor, ferro):
    N_S = int(sconductor.N)
    N = int(sconductor.N + ferro.N)
    G = np.zeros(N, dtype='complex_')
    for i in range(N_S):
        wm = complex(w, sconductor.H)
        G[i] = wm/np.sqrt(wm*wm + Fi[i]*Fi1[i].conjugate())
    for i in range(N_S, N):
        wm = complex(w, ferro.H)
        G[i] = wm/np.sqrt(wm*wm + Fi[i]*Fi1[i].conjugate())
    return G

#Вычисление начального приближения парного потенциала
@njit(fastmath=True, cache=True)
def selfcons0(T, Tc):
    Del1 = 1.76
    dDel = 1
    w_max = int(30/T)
    while abs(dDel)>eps:
        S1 = 0
        S2 = -math.log(Tc/T)/T/pi/2
        for wi in range(w_max):
            w = pi*T*(2*wi + 1)
            S1 += Del1/np.sqrt(w**2 + Del1**2)
            S2 += 1/w
        dDel = Del1 - S1/S2
        Del1 = Del1- dDel
    return Del1

#Нахождение из системы уравнений параметра "дельта" - парного потенциала
@njit(fastmath=True, cache=True)
def selfcons(Del0, T, sconductor, ferro):
    epsG = 1e-6
    alpha=0.7

    N_S = sconductor.N
    N_F = ferro.N
    N = int(N_S + N_F)
    Tc = sconductor.Tc
    
    w_max = int(30/T)
    Del = np.zeros(N, dtype = 'complex_')
    G = np.ones(N, dtype = 'complex_')
    Fi1 = np.zeros(N, dtype = 'complex_')
    Fi2 = np.zeros(N, dtype = 'complex_')
    for i in range(N_S):
        Del[i] = complex(Del0, 0)

    tn = 50000
    dDelmax = 1
    for k in range(tn):
        S1 = np.zeros(N, dtype = 'complex_')
        S2 = np.ones(N, dtype = 'complex_')*np.log(T/Tc)/pi/T

        for wi in range(w_max):
            w = pi*T*(2*wi+1)
            itera = 0
            dGmax = 1

            for m in range(tn):
                Fi1_old = np.copy(Fi1)
                Fi1 = SolveUsadel(Del, w, G, sconductor, ferro)
                Fi1 = 0.1*Fi1 + 0.9*Fi1_old
                G = -G.conjugate()
                
                Fi2_old = np.copy(Fi2)
                Fi2 = SolveUsadel(Del, -w, G, sconductor, ferro)
                Fi2 = 0.1*Fi2 + 0.9*Fi2_old
                G = -G.conjugate()

                G1= Gcalc(Fi1, Fi2, w, sconductor, ferro)
                dGmax = 0
                for i in range(N):
                    if dGmax < (abs(G1[i] - G[i])):
                        dGmax = abs(G1[i] - G[i])
                G = G1
                if dGmax <= epsG:
                    break

            for i in range(N_S):
                S1[i] += Fi1[i]*G[i]/w + Fi2[i]*G[i].conjugate()/w
            S2 += 2/w
  
        Delbuf = np.zeros(N, dtype = 'complex_')
        dDelmax = 0
        for i in range(N):
            Delbuf[i] = Del[i]
            Del[i] = (S1[i]/S2[i] + Delbuf[i]*(alpha-1))/alpha
            if dDelmax < abs(Del[i]-Delbuf[i]):
                dDelmax = abs(Del[i]-Delbuf[i])
        if dDelmax <=eps:
            return Del
        
    return Del

#Нахождение критической температуры из зависимости "дельта" от температуры
def f(sconductor, ferro, T = 0.98):
    Tc = sconductor.Tc
    T_res = np.zeros(6)  
    
    dT = 0.005

    dDel = np.zeros(3)
    ddDel = 0
    T = T+dT
    tn = 5000
    for i in range(tn):
        Del0 = selfcons0(T, Tc)
        Del = selfcons(Del0, T, sconductor, ferro)
        dDel[0] = dDel[1]
        dDel[1] = dDel[2]
        dDel[2] = Del[1].real
        ddDel = dDel[2] - 2*dDel[1] + dDel[0]
        T -= dT
        if T <= 0.05 or abs(ddDel) >= 0.07:
            return T + dT
    T_res = T + dT
    return T_res

#Функция для получения критической температуры в зависимости от размера сверхпроводника
def calc(sconductor, ferro, num_points = 5):
    dT = 0.005
    L = np.linspace(sconductor.L, 0.5, num_points)
    T_res = np.zeros(num_points)
    T = 0.98
    
    for i in range(num_points):
        sconductor.L = L[i]
        T_res[i] = f(sconductor, ferro, T)
        # T = T_res[i] +2*dT
    plt.scatter(L, T_res)
    plt.show()
    return T_res

#Функция для считывания из файла параметров материалов 
def f_read(path):
    empty = (0, 0, 0, 0, 0, 0, 0, 0)
    sconductor_par = []
    ferro_par = []
    with open(path) as f:
        for line in f:
            line = line.split()
            sconductor_par.append(float(line[1]))
            ferro_par.append(float(line[2]))
    sconductor = Material(sconductor_par)
    ferro = Material(ferro_par)
    return sconductor, ferro

if __name__ == "__main__":
    path = r'D:\python\config.txt'
    superconductor, ferromagnet = f_read(path)
    T = f(superconductor, ferromagnet)
    print(T)
    # T = calc(superconductor, ferromagnet)
    # print(T)
    