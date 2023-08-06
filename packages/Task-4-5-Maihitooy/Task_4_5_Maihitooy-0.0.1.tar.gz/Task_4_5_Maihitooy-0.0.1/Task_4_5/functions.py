import random
from matplotlib import pyplot as plt


# размер популяции, размеры сетки, процентное соотношение агентов двух групп,
# пороговое значение «толерантности», количество шагов моделирования.

# Класс, который хранит значения соответсвующее полям на сетке
# Пустая область - это empty = 0
# Агент первого типа - agent_1 = 1
# Агент второго типа - agent_2 = 2
class Info:
    empty = 0
    agent_1 = 1
    agent_2 = 2


# Функция, которая создает матрицу и заполняет её значениями по условию
# Первый параметр это размерность матрицы 2x2, 3x3 и т.п
# Второй параметр это размер популяции, сколько в сумме агентов первого типа и второго типа
# Третий параметр это отношение первых агентов ко вторым агентам
# пример: размер = 100, популяция 100, отношение 50 => агентов первого типа 50, второго типа 50, пустых областей 0
def create_matrix(size: int, population: int, relation: int) -> list:
    # список где в будущем будет матрица
    matrix = []

    # Высчитываем кол-во агентов первой группы
    group_1 = int((population * relation) / 100)
    # Высчитываем кол-во агентов второй группы
    group_2 = population - group_1
    # Высчитываем кол-во пустых областей
    empty = size ** 2 - group_1 - group_2

    # Переменная счетчик для хранения текущего кол-ва агентов перовой группы
    count_group_1 = 0
    # Переменная счетчик для хранения текущего кол-ва агентов второй группы
    count_group_2 = 0
    # Переменная счетчик для хранения текущего кол-ва пустых областей
    count_empty = 0

    # Временный список для создания списка с нужным кол-вом элементов
    temp = []
    for i in range(size ** 2):
        # Нужно ли еще добавлять агентов первого типа
        if count_group_1 < group_1:
            temp.append(Info.agent_1)
            count_group_1 += 1
        # Нужно ли еще добавлять агентов второго типа
        elif count_group_2 < group_2:
            temp.append(Info.agent_2)
            count_group_2 += 1
        # Нужно ли еще добавлять пустые области
        elif count_empty < empty:
            temp.append(Info.empty)
            count_empty += 1
    # После того как мы составили список, все элементы идут упорядочено, сначала первые агенты, потом вторые,
    # Потом пустые области. [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 0, 0, 0]
    # Поэтому мы вызываем метод shuffle из библиотеки random который перемешает элементы в последовательности
    random.shuffle(temp)

    # Теперь из перемешанного списка нужно составить матрицу
    # Начало от 0, до размера в квадрате и с шагом размера матрицы
    # Пример: range(0, 100, 10): [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
    for i in range(0, size ** 2, size):
        # Берем срез размеров в size
        matrix.append(temp[i:i + size])

    # Возвращаем готовую матрицу
    return matrix


# Функция на основе метрики манхеттенского расстояния.
# Возвращает расстояние от 1 точки к другой
def distance(i: int, j: int, i_empty: int, j_empty: int) -> int:
    return abs(i - i_empty) + abs(j - j_empty)


# Функция ищет все свободные поля и возвращает список их индексов
def find_empty(matrix: list) -> list:
    index_list = []
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == Info.empty:
                index_list.append([i, j])

    return index_list


def add_score(item: int, group_1: int, group_2: int) -> tuple:
    if item == Info.agent_1:
        group_1 += 1
    elif item == Info.agent_2:
        group_2 += 1

    return group_1, group_2


def is_happy(matrix: list, i: int, j: int, size=1, quantity=4, tolerance=3) -> bool:
    # Кол-во агентов №1
    group_1 = 0
    # Кол-во агентов №2
    group_2 = 0

    for _i in range(i - size, i + size + 1):
        for _j in range(j - size, j + size + 1):
            group_1, group_2 = add_score(
                matrix[_i if _i < 0 else _i % len(matrix)][_j if _j < 0 else _j % len(matrix)],
                group_1,
                group_2
            )

    if matrix[i][j] == Info.agent_1:
        return (group_1 - 1) >= quantity and group_2 <= tolerance
    else:
        return (group_2 - 1) >= quantity and group_1 <= tolerance


def happy_plot(happy: list) -> None:
    plt.plot(happy)
    plt.title("Изменение счастье агентов")
    plt.show()
