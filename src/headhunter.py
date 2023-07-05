from .abc_classes import JobParser

from requests import *
import json


class HeadHunter(JobParser):
    """
    Класс для работы с API сайта headhunter.ru
    """

    _api_link_vacancies = "https://api.hh.ru/vacancies"
    _api_link_employers = "https://api.hh.ru/employers"

    def __str__(self):
        return "headhunter.ru"

    def get_vacancies(self, **kwargs):
        """
        :param kwargs:
        text - Поисковый запрос
        per_page - Количество вакансий на странице
        :return:
        Возвращает список вакансий
        """
        params = {}
        for key, value in kwargs.items():
            params[key] = value

        response = get(self._api_link_vacancies, params=params)

        if response.status_code == 200:
            data = response.text
            data_dict = json.loads(data)
            return data_dict
        else:
            print("Ошибка при выполнении запроса:", response.status_code)
            return None

    def get_search_vacancies(self, search_data, n=10):
        """
        Метод для поиска вакансий по параметрам
        :param search_data: Поисковый запрос
        :param n: Количество вакансий на странице
        :return:
        Возвращает список найденных вакансий в соответствии с параметрами
        """
        return self.get_vacancies(text=search_data, per_page=n)

    def get_employer(self, employer_id):
        response = get(f'{self._api_link_employers}/{employer_id}')

        if response.status_code == 200:
            return json.loads(response.text)
        else:
            print("Ошибка при выполнении запроса:", response.status_code)
            return None
