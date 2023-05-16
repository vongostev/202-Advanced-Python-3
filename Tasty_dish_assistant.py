import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from skfuzzy.control import visualization


if __name__ == '__main__':

    """
    Параметры, опредиляющие точность разбиения
    """
    flame_accur = 20 + 1
    sweet_accur = 32 + 1
    ingrd_accur = 30 + 1

    """
    Функции принадлежности
    """
    flame = ctrl.Antecedent(np.linspace(0, 2.0, flame_accur), 'flame')
    sweet = ctrl.Antecedent(np.linspace(0, 1.6, sweet_accur), 'sweetness')
    ingrd = ctrl.Consequent(np.linspace(0, 60, ingrd_accur), 'ingredient')

    flame['медленный'] = fuzz.trapmf(flame.universe, [0, 0, 0.45, 0.8])
    flame['средний'] = fuzz.trapmf(flame.universe, [0.5, 0.8, 1.3, 1.7])
    flame['сильный'] = fuzz.trapmf(flame.universe, [1.25, 1.6, 2.0, 2.0])

    sweet['несладкий'] = fuzz.trapmf(sweet.universe, [0, 0, 0.1, 0.2])
    sweet['немного сладкий'] = fuzz.trimf(sweet.universe, [0.1, 0.4, 0.7])
    sweet['средней сладости'] = fuzz.trapmf(sweet.universe, [0.5, 0.7, 0.9, 1.4])
    sweet['сильно сладкий'] = fuzz.trapmf(sweet.universe, [1.0, 1.3, 1.6, 1.6])

    ingrd['пару щепоток'] = fuzz.trimf(ingrd.universe, [-2, 6, 10])
    ingrd['пару чайных ложек'] = fuzz.trimf(ingrd.universe, [4, 20, 40])
    ingrd['пару столовых ложек'] = fuzz.trimf(ingrd.universe, [30, 42, 60])

    """
    Построение функций принадлежности
    """
    """flame"""
    fig, ax = visualization.FuzzyVariableVisualizer(flame).view()
    fig.set_size_inches(8, 5)
    fig.set_dpi(200)
    # fig.patch.set_facecolor('xkcd:mint green')

    for line in plt.gca().lines:
        line.set_linewidth(6.)
        # line.set_color('tab:orange')

    # ax.legend(loc="lower right", fontsize=16)
    ax.get_legend().remove()
    plt.text(0.03, 1.06, 'медленный', fontsize=18, style='italic')
    plt.text(0.88, 1.06, 'средний', fontsize=18, style='italic')
    plt.text(1.63, 1.06, 'сильный', fontsize=18, style='italic')
    # ax.set_xticks(np.linspace(10, 30, 11))
    ax.set_yticks(np.linspace(0, 1, 6))
    # ax.set_xticklabels(np.linspace(10, 30, 11), fontsize=22)
    ax.set_facecolor('#e9e9e9')
    ax.tick_params(axis="x", labelsize=14)
    ax.tick_params(axis="y", labelsize=14)
    ax.set_ylim(top=1.2)
    ax.set_title("Огонь", fontsize=20, weight='bold')
    ax.set_xlabel("Мощность плиты, кВт", fontsize=20)
    ax.set_ylabel("$\mu$", fontsize=24)

    """sweetness"""
    fig, ax = visualization.FuzzyVariableVisualizer(sweet).view()
    fig.set_size_inches(8, 5)
    fig.set_dpi(200)
    # fig.patch.set_facecolor('xkcd:mint green')

    for line in plt.gca().lines:
        line.set_linewidth(6.)
        # line.set_color('tab:orange')

    # ax.legend(loc="lower right", fontsize=16)
    ax.get_legend().remove()
    plt.text(-0.16, 1.1, 'несладкий', fontsize=18, style='italic')
    plt.text(0.29, 1.06, 'немного \nсладкий', fontsize=18, style='italic')
    plt.text(0.68, 1.06, 'средней \nсладости', fontsize=18, style='italic')
    plt.text(1.31, 1.06, 'сильно \nсладкий', fontsize=18, style='italic')
    # ax.set_xticks(np.linspace(10, 30, 11))
    ax.set_yticks(np.linspace(0, 1, 6))
    # ax.set_xticklabels(np.linspace(10, 30, 11), fontsize=22)
    ax.set_facecolor('#e9e9e9')
    ax.tick_params(axis="x", labelsize=14)
    ax.tick_params(axis="y", labelsize=14)
    ax.set_ylim(top=1.3)
    ax.set_title("Сладость", fontsize=20, weight='bold')
    ax.set_xlabel("Концентрация сахара, г/см\u00b3", fontsize=20)
    ax.set_ylabel("$\mu$", fontsize=24)
    
    """ingredient"""
    fig, ax = visualization.FuzzyVariableVisualizer(ingrd).view()
    fig.set_size_inches(8, 5)
    fig.set_dpi(200)
    # fig.patch.set_facecolor('xkcd:mint green')

    for line in plt.gca().lines:
        line.set_linewidth(6.)
        # line.set_color('tab:orange')

    # ax.legend(loc="lower right", fontsize=16)
    ax.get_legend().remove()
    plt.text(1, 1.06, 'пару щепоток', fontsize=18, style='italic')
    plt.text(10.5, 0.78, 'пару чайных ложек', fontsize=18, style='italic')
    plt.text(31, 1.06, 'пару столовых ложек', fontsize=18, style='italic')
    # ax.set_xticks(np.linspace(10, 30, 11))
    ax.set_yticks(np.linspace(0, 1, 6))
    # ax.set_xticklabels(np.linspace(10, 30, 11), fontsize=22)
    ax.set_facecolor('#e9e9e9')
    ax.tick_params(axis="x", labelsize=14)
    ax.tick_params(axis="y", labelsize=14)
    ax.set_ylim(top=1.2)
    ax.set_title("Добавка", fontsize=20, weight='bold')
    ax.set_xlabel("Масса, г", fontsize=20)
    ax.set_ylabel("$\mu$", fontsize=24)

    """
    Набор правил
    """
    rule1 = ctrl.Rule((flame['медленный'] & sweet['немного сладкий']) |
                      ((flame['медленный'] | flame['сильный']) & sweet['несладкий']) |
                      (flame['сильный'] & sweet['сильно сладкий']),
                      consequent = ingrd['пару щепоток'])
    rule2 = ctrl.Rule((flame['средний'] | (sweet['средней сладости'] | sweet['немного сладкий'])) |
                      (flame['сильный'] & sweet['средней сладости']) |
                      (flame['медленный'] & sweet['сильно сладкий']),
                      consequent = ingrd['пару чайных ложек'])
    rule3 = ctrl.Rule((flame['медленный'] & sweet['сильно сладкий']) |
                      (flame['средний'] & sweet['средней сладости']),
                      consequent = ingrd['пару столовых ложек'])

    dosage_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
    dosage = ctrl.ControlSystemSimulation(dosage_ctrl)

    """
    Обработка фаззифицированной информации + дефазз
    """
    x, y = np.meshgrid(np.linspace(flame.universe[0],
                                   flame.universe[-1],
                                   flame_accur),
                       np.linspace(sweet.universe[0],
                                   sweet.universe[-1],
                                   sweet_accur))
    z = np.zeros_like(x)
    for i in range(sweet_accur):
        for j in range(flame_accur):
            dosage.input['flame'] = x[i, j]
            dosage.input['sweetness'] = y[i, j]
            dosage.compute()
            z[i, j] = dosage.output['ingredient']

    """
    Построение конечного графика
    """
    fig = plt.figure(figsize=(16, 8), dpi=200)
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap='viridis',
                           linewidth=0.4, antialiased=True, alpha=.95)
    ax.view_init(30, 250)
    ax.set_xlabel("Мощность плиты, кВт", fontsize=11)
    ax.set_ylabel("Концентрация сахара, г/см\u00b3", fontsize=11)
    ax.set_zlabel("Масса ингредиента, г", fontsize=11)




