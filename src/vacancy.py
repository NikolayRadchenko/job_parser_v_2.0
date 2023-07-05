import json


class Vacancy:
    """
    Класс для работы с вакансиями
    id - id вакансии
    name - название вакансии
    salary - зарплата предлагаемая в вакансии
    description - описание вакансии
    link - ссылка на вакансию
    """
    def __init__(self, id: str, name: str, salary: str, description: str, link: str):
        self.id = id
        self.name = name
        self.salary = salary
        self.description = description
        self.link = link

    def __eq__(self, other):
        return self.str_to_digit(self.salary) == self.str_to_digit(other.salary)

    def __lt__(self, other):
        return self.str_to_digit(self.salary) < self.str_to_digit(other.salary)

    def __gt__(self, other):
        return self.str_to_digit(self.salary) > self.str_to_digit(other.salary)

    def str_to_digit(self, string):
        return int(string.split(" ")[0])

    # def get_employer_data(self, data) -> list[dict]:
    #     """Извлекает данные о работодателях из JSON-данных
    #      и возвращает список словарей с соответствующей информацией."""
    #     data_employer = []
    #     data_employer.append(data[])
    #     return data_employer
