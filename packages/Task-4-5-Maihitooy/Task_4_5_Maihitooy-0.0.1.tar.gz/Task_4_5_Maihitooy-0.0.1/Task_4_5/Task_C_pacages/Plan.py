from Practic.Task_C_pacages.Academic import Academic
from Practic.Task_C_pacages.Practice import Practice
from Practic.Task_C_pacages.Base.function import logg


class Plan:
    """Создать класс Plan. Поля: код направления, название направления, кафедр, список основных дисциплин (список
    экземпляров класса Academic), список практик (список экземпляров класса Practice). Определить конструктор.
    Переопределить метод преобразования в строку для печати всей информации об учебном плане (с использованием
    переопределения в классах Academic и Practice). Переопределить методы получения количества дисциплин
    функцией len, получения дисциплины по индексу, изменения по индексу, удаления по индексу (пусть вначале
    идут индексы основных дисциплин, затем практик). Переопределить операции + и - для добавления или удаления
    дисциплины. Добавить функцию создания txt-файла и записи всей информации в него (в том числе количество
    часов и тематику практик)."""

    @logg("CRE", "Вызван __init__ класса Plan")
    def __init__(self, direction_code: int, name_of_the_direction: str, department: str,
                 list_of_main_disciplines: list, list_of_practices: list):

        self.__direction_code = direction_code
        self.__name_of_the_direction = name_of_the_direction
        self.__department = department
        self.__list_of_main_disciplines = list_of_main_disciplines
        self.__list_of_practices = list_of_practices

    @logg("INF", "Изменение, вызван __getitem__ класса Plan, функция получения элемента")
    def __getitem__(self, index: int) -> Academic:
        return self.__list_of_main_disciplines[index]

    @logg("INF", "Изменение, вызван __setitem__ класса Plan, функция изменения элемента")
    def __setitem__(self, index: int, academic: Academic) -> Academic:
        try:
            self.__list_of_main_disciplines[index] = academic
            return self.__list_of_main_disciplines[index]
        except IndexError:
            print("Вы что-то делаете не так")
            logg("ERR", "Ошибка, __setitem__ класса Plan, функция изменения элемента")(lambda: None)()

    @logg("INF", "Изменение, вызван __delitem__ класса Plan, функция удаления элемента")
    def __delitem__(self, index: int) -> None:
        try:
            if index <= len(self.__list_of_main_disciplines):
                self.__list_of_main_disciplines.pop(index)
            else:
                self.__list_of_practices.pop(index - len(self.__list_of_main_disciplines))
        except IndexError:
            print("Вы что-то делаете не так")
            logg("ERR", "Ошибка, __delitem__ класса Plan, функция удаления элемента")(lambda: None)()

    @logg("INF", "Изменение, вызван create_file класса Plan, функция сохранения в файл")
    def create_file(self, path="", name="Plan", extension=".txt") -> None:

        text = f"Код направления: {self.__direction_code}, название направления: {self.__name_of_the_direction}, " \
               f"кафедра: {self.__department}\nCписок основных дисциплин:\n"

        for item in self.__list_of_main_disciplines:
            text = text + " * " + item.__str__()
            text = text + "     * " + "Часы:\n"
            for key, value in item.get_hours().items():
                text += "         * " + f"форма занятия: {key}, количество занятий: {value}\n"

        text = text + "Cписок практик:\n"
        for item in self.__list_of_practices:
            text = text + " * " + item.__str__()
            text = text + "     * " + "Темы для практик:\n"
            for topic in item.get_topics_of_practice():
                text += "         * " + topic + "\n"

        with open(path + name + extension, "w") as file:
            print(text, file=file)

    @logg("INF", "Изменение, вызван __add__ класса Plan, функция добавления элемента")
    def __add__(self, other) -> None:
        if type(other) == Academic:
            self.__list_of_main_disciplines.append(other)
        elif type(other) == Practice:
            self.__list_of_practices.append(other)

    @logg("INF", "Изменение, вызван __sub__ класса Plan, функция удаления элемента")
    def __sub__(self, other) -> None:
        if type(other) == Academic:
            for index in range(len(self.__list_of_main_disciplines)):
                if self.__list_of_main_disciplines[index] == other:
                    self.__list_of_main_disciplines.pop(index)
                    break

        elif type(other) == Practice:
            for index in range(len(self.__list_of_practices)):
                if self.__list_of_practices[index] == other:
                    self.__list_of_practices.pop(index)
                    break

    @logg("INF", "Изменение, вызван __len__ класса Plan, функция кол-ва элементов")
    def __len__(self) -> int:
        return len(self.__list_of_main_disciplines) + len(self.__list_of_practices)

    @logg("INF", "Изменение, вызван __str__ класса Plan, функция преобразования в строку")
    def __str__(self) -> str:
        text = f"Код направления: {self.__direction_code}, название направления: {self.__name_of_the_direction}, " \
               f"кафедра: {self.__department}\nCписок основных дисциплин:\n"

        for item in self.__list_of_main_disciplines:
            text = text + " * " + item.__str__() + "\n"

        text = text + "Cписок практик:\n"
        for item in self.__list_of_practices:
            text = text + " * " + item.__str__() + "\n"

        return text
