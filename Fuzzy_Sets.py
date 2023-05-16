import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np


# Создание нечеткого множества
def FS_create(M: np.array, U=None, norm=True, precision=False):
    # U, M - np.array
    if (U is None):
        U = np.arange(1, M.size+1)
    if (M.size < U.size):
        raise Exception("Функция принадлежности не задана на всем U")
    if (M.size > U.size):
        M = M[:U.size]
    if norm:
        M = M/M.max()
    F = dict()
    if precision is False:
        for i in range(0, U.size):
            F[U[i]] = M[i]
        return F
    elif type(precision) == int:
        for i in range(0, U.size):
            F[round(U[i], precision)] = M[i]
        return F


# Задание численного трапециедального распределения
def MS_trapezoid(U: np.array, a=None, b=None, c=None, d=None):
    # scipy.stats.trapezoid
    M = np.empty(U.size)
    if (a is None) or (b is None):
        if (c is None) or (d is None):
            M = np.ones(U.size)
            return M
        else:
            for ind in range(0, U.size):
                if (U[ind] <= c):
                    M[ind] = 1
                elif (U[ind] >= d):
                    M[ind] = 0
                elif (c != d):
                    M[ind] = (d-U[ind])/(d-c)
            return M
    else:
        if (c is None) or (d is None):
            for ind in range(0, U.size):
                if (U[ind] <= a):
                    M[ind] = 0
                elif (U[ind] >= b):
                    M[ind] = 1
                elif (a != b):
                    M[ind] = (U[ind]-a)/(b-a)
            return M
        else:
            for ind in range(0, U.size):
                if (U[ind] <= a):
                    M[ind] = 0
                elif (U[ind] < b):
                    M[ind] = (U[ind]-a)/(b-a)
                elif (U[ind] >= b) and (U[ind] <= c):
                    M[ind] = 1
                elif (U[ind] < d):
                    M[ind] = (d-U[ind])/(d-c)
                else:
                    M[ind] = 0
            return M


# Распределение Гаусса
def gaussian(x, alpha, r):
    return np.exp(-alpha*np.power((x - r), 2.))


# Построение нечеткого множества
def FS_plot(FS: list, labels=None, title=None, save=None):
    fig, ax = plt.subplots(figsize=(10, 7), dpi=70)
    ax.grid()
    for idx, elm in enumerate(FS):
        x, y = zip(*elm.items())
        if (labels is None):
            lab = ' '
        else:
            lab = labels[idx]
        y_max = float(max(y))
        plt.ylim([0, max(1, y_max)*1.4])
        line, = ax.plot(x, y, label=lab, linewidth=3)
    if not (labels is None):
        ax.legend(loc='upper right')
    if not (title is None):
        ax.set_title(title)
    if not (save is None):
        fig.savefig(save+'.png', format="png", dpi=100)


# Complement of F
def FS_compl(F_1: dict, norm=False):
    F = F_1.copy()
    mx = max(F.values())
    for key in F.keys():
        F[key] = mx - F[key]
    if norm:
        for key in F.keys():
            F[key] = F[key]/mx
    return F


# Intersection of F_1 & F_2
def FS_intersc(F_1: dict, F_2: dict):
    if sorted(F_1.keys()) != sorted(F_2.keys()):
        raise Exception("Несовпадение универсальных множеств")
    F = F_1.copy()
    for key in F.keys():
        F[key] = min(F_1[key], F_2[key])
    return F


# Union of F_1 & F_2
def FS_union(F_1: dict, F_2: dict):
    if sorted(F_1.keys()) != sorted(F_2.keys()):
        raise Exception("Несовпадение универсальных множеств")
    F = F_1.copy()
    for key in F.keys():
        F[key] = max(F_1[key], F_2[key])
    return F


# Union of Fuzzy Sets
def FS_union_list(FS: list):
    if len(FS) == 0:
        raise Exception("Множества не указаны")
    Keys = sorted(FS[0].keys())
    for ind in range(1, len(FS)):
        if sorted(FS[ind].keys()) != Keys:
            raise Exception("Несовпадение универсальных множеств")
    FU = FS[0].copy()
    for key in FU.keys():
        max_val = FS[0][key]
        for ind in range(1, len(FS)):
            if max_val <= FS[ind][key]:
                max_val = FS[ind][key]
        FU[key] = max_val
    return FU


# Альфа-срез
def FS_alphacut(F_1: dict, alpha: float):
    max_val = max(F_1.values())
    if (alpha <= 0) or (alpha > max_val):
        raise Exception("Альфа выходит за диапазон")
    F = F_1.copy()
    for key in list(F.keys()):
        if (F[key] < alpha):
            F.pop(key)
    return F


# Заполнение нижней части
def FS_mark_fill(F_1: dict, mark: float):
    if (mark < 0):
        raise Exception("Mark < 0")
    elif (mark == 0):
        F = F_1.copy()
        for key in F.keys():
            F[key] = 0
        return F
    else:
        F = F_1.copy()
        for key in F.keys():
            if (F[key] > mark):
                F[key] = mark
        return F


# Центр масс (дефаззификация в число)
def FS_centroid(F: dict, U=None):
    # U - числовое множество
    if len(F) == 0:
        raise Exception("F - пустое множество")
    S1 = 0.
    S2 = 0.
    if U is None:
        for key in F.keys():
            S1 += float(key)*F[key]
            S2 += F[key]
        return S1/S2
    else:
        if len(F) > U.size():
            raise Exception("Функция принадлежности не задана на всем U")
        for ind, key in enumerate(F.keys()):
            S1 += U[ind]*F[key]
            S2 += F[key]
        return S1/S2


if __name__ == '__main__':

    '''
Заданные распределения
    '''
    U = np.arange(0, 10.1, 0.1, dtype=float)  # U - универсум
    Ans_1 = FS_create(MS_trapezoid(U, None, None, 1.5, 3), U, False, 1)
    Ans_2 = FS_create(MS_trapezoid(U, 2, 4, 4, 6), U, False, 1)
    Ans_3 = FS_create(MS_trapezoid(U, 5.2, 6.8, 6.8, 8), U, False, 1)
    Ans_4 = FS_create(MS_trapezoid(U, 7, 8, 8, 9), U, False, 1)
    Ans_5 = FS_create(MS_trapezoid(U, 8, 8.5, None, None), U, False, 1)
    ANS = [Ans_1, Ans_2, Ans_3, Ans_4, Ans_5]
    ANS_ls = ["Никакой", "Средний", "Хороший", "Почти полный", "Полный"]
    FS_plot(ANS, labels=ANS_ls, title='Ответ на экзамене')

    Wrk_1 = FS_create(gaussian(U, 0.4, 0.3), U, False, 1)
    Wrk_2 = FS_create(gaussian(U, 0.5, 5), U, False, 1)
    Wrk_3 = FS_create(gaussian(U, 0.15, 9.5), U, False, 1)
    WRK = [Wrk_1, Wrk_2, Wrk_3]
    WRK_ls = ["Плохая", "Средняя", "Хорошая"]
    FS_plot(WRK, labels=WRK_ls, title='Работа в семестре')

    R = np.arange(2, 5.1, 0.1)
    Rsl_2 = FS_create(MS_trapezoid(R, None, None, 2.5, 2.7), R, False, 1)
    Rsl_3 = FS_create(MS_trapezoid(R, 2.5, 2.8, 3.4, 3.7), R, False, 1)
    Rsl_4 = FS_create(MS_trapezoid(R, 3.5, 3.8, 4.2, 4.5), R, False, 1)
    Rsl_5 = FS_create(MS_trapezoid(R, 4.6, 4.6, None, None), R, False, 1)
    RSL = [Rsl_2, Rsl_3, Rsl_4, Rsl_5]
    RSL_ls = ["Неуд", "Уд", "Хор", "Отл"]
    FS_plot(RSL, labels=RSL_ls, title='Оценка')

    '''
Правила оценивания
    '''
    ans = input("В диапазоне [0, 10] оцените ответ студента на билет: ")
    wrk = input("В диапазоне [0, 10] оцените работу студента в семестре: ")
    ans = round(float(ans), 1)
    wrk = round(float(wrk), 1)
    Otl = max(Ans_5[ans],
              min(Ans_4[ans],
                  Wrk_3[wrk]))
    Khor = max(min(Ans_4[ans],
                   max(Wrk_1[wrk],
                       Wrk_2[wrk])),
               Ans_3[ans],
               min(Ans_2[ans],
                   Wrk_3[wrk]))
    Udovl = max(min(Ans_2[ans],
                    max(Wrk_1[wrk],
                        Wrk_2[wrk])),
                min(Ans_1[ans],
                    Wrk_3[wrk]))
    Neud = min(Ans_1[ans],
               max(Wrk_1[wrk],
                   Wrk_2[wrk]))

    Final = FS_union_list([FS_mark_fill(Rsl_2, Neud),
                           FS_mark_fill(Rsl_3, Udovl),
                           FS_mark_fill(Rsl_4, Khor),
                           FS_mark_fill(Rsl_5, Otl)])
    FS_plot([Final], labels=['Комбинированный срез'], title='Оценка')
    judgment = FS_centroid(Final)
    print("Объективная оценка:", '%.2f' % judgment)

    '''
Итоговый график
    '''
    if False:
        Z = np.empty([101, 101])
        for i in range(0, 101, 1):
            ans = 0.1*i
            ans = round(ans, 1)
            for j in range(0, 101, 1):
                wrk = 0.1*j
                wrk = round(wrk, 1)

                Otl = max(Ans_5[ans],
                          min(Ans_4[ans],
                              Wrk_3[wrk]))
                Khor = max(min(Ans_4[ans],
                               max(Wrk_1[wrk],
                                   Wrk_2[wrk])),
                           Ans_3[ans],
                           min(Ans_2[ans],
                               Wrk_3[wrk]))
                Udovl = max(min(Ans_2[ans],
                                max(Wrk_1[wrk],
                                    Wrk_2[wrk])),
                            min(Ans_1[ans],
                                Wrk_3[wrk]))
                Neud = min(Ans_1[ans],
                           max(Wrk_1[wrk],
                               Wrk_2[wrk]))

                Final = FS_union_list([FS_mark_fill(Rsl_2, Neud),
                                       FS_mark_fill(Rsl_3, Udovl),
                                       FS_mark_fill(Rsl_4, Khor),
                                       FS_mark_fill(Rsl_5, Otl)])
                Z[i][j] = FS_centroid(Final)

        fig, ax = plt.subplots(subplot_kw={"projection": "3d"},
                               figsize=(10, 7),
                               dpi=100)
        X = np.arange(0, 10.1, 0.1)
        Y = np.arange(0, 10.1, 0.1)
        X, Y = np.meshgrid(X, Y)
        surf = ax.plot_surface(X, Y, Z, cmap=cm.Spectral,
                               linewidth=0, antialiased=False)
        fig.colorbar(surf, shrink=0.5, aspect=5)
        ax.set_zlim(2, 5)
        ax.zaxis.set_major_locator(LinearLocator(7))
        ax.zaxis.set_major_formatter('{x:.01f}')
        ax.invert_xaxis()
        ax.set_xlabel("Работа в семестре")
        ax.set_ylabel("Ответ на экзамене")
        ax.set_zlabel("Оценка")
        # fig.savefig('Resume.png', format="png", dpi=150)




