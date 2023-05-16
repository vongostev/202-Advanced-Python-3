#######################################################
#######################################################
# Импорт зависимостей:
import time
import sympy
import einsteinpy.symbolic
#######################################################
#######################################################
class Output_Object ():
    output_file_path: str

    # Процедура инициализации файла вывода:
    def __init__(self, output_file_path_0):
        self.output_file_path = output_file_path_0
        with open(self.output_file_path, mode='w', encoding='utf-8') as output_file:
            output_file.write(
                '\\documentclass[a4paper, 10pt]{article}\n')
            output_file.write('\\usepackage[T2A]{fontenc}\n')
            output_file.write('\\usepackage[utf8]{inputenc}\n')
            output_file.write('\\usepackage[russian,english]{babel}\n')
            output_file.write('\\usepackage{amsfonts}\n')
            output_file.write('\\usepackage{amssymb}\n')
            output_file.write('\\usepackage{amsmath}\n')
            output_file.write('\\begin{document}\n')

    # Процедура завершения файла вывода:
    def end(self):
        with open(self.output_file_path, mode='a', encoding='utf-8') as output_file:
            output_file.write('\end{document}\n')

    # Процедура записи в файл вывода:
    def write(self, s: str):
        with open(self.output_file_path, mode='a', encoding='utf-8') as output_file:
            output_file.write(s)

    # Нижеследующий алгоритм внесён в методы из-за своего большого объёма
    # Вывод тензора кривизны Римана (4-ковариантного):
    def write_riemann(self, local_riemann_curvature, local_coordinates):
        local_list_1 = [[index_I, index_II, index_III, index_IV] for index_I in range(
            4) for index_II in range(4) for index_III in range(4) for index_IV in range(4)]
        local_list_2 = []
        for index_I in local_list_1:
            key_I = True
            for index_II in local_list_2:
                if (index_I == index_II) or (index_I == [index_II[1], index_II[0], index_II[2], index_II[3]]) or (index_I == [index_II[0], index_II[1], index_II[3], index_II[2]]) or (index_I == [index_II[1], index_II[0], index_II[3], index_II[2]]) or (index_I == [index_II[2], index_II[3], index_II[0], index_II[1]]) or (index_I == [index_II[3], index_II[2], index_II[0], index_II[1]]) or (index_I == [index_II[2], index_II[3], index_II[1], index_II[0]]) or (index_I == [index_II[3], index_II[2], index_II[1], index_II[0]]):
                    key_I = False
            if key_I:
                local_list_2.append(index_I)
        local_list_1 = []
        for index_II in local_list_2:
            key_I = True
            key_II = True
            for index_I in local_list_1:
                if (index_I == [index_II[0], index_II[2], index_II[3], index_II[1]]) or (index_I == [index_II[2], index_II[0], index_II[3], index_II[1]]) or (index_I == [index_II[0], index_II[2], index_II[1], index_II[3]]) or (index_I == [index_II[2], index_II[0], index_II[1], index_II[3]]) or (index_I == [index_II[3], index_II[1], index_II[0], index_II[2]]) or (index_I == [index_II[1], index_II[3], index_II[0], index_II[2]]) or (index_I == [index_II[3], index_II[1], index_II[2], index_II[0]]) or (index_I == [index_II[1], index_II[3], index_II[2], index_II[0]]):
                    key_I = False
                if (index_I == [index_II[0], index_II[3], index_II[1], index_II[2]]) or (index_I == [index_II[3], index_II[0], index_II[1], index_II[2]]) or (index_I == [index_II[0], index_II[3], index_II[2], index_II[1]]) or (index_I == [index_II[3], index_II[0], index_II[2], index_II[1]]) or (index_I == [index_II[1], index_II[2], index_II[0], index_II[3]]) or (index_I == [index_II[2], index_II[1], index_II[0], index_II[3]]) or (index_I == [index_II[1], index_II[2], index_II[3], index_II[0]]) or (index_I == [index_II[2], index_II[1], index_II[3], index_II[0]]):
                    key_II = False
            if key_I or key_II:
                local_list_1.append(index_II)
        local_list_2 = []
        for index_I in local_list_1:
            if (index_I[0] != index_I[1]) and (index_I[2] != index_I[3]):
                local_list_2.append(index_I)
        self.write("\\subsection{Тензор кривизны Римана (4-ковариантный):}\n\nС учётом симметрий:\n$$R_{abcd}=-R_{bacd}=-R_{abdc}=R_{cdab}$$\nи первого тождества Бианки:\n$$R_{abcd}+R_{acdb}+R_{adbc}=0$$\nего независимые компоненты имеют вид:\n\n")
        for index_I in local_list_2:
            self.write('$$' +
                       'R_{'+sympy.latex(local_coordinates[index_I[0]])+' '+sympy.latex(local_coordinates[index_I[1]])+' '+sympy.latex(local_coordinates[index_I[2]])+' '+sympy.latex(local_coordinates[index_I[3]]) +
                       '} = '+sympy.latex(local_riemann_curvature[index_I[0], index_I[1], index_I[2], index_I[3]]) +
                       '$$\n')
#######################################################
#######################################################
if __name__ == '__main__':
#######################################################
    # Запуск счётчика времени:
    time_counter = time.perf_counter()
#######################################################

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    # ОСНОВНЫЕ ПАРАМЕТРЫ:

    # Расположение файла вывода:
    main_parameter_output_file_name = '.\Выкладки.tex'

    # Инициализация основных символов и функций:
    # Координаты:
    coordinates = sympy.symbols('t r theta phi')
    # Константы:
    consts = sympy.symbols('r_0 r_1')
    # функции
    function_A = sympy.Function('A')(coordinates[0], coordinates[1])
    function_B = sympy.Function('B')(coordinates[0], coordinates[1])

    # Инициализация (пре)метрики (ковариантной):
    pre_metric = [[0 for i in range(4)] for k in range(4)]
    pre_metric[0][0] = - 1 + consts[0]/coordinates[1]
    pre_metric[1][1] = 1/(1 - consts[0]/coordinates[1])
    pre_metric[2][2] = (coordinates[1]**2)
    pre_metric[3][3] = (coordinates[1]**2)*((sympy.sin(coordinates[2]))**2)

    # Ключи расчёта:
    key_calc_metric_contravariant = True
    key_calc_christoffel_second = True
    key_calc_riemann_curvature = True
    key_calc_ricci_curvature = True
    key_calc_ricci_scalar = True
    key_calc_einstein_tensor = True
    key_calc_ricci_curvature_square = True
    key_calc_riemann_curvature_square = True

    # Ключи вывода:
    key_write_metric_contravariant = True
    key_write_christoffel_second = True
    key_write_riemann_curvature = True
    key_write_ricci_curvature = True
    key_write_ricci_scalar = True
    key_write_einstein_tensor = True
    key_write_ricci_curvature_square = True
    key_write_riemann_curvature_square = True

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#######################################################
    # Инициализация файла вывода:
    output_object = Output_Object(main_parameter_output_file_name)
#######################################################
    # Инициализация дополнительных символов и функций:
    # Вектор координат:
    coordinates_vector = sympy.Array(coordinates)
    # Матрица ковариантного метрического тензора:
    metric_covariant = einsteinpy.symbolic.MetricTensor(
        pre_metric, coordinates)
#######################################################
    # Вывод начальных данных:
    output_object.write("\\section{Начальные данные:}\n")
    output_object.write("\\subsection{Ковариантная метрика:}\n")
    output_object.write('$$'+sympy.latex(metric_covariant.tensor())+'$$\n')
#######################################################
    # Расчёт базовой геометрии:
    # Контравариантная метрика:
    if key_calc_metric_contravariant:
        metric_contravariant = metric_covariant.inv()
        metric_contravariant.simplify()
    # Символы Кристоффеля II рода:
    if key_calc_christoffel_second:
        christoffel_second = einsteinpy.symbolic.ChristoffelSymbols.from_metric(
            metric_covariant)
        christoffel_second.simplify()
    # Тензор кривизны Римана (4-ковариантный):
    if key_calc_riemann_curvature:
        riemann_curvature = einsteinpy.symbolic.riemann.RiemannCurvatureTensor.from_metric(
            metric_covariant)
        riemann_curvature = riemann_curvature.change_config(newconfig='llll')
        riemann_curvature.simplify()
    # Скалярный квадрат тензора Римана:
    if key_calc_riemann_curvature_square:
        riemann_curvature_square = sympy.tensorcontraction(sympy.tensorcontraction(sympy.tensorcontraction(sympy.tensorcontraction(
            sympy.tensorproduct(riemann_curvature.tensor(), (riemann_curvature.change_config(newconfig='uuuu')).tensor()), (0, 4)), (0, 3)), (0, 2)), (0, 1))
        riemann_curvature_square = sympy.simplify(riemann_curvature_square)
    # Тензор Риччи (ковариантный):
    if key_calc_ricci_curvature:
        ricci_curvature = einsteinpy.symbolic.ricci.RicciTensor.from_metric(
            metric_covariant)
        ricci_curvature = ricci_curvature.change_config(newconfig='ll')
        ricci_curvature.simplify()
    # Скалярный квадрат тензора Риччи:
    if key_write_ricci_curvature_square:
        ricci_curvature_square = sympy.tensorcontraction(sympy.tensorcontraction(sympy.tensorproduct(
            ricci_curvature.tensor(), (ricci_curvature.change_config(newconfig='uu')).tensor()), (0, 2)), (0, 1))
        ricci_curvature_square = sympy.simplify(ricci_curvature_square)
    # Скалярная кривизна:
    if key_calc_ricci_scalar:
        ricci_scalar = sympy.tensorcontraction(sympy.tensorcontraction(sympy.tensorproduct(
            ricci_curvature.tensor(), metric_contravariant.tensor()), (0, 2)), (0, 1))
        ricci_scalar = sympy.simplify(ricci_scalar)
    # Тензор Эйнштейна:
    if key_calc_einstein_tensor:
        einstein_tensor = einsteinpy.symbolic.EinsteinTensor.from_metric(
            metric_covariant)
        einstein_tensor = einstein_tensor.change_config(newconfig='ll')
        einstein_tensor.simplify()
#######################################################
    # Вывод базовой геометрии
    output_object.write("\\section{Базовая геометрия:}\n")
    if key_write_metric_contravariant and key_calc_metric_contravariant:
        output_object.write("\\subsection{Контравариантная метрика:}\n")
        output_object.write(
            '$$'+sympy.latex(metric_contravariant.tensor())+'$$\n')
    if key_write_christoffel_second and key_calc_christoffel_second:
        output_object.write("\\subsection{Символы Кристоффеля II рода:}\n")
        for index_I in range(4):
            for index_II in range(4):
                for index_III in range(index_II+1):
                    output_object.write('$$'+'\\Gamma^{'+sympy.latex(coordinates[index_I])+'}_{'+sympy.latex(coordinates[index_II])+' '+sympy.latex(coordinates[index_III])+'} = \\Gamma^{'+sympy.latex(
                        coordinates[index_I])+'}_{'+sympy.latex(coordinates[index_III])+' '+sympy.latex(coordinates[index_II])+'} = '+sympy.latex(christoffel_second.tensor()[index_I][index_II, index_III])+'$$\n')
    if key_write_riemann_curvature and key_calc_riemann_curvature:
        output_object.write_riemann(riemann_curvature.tensor(), coordinates)
    if key_write_riemann_curvature_square and key_calc_riemann_curvature_square:
        output_object.write(
            "\\subsection{Скалярный квадрат тензора Римана:}\n")
        output_object.write('$$ R_{abcd}R^{abcd} = ' +
                            sympy.latex(riemann_curvature_square)+'$$\n')
    if key_write_ricci_curvature and key_calc_ricci_curvature:
        output_object.write("\\subsection{Тензор Риччи (ковариантный):}\n")
        for index_I in range(4):
            for index_II in range(index_I+1):
                output_object.write('$$'+'R_{'+sympy.latex(coordinates[index_I])+' '+sympy.latex(coordinates[index_II])+'} = R_{'+sympy.latex(
                    coordinates[index_II])+' '+sympy.latex(coordinates[index_I])+'} = '+sympy.latex(ricci_curvature.tensor()[index_I, index_II])+'$$\n')
    if key_write_ricci_curvature_square and key_calc_ricci_curvature_square:
        output_object.write("\\subsection{Скалярный квадрат тензора Риччи:}\n")
        output_object.write('$$ R_{ab}R^{ab} = ' +
                            sympy.latex(ricci_curvature_square)+'$$\n')
    if key_write_ricci_scalar and key_calc_ricci_scalar:
        output_object.write("\\subsection{Cкалярная кривизна:}\n")
        output_object.write('$$ R = '+sympy.latex(ricci_scalar)+'$$\n')
    if key_write_einstein_tensor and key_calc_einstein_tensor:
        output_object.write("\\subsection{Тензор Эйнштейна:}\n")
        for index_I in range(4):
            for index_II in range(index_I+1):
                output_object.write('$$'+'G_{'+sympy.latex(coordinates[index_I])+' '+sympy.latex(coordinates[index_II])+'} = G_{'+sympy.latex(
                    coordinates[index_II])+' '+sympy.latex(coordinates[index_I])+'} = '+sympy.latex(einstein_tensor.tensor()[index_I, index_II])+'$$\n')
#######################################################

#######################################################
    # Завершение файла:
    output_object.end()
    # Отбой счётчика времени:
    time_counter = time.perf_counter() - time_counter
    # Терминальная фраза
    print(f'Execution time: {time_counter} seconds')
#######################################################
#######################################################

    '''
    # Даламбертиан тензора Риччи (ковариантный):
    # "ricci_curvature_dalambert"
    ricci_curvature_dalambert = sympy.tensorcontraction(sympy.tensorcontraction(sympy.tensorproduct(sympy.derive_by_array(sympy.derive_by_array(ricci_curvature.tensor(), coordinates_vector), coordinates_vector), metric_contravariant.tensor()), (2, 4)), (2, 3)) - 2*sympy.tensorcontraction(sympy.tensorcontraction(sympy.tensorproduct(sympy.tensorcontraction(sympy.tensorproduct(sympy.derive_by_array(ricci_curvature.tensor(), coordinates_vector), christoffel_second.tensor()), (1, 3)), metric_contravariant.tensor()), (1, 4)), (1, 3)) - 2*sympy.tensorcontraction(sympy.tensorcontraction(sympy.tensorproduct(sympy.tensorcontraction(sympy.tensorproduct(christoffel_second.tensor(), sympy.derive_by_array(ricci_curvature.tensor(), coordinates_vector)), (0, 3)), metric_contravariant.tensor()), (0, 4)), (2, 3)) - 2*sympy.tensorcontraction(sympy.tensorcontraction(sympy.tensorproduct(sympy.tensorcontraction(sympy.tensorproduct(christoffel_second.tensor(), sympy.derive_by_array(ricci_curvature.tensor(), coordinates_vector)), (0, 5)), metric_contravariant.tensor()), (0, 4)), (0, 3)) - sympy.tensorcontraction(sympy.tensorcontraction(sympy.tensorproduct(sympy.tensorcontraction(sympy.tensorproduct(sympy.derive_by_array(christoffel_second.tensor(), coordinates_vector), ricci_curvature.tensor()), (0, 4)), metric_contravariant.tensor()), (2, 4)), (0, 3)) - sympy.tensorcontraction(sympy.tensorcontraction(sympy.tensorproduct(sympy.tensorcontraction(sympy.tensorproduct(ricci_curvature.tensor(), sympy.derive_by_array(christoffel_second.tensor(), coordinates_vector)), (1, 2)), metric_contravariant.tensor(
    )), (3, 4)), (1, 3)) + sympy.tensorcontraction(sympy.tensorcontraction(sympy.tensorproduct(sympy.tensorcontraction(sympy.tensorproduct(sympy.tensorcontraction(sympy.tensorproduct(christoffel_second.tensor(), christoffel_second.tensor()), (0, 4)), ricci_curvature.tensor()), (2, 4)), metric_contravariant.tensor()), (0, 4)), (0, 3)) + sympy.tensorcontraction(sympy.tensorcontraction(sympy.tensorproduct(sympy.tensorcontraction(sympy.tensorproduct(sympy.tensorcontraction(sympy.tensorproduct(christoffel_second.tensor(), christoffel_second.tensor()), (0, 5)), ricci_curvature.tensor()), (2, 4)), metric_contravariant.tensor()), (0, 4)), (1, 3)) + sympy.tensorcontraction(sympy.tensorcontraction(sympy.tensorproduct(sympy.tensorcontraction(sympy.tensorproduct(ricci_curvature.tensor(), sympy.tensorcontraction(sympy.tensorproduct(christoffel_second.tensor(), christoffel_second.tensor()), (0, 4))), (0, 4)), metric_contravariant.tensor()), (1, 4)), (1, 3)) + sympy.tensorcontraction(sympy.tensorcontraction(sympy.tensorproduct(sympy.tensorcontraction(sympy.tensorproduct(ricci_curvature.tensor(), sympy.tensorcontraction(sympy.tensorproduct(christoffel_second.tensor(), christoffel_second.tensor()), (0, 5))), (0, 4)), metric_contravariant.tensor()), (1, 4)), (2, 3)) + 2*sympy.tensorcontraction(sympy.tensorcontraction(sympy.tensorproduct(sympy.tensorcontraction(sympy.tensorcontraction(sympy.tensorproduct(sympy.tensorproduct(christoffel_second.tensor(), christoffel_second.tensor()), ricci_curvature.tensor()), (0, 6)), (2, 5)), metric_contravariant.tensor()), (0, 4)), (1, 3))
    ricci_curvature_dalambert = sympy.simplify(ricci_curvature_dalambert)
#    output_file.write("Даламбертиан тензора Риччи (ковариантный):\n")
#    output_file.write('$$'+sympy.latex(ricci_curvature_dalambert)+'$$\n')

    # Биградиент скалярной кривизны:
    # "ricci_scalar_bigrad"
    ricci_scalar_bigrad = sympy.derive_by_array(sympy.derive_by_array(ricci_scalar, coordinates_vector), coordinates_vector) - sympy.tensorcontraction(
        sympy.tensorproduct(christoffel_second.tensor(), sympy.derive_by_array(ricci_scalar, coordinates_vector)), (0, 3))
    ricci_scalar_bigrad = sympy.simplify(ricci_scalar_bigrad)
#    output_file.write("Биградиент скалярной кривизны:\n")
#    output_file.write('$$'+sympy.latex(ricci_scalar_bigrad)+'$$\n')
    # Даламбертиан скалярной кривизны:
    # "ricci_scalar_dalambert"
    ricci_scalar_dalambert = sympy.tensorcontraction(sympy.tensorcontraction(
        sympy.tensorproduct(ricci_scalar_bigrad, metric_contravariant.tensor()), (0, 2)), (0, 1))
    ricci_scalar_dalambert = sympy.simplify(ricci_scalar_dalambert)
#    output_file.write("Даламбертиан скалярной кривизны:\n")
#    output_file.write('$$'+sympy.latex(ricci_scalar_dalambert)+'$$\n')
    
    # Биградиент даламбертиана скалярной кривизны:
    # "ricci_scalar_dalambert_bigrad"
#    ricci_scalar_dalambert_bigrad = sympy.derive_by_array(sympy.derive_by_array(ricci_scalar_dalambert, coordinates_vector), coordinates_vector) - sympy.tensorcontraction(
#        sympy.tensorproduct(christoffel_second.tensor(), sympy.derive_by_array(ricci_scalar_dalambert, coordinates_vector)), (0, 3))
#    ricci_scalar_dalambert_bigrad = sympy.simplify(
#        ricci_scalar_dalambert_bigrad)
#    output_file.write("Биградиент даламбертиана скалярной кривизны:\n")
#    output_file.write('$$'+sympy.latex(ricci_scalar_dalambert_bigrad)+'$$\n')
    # Даламбертиан даламбертиана скалярной кривизны:
#    ricci_scalar_dalambert_2 = sympy.tensorcontraction(sympy.tensorcontraction(
#        sympy.tensorproduct(ricci_scalar_dalambert_bigrad, metric_contravariant.tensor()), (0, 2)), (0, 1))
#    ricci_scalar_dalambert_2 = sympy.simplify(ricci_scalar_dalambert_2)
#    output_file.write("Даламбертиан даламбертиана скалярной кривизны:\n")
#    output_file.write('$$'+sympy.latex(ricci_scalar_dalambert_2)+'$$\n')

    # ----------------------------------------------------------------------

    # Расчёт уравнений (ковариантных)
    # -----------------------------------------------------------
    lambda_member = \
        sympy.simplify((1/2)*metric_covariant.tensor())
    kappa_member = sympy.simplify(
        (1/2)*ricci_scalar*metric_covariant.tensor() - ricci_curvature.tensor())
    alpha_member = sympy.simplify((1/2)*(ricci_scalar**2)*metric_covariant.tensor(
    ) + 2*ricci_scalar_bigrad - 2*ricci_scalar_dalambert*metric_covariant.tensor() - 2*ricci_scalar*ricci_curvature.tensor())
    beta_member = sympy.simplify((1/2)*metric_covariant.tensor()*ricci_curvature_square + ricci_scalar_bigrad - 2*sympy.tensorcontraction(sympy.tensorcontraction(sympy.tensorproduct(
        riemann_curvature.tensor(), (ricci_curvature.change_config(newconfig='uu')).tensor()), (1, 4)), (2, 3)) - ricci_curvature_dalambert - (1/2)*ricci_scalar_dalambert*metric_covariant.tensor())
#    gamma_member = sympy.simplify(- 2*ricci_scalar_dalambert*ricci_curvature.tensor() + 2*ricci_scalar_dalambert_bigrad - 2*ricci_scalar_dalambert_2*metric_covariant.tensor() - (1/2)*sympy.tensorcontraction(sympy.tensorcontraction(sympy.tensorproduct(metric_contravariant.tensor(), sympy.tensorproduct(
#        sympy.derive_by_array(ricci_scalar, coordinates_vector), sympy.derive_by_array(ricci_scalar, coordinates_vector))), (0, 2)), (0, 1))*metric_covariant.tensor() + sympy.tensorproduct(sympy.derive_by_array(ricci_scalar, coordinates_vector), sympy.derive_by_array(ricci_scalar, coordinates_vector)))
    output_file.write("Уравнения:\n")
    for index_I in range(4):
        for index_II in range(index_I + 1):
            output_file.write('\n')
            output_file.write('% New equation\n')
            output_file.write('\n')
            output_file.write(
                "For $ g_{ "+f"{sympy.latex(coordinates[index_I])} "+f"{sympy.latex(coordinates[index_II])}"+" } $ :\n")
            output_file.write('\n')
            output_file.write("$\\lambda$-член:\n")
            output_file.write(
                '$$' + sympy.latex(sympy.collect(lambda_member[index_I][index_II])) + '$$\n')
            output_file.write('\n')
            output_file.write("$\\kappa$-член:\n")
            output_file.write(
                '$$' + sympy.latex(sympy.collect(kappa_member[index_I][index_II])) + '$$\n')
            output_file.write('\n')
            output_file.write("$\\alpha$-член:\n")
            output_file.write(
                '$$' + sympy.latex(sympy.collect(alpha_member[index_I][index_II])) + '$$\n')
            output_file.write('\n')
            output_file.write("$\\beta$-член:\n")
            output_file.write(
                '$$' + sympy.latex(sympy.collect(beta_member[index_I][index_II])) + '$$\n')
#            output_file.write('\n')
#            output_file.write("$\\gamma$-член:\n")
#            output_file.write(
#                '$$' + sympy.latex(sympy.collet(gamma_member[index_I][index_II])) + '$$\n')
    # -----------------------------------------------------------
    '''
