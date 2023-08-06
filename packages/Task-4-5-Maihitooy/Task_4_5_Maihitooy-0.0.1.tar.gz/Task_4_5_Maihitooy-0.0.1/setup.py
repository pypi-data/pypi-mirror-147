# Импорт недавно установленного пакета setuptools.
import setuptools
from io import open
from setuptools import setup

# Открытие README.md и присвоение его long_description.
with open("README.md", "r") as fh:
    long_description = fh.read()

# Определение requests как requirements для того, чтобы этот пакет работал. Зависимости проекта.
# requirements = ["requests<=2.21.0"]

with open("requirements.txt", "r", encoding='utf-16') as freq:
    requirements = [item.replace("\n", '') for item in freq.readlines()]

# Функция, которая принимает несколько аргументов. Она присваивает эти значения пакету.
setuptools.setup(
    # Имя дистрибутива пакета. Оно должно быть уникальным, поэтому добавление вашего имени пользователя в конце
    # является обычным делом.
    name="Task_4_5_Maihitooy",
    # Номер версии вашего пакета. Обычно используется семантическое управление версиями.
    version="0.0.1",
    # Имя автора.
    author="Maihitooy",
    # Его почта.
    author_email="markevich_maria@bk.ru",
    # Краткое описание, которое будет показано на странице PyPi.
    description="A task",
    # Длинное описание, которое будет отображаться на странице PyPi. Использует README.md репозитория для заполнения.
    # long_desription=long_description,
    # Определяет тип контента, используемый в long_description.
    # long_description_content_type="text/markdown",
    # URL-адрес, представляющий домашнюю страницу проекта. Большинство проектов ссылаются на репозиторий.
    # url="https://github.com/Maihitooy/Django-site/tree/main/courses",
    # Находит все пакеты внутри проекта и объединяет их в дистрибутив.
    packages=setuptools.find_packages(),
    # requirements или dependencies, которые будут установлены вместе с пакетом,
    # когда пользователь установит его через pip.
    # install_requires=requirements,
    # Предоставляет pip некоторые метаданные о пакете. Также отображается на странице PyPi.
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # Требуемая версия Python.
    python_requires='>=3.6',
)
