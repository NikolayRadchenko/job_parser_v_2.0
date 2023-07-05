from prettytable import PrettyTable, ALL


def get_prettytable():
    """
    Метод для создания таблицы для удобного вывода
    """
    table = PrettyTable()
    table.field_names = ["id", "Вакансия", "Зарплата", "Описание", "Ссылка"]

    # Установка горизонтальных линий
    table.hrules = ALL
    return table


def print_prettytable(json_data, sorty: str):
    """
    Метод сбора данных с сайта headhunter.ru в таблицы
    :param json_data: данные о вакансиях в формате JSON
    :param sorty: вариант сортировки
    """

    table = get_prettytable()
    vacancies = []

    for item in json_data["items"]:
        item_values = []
        values = {}
        item_values.append(item.get("id", ""))
        values["id"] = item_values[0]
        item_values.append(item.get("name", "")[:30])
        values["name"] = item_values[1]
        if item.get("salary", "") is not None:
            item_values.append(f'{item.get("salary", {}).get("from", "")} '
                               f'{item.get("salary", {}).get("currency", "")}')
        elif item.get("salary", "") is not None:
            if item.get("salary", {}).get("from") is None:
                item_values.append(f'{item.get("salary", {}).get("to", "")} '
                                   f'{item.get("salary", {}).get("currency", "")}')
        else:
            item_values.append("Не указана")
        values["salary"] = item_values[2]
        if item.get("snippet", {}).get("responsibility", "") is not None:
            item_values.append(f'{item.get("snippet", {}).get("responsibility", "")[0:50]}...')
        else:
            item_values.append("Не указано")
        values["description"] = item_values[3]
        item_values.append(item.get("alternate_url", ""))
        values["url"] = item_values[4]
        vacancies.append(values)

        table.add_row(item_values)
    return table.get_string(sortby=sorty), vacancies
