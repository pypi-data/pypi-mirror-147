from Practic.Task_C_pacages.Base.function import logg


class Discipline:
    """Создать класс Discipline с полями название, семестр, кафедра. Добавить конструктор класса."""

    @logg("CRE", "Вызван __init__ класса Discipline")
    def __init__(self, name: str, term: int, department: str):
        self._name = name
        self._term = term
        self._department = department
