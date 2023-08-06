from Practic.Task_C_pacages.Base.Discipline import Discipline
from Practic.Task_C_pacages.Base.function import logg


class Academic(Discipline):
    """Создать производный от Discipline класс Academic. Новые поля: преподаватель, форма контроля (зачет или экзамен),
    часы (словарь вида форма занятия (лекция/лабораторная/практическая): количество занятий). Определить конструктор,
    с вызовом родительского конструктора. Определить функции изменения преподавателя и формы контроля,
    форматированной печати количества занятий различного вида. Переопределить метод преобразования в строку
    для печати основной информации (название, семестр, кафедра, преподаватель, форма контроля)."""

    @logg("CRE", "Вызван __init__ класса Academic, конструктор")
    def __init__(self, name: str, term: int, department: str, teacher: str, form_of_control: str, hours: dict):
        super().__init__(name, term, department)

        self.__teacher = teacher
        self.__form_of_control = form_of_control
        self.__hours = hours

    @logg("INF", "Изменение, вызван set_teacher класса Academic, функция изменения преподавателя")
    def set_teacher(self, teacher: str) -> None:
        self.__teacher = teacher

    @logg("INF", "Изменение, вызван set_form_of_control класса Academic, функция изменения формы контроля")
    def set_form_of_control(self, form_of_control: str) -> None:
        self.__form_of_control = form_of_control

    @logg("INF", "Изменение, вызван get_hours класса Academic, возвращено")
    def get_hours(self) -> dict:
        return self.__hours

    @logg("INF",
          "Изменение, вызван print_hours класса Academic, "
          "функция форматированной печати количества занятий различного вида")
    def print_hours(self) -> None:
        for key, value in self.__hours.items():
            print(f"Тип: {key}, кол-во часов: {value}")

    @logg("INF", "Изменение, вызван __eq__ класса Academic, операция сравнения")
    def __eq__(self, other) -> bool:
        return self._name == other._name \
               and self._term == other._term \
               and self._department == other._department \
               and self.__teacher == other.__teacher \
               and self.__form_of_control == other.__form_of_control \
               and self.__hours == other.__hours

    @logg("INF", "Изменение, вызван __str__ класса Academic, O_o")
    def __str__(self) -> str:
        return f"название: {self._name}, семестр: {self._term}, кафедра: {self._department}," \
               f" преподаватель: {self.__teacher}, форма контроля: {self.__form_of_control}\n"
