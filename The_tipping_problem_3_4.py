import numpy as np
import matplotlib.pyplot as plt
import math
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from skfuzzy.control import visualization
# tip['high'].mf
# plt.hist(P_EH, bins=10)


"""Функции принадлежности"""
qual_accur = 11
serv_accur = 11
tip_order = 1
tip_accur = 25*tip_order+1
quality = ctrl.Antecedent(np.linspace(0, 10, qual_accur), 'quality')
service = ctrl.Antecedent(np.linspace(0, 10, serv_accur), 'service')
tip = ctrl.Consequent(np.linspace(0, 25, tip_accur), 'tip')

quality['unsavory'] = fuzz.trapmf(quality.universe, [0, 0, 2, 6])
quality['tasty'] = fuzz.trapmf(quality.universe, [2, 9, 10, 10])

service['bad'] = fuzz.trapmf(service.universe, [0, 0, 2, 6])
service['good'] = fuzz.trimf(service.universe, [2, 5, 9])
service['excellent'] = fuzz.trapmf(service.universe, [3, 9, 10, 10])

tip['low'] = fuzz.trimf(tip.universe, [0, 3, 5])
tip['medium'] = fuzz.trimf(tip.universe, [5, 13, 20])
tip['high'] = fuzz.trimf(tip.universe, [20, 23, 25])


"""Функции распределения"""
P1 = fuzz.gaussmf(quality.universe, 5, 2)
P1 /= P1.sum()
P2 = fuzz.gaussmf(service.universe, 7, 3)
P2 /= P2.sum()


"""Построение функций"""
fig, ax = visualization.FuzzyVariableVisualizer(quality).view()
fig.set_size_inches(9, 6)
fig.set_dpi(80)
for line in plt.gca().lines:
    line.set_linewidth(5.)
ax.set_title("Качество еды")
ax.set_xlabel("Quality", fontsize=16)
ax.set_ylabel("$p(z)$", fontsize=16)
service.view()
tip.view()

fig, ax = plt.subplots(figsize=(10, 8))
ax.bar(quality.universe, P1, width=10./(qual_accur-1), edgecolor="white", linewidth=0.7, zorder=2)
ax.set_title("Плотность распределения Quality")
ax.grid(zorder=1)
fig, ax = plt.subplots(figsize=(10, 8))
ax.bar(service.universe, P2, width=10./(serv_accur-1), edgecolor="white", linewidth=0.7, zorder=2)
ax.set_title("Плотность распределения Service")
ax.grid(zorder=1)


"""Правила ..."""
rulP1 = ctrl.Rule(quality['unsavory'] | service['bad'], tip['low'])
rulP2 = ctrl.Rule(service['good'], tip['medium'])
rule3 = ctrl.Rule(quality['tasty'] | service['excellent'], tip['high'])
tipping_ctrl = ctrl.ControlSystem([rulP1, rulP2, rule3])
tipping = ctrl.ControlSystemSimulation(tipping_ctrl)


"""Обработка фаззифицированной информации + дефазз"""
x, y = np.meshgrid(np.linspace(quality.universe[0], quality.universe[-1], qual_accur),
                   np.linspace(service.universe[0], service.universe[-1], serv_accur))
z = np.zeros_like(x)
P_EH = np.zeros([qual_accur, serv_accur])
for i in range(serv_accur):
    for j in range(qual_accur):
        tipping.input['quality'] = x[i, j]
        tipping.input['service'] = y[i, j]
        tipping.compute()
        # zk = tipping.output['tip']
        zk = round(tipping.output['tip'], int(math.log(tip_order)))
        z[i, j] = zk
        P_EH[i, j] = zk


"""Построение конечного графика"""
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap='viridis',
                       linewidth=0.4, antialiased=True)
ax.view_init(30, 210, 'z')
ax.set_xlabel("Quality of food")
ax.set_ylabel("Service")
ax.set_zlabel("Tip, %")


"""Плотность вероятность совместного распределения P(z), где z = f(x,y)"""
P_Z = np.zeros(tip_accur)
for k in range(tip_accur):
    crds = np.where(P_EH == k/tip_order)
    for i in range(len(crds[0])):
        P_Z[k] += P1[crds[0][i]]*P2[crds[1][i]]


"""График совместного распределения"""
fig, ax = plt.subplots(figsize=(10, 8))
ax.bar(tip.universe, P_Z, width=25./(tip_accur-1), edgecolor="white", linewidth=0.4, zorder=2)
ax.grid(zorder=1)
ax.set_title("Оценка z", fontsize=16)
ax.set_xlabel("$Tip,$ %", fontsize=16)
ax.set_ylabel("$p(z)$", fontsize=16)
# ax.set_ylim([0, 1])


