import datetime
import os


def logg(key: str, comm: str):
    # Ключи: CRE (создание экземпляра класса), INF (изменение), ERR (сработало исключение).
    # Файл строки следующего содержания: КЛЮЧ --- ДАТА И ВРЕМЯ --- КОММЕНТАРИЙ.
    # Комментарий: создано …, удален …, добавлен …, распечатан …
    def decorate(function):
        def wrapper(*args, **kwargs):
            if not os.path.isdir("logg"):
                os.mkdir("logg")
            date = str(datetime.date.today()).replace(' ', '_')
            with open(rf'logg\logg_{date}.txt', "a", encoding='UTF-8') as file:
                print(f"{key} --- {datetime.datetime.now()} --- {comm}", file=file)
            return function(*args, **kwargs)

        return wrapper

    return decorate

