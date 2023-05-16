import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from skfuzzy.control import visualization
# tip['high'].mf
# plt.hist(P_EH, bins=10)


"""Функция принадлежности"""
qual_accur = 51
qual_U = np.linspace(0, 50, qual_accur)
quality = ctrl.Antecedent(qual_U, 'example')

quality['A'] = fuzz.trapmf(quality.universe, [-10, 5, 15, 30])
quality['B'] = fuzz.trapmf(quality.universe, [10, 25, 35, 40])
quality['C'] = fuzz.trapmf(quality.universe, [20, 30, 50, 50])


"""Построение функций"""
fig, ax = visualization.FuzzyVariableVisualizer(quality).view()
fig.set_size_inches(8, 5)
fig.set_dpi(200)
# fig.patch.set_facecolor('xkcd:mint green')

for line in plt.gca().lines:
    line.set_linewidth(6.)
    # line.set_color('tab:orange')

# ax.legend(loc="lower right", fontsize=16)
ax.get_legend().remove()
plt.text(9, 1.06, 'A\u2091', fontsize=18, style='italic')
plt.text(26, 1.06, 'B\u2091', fontsize=18, style='italic')
plt.text(42, 1.06, 'C\u2091', fontsize=18, style='italic')

qual_0 = np.zeros_like(qual_U)
qual_activation_A = np.fmin(quality['A'].mf, 0.2)
qual_activation_B = np.fmin(quality['B'].mf, 0.4)
qual_activation_C = np.fmin(quality['C'].mf, 0.7)
if (False):
    ax.fill_between(qual_U, qual_0, qual_activation_A, facecolor='Blue', alpha=1)
    ax.fill_between(qual_U, qual_0, qual_activation_B, facecolor='Orange', alpha=1)
    ax.fill_between(qual_U, qual_0, qual_activation_C, facecolor='Green', alpha=1)

if (True):
    aggregated = np.fmax(qual_activation_A,
                         np.fmax(qual_activation_B, qual_activation_C))
    ax.fill_between(qual_U, qual_0, aggregated, facecolor='#4169E1', alpha=1, zorder=10)
    ax.plot([30, 30], [0, 0.69], 'k', linewidth=3, alpha=1, zorder=11)
    plt.text(29.5, -0.07, 'C', fontsize=18, style='italic', zorder=12)
    plt.text(30.8, -0.09, 'G', fontsize=10, style='italic', zorder=12)
ax.set_xticks(np.linspace(10, 30, 0))
ax.set_yticks(np.linspace(0, 1, 6))
# ax.set_xticklabels(np.linspace(10, 30, 11), fontsize=22)
ax.set_facecolor('#e9e9e9')
ax.tick_params(axis="x", labelsize=14)
ax.tick_params(axis="y", labelsize=14)
ax.set_ylim(top=1.2)
ax.set_xlabel("T\u2091", fontsize=22)
ax.set_ylabel("$\mu$", fontsize=24)
