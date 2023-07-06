from prettytable import PrettyTable, ALL


def get_prettytable():
    """
    Метод для создания таблицы для удобного вывода
    """
    table = PrettyTable()
    table.field_names = ["id", "id работодателя", "Вакансия", "Зарплата", "Ссылка", "Описание"]

    # Установка горизонтальных линий
    table.hrules = ALL
    return table


def print_prettytable(data, sorty: str):
    """
    Метод сбора данных с сайта headhunter.ru в таблицы
    :param data: данные о вакансиях в формате JSON
    :param sorty: вариант сортировки
    """

    table = get_prettytable()

    for items in data:
        vacancy = []
        for item in items:
            vacancy.append(item)
        table.add_row(vacancy)
    return table.get_string(sortby=sorty, reversesort=True)


def get_prettytable_avg_salary():
    """
    Метод для создания таблицы для удобного вывода
    """
    table = PrettyTable()
    table.field_names = ["Средняя зарплата по вакансиям"]

    # Установка горизонтальных линий
    table.hrules = ALL
    return table


def print_prettytable_avg_salary(data):
    """
    Метод сбора данных с сайта headhunter.ru в таблицы
    :param data: данные о вакансиях в формате JSON
    :param sorty: вариант сортировки
    """

    table = get_prettytable_avg_salary()

    for items in data:
        vacancy = []
        for item in items:
            vacancy.append(item)
        table.add_row(vacancy)
    return table.get_string()

def get_prettytable_company():
    """
    Метод для создания таблицы для удобного вывода
    """
    table = PrettyTable()
    table.field_names = ["Название компании", "Количество открытых вакансий"]

    # Установка горизонтальных линий
    table.hrules = ALL
    return table


def print_prettytable_company(data):
    """
    Метод сбора данных с сайта headhunter.ru в таблицы
    :param data: данные о вакансиях в формате JSON
    :param sorty: вариант сортировки
    """

    table = get_prettytable_company()

    for items in data:
        vacancy = []
        for item in items:
            vacancy.append(item)
        table.add_row(vacancy)
    return table.get_string()
