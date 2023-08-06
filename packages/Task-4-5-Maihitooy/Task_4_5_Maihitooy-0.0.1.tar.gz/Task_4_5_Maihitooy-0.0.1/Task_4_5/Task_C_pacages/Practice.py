from Practic.Task_C_pacages.Base.Discipline import Discipline
from Practic.Task_C_pacages.Base.function import logg


class Practice(Discipline):
    """Создать производный от Discipline класс Practice. Новые поля: вид практики (учебная/производственная/преддипломная),
    руководитель практики, тематика практики (список тем). Определить конструктор, с вызовом родительского
    конструктора. Определить функции изменения руководителя, добавления, удаления и изменения тематики.
    Переопределить метод преобразования в строку для печати основной информации (название, вид практики, семестр,
    кафедра, руководитель)."""

    @logg("CRE", "Вызван __init__ класса Practice, конструктор")
    def __init__(self, name: str, term: int, department: str, type_of_practice: str, head_of_practice: str,
                 topics_of_practice: list):
        super().__init__(name, term, department)

        self.__type_of_practice = type_of_practice
        self.__head_of_practice = head_of_practice
        self.__topics_of_practice = topics_of_practice

    @logg("INF", "Изменение, вызван set_head_of_practice класса Practice, функция изменения руководителя")
    def set_head_of_practice(self, head_of_practice: str) -> None:
        self.__head_of_practice = head_of_practice

    @logg("INF", "Изменение, вызван add_topics_of_practice класса Practice, функция добавления тематики")
    def add_topics_of_practice(self, topic: str) -> None:
        self.__topics_of_practice.append(topic)

    @logg("INF", "Изменение, вызван delete_index_topics класса Practice, функция удаления тематики")
    def delete_index_topics(self, index: int) -> None:
        try:
            self.__topics_of_practice.pop(index)
        except IndexError:
            print("Вы что-то делаете не так")
            logg("ERR", "Ошибка, delete_index_topics класса Practice, функция удаления тематики")(lambda: None)()

    @logg("INF", "Изменение, вызван set_index_topics класса Practice, функция изменения тематики")
    def set_index_topics(self, index: int, topic: str) -> None:
        try:
            self.__topics_of_practice[index] = topic
        except IndexError:
            print("Вы что-то делаете не так")
            logg("ERR", "Ошибка, set_index_topics класса Practice, функция изменения тематики")(lambda: None)()

    @logg("INF", "Изменение, вызван get_topics_of_practice класса Practice, функция получения тематик")
    def get_topics_of_practice(self) -> list:
        return self.__topics_of_practice

    @logg("INF", "Изменение, вызван __eq__ класса Practice, операция сравнения")
    def __eq__(self, other) -> bool:
        return self._name == other._name \
               and self._term == other._term \
               and self._department == other._department \
               and self.__type_of_practice == other.__type_of_practice \
               and self.__head_of_practice == other.__head_of_practice \
               and self.__topics_of_practice == other.__topics_of_practice

    @logg("INF", "Изменение, вызван __str__ класса Practice, преобразования в строку")
    def __str__(self) -> str:
        return f"название: {self._name}, вид практики: {self.__type_of_practice}, семестр: {self._term}," \
               f" кафедра: {self._department}, руководитель: {self.__head_of_practice}\n"
