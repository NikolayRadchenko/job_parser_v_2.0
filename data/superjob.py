from abc_api import JobParser

from requests import *
import os
import json


class SuperJob(JobParser):
    """
        Класс для работы с API сайта superjob.ru
    """
    __api_key = os.getenv('SJ_API_KEY')
    _api_link = "https://api.superjob.ru/2.0/vacancies"

    def __str__(self):
        return "superjob.ru"

    def get_vacancies(self, **kwargs):
        """
        :param kwargs:
        text - Поисковый запрос
        per_page - Количество вакансий на странице
        :return:
        Возвращает список вакансий
        """
        params = {}
        headers = {
            'X-Api-App-Id': self.__api_key
        }

        for key, value in kwargs.items():
            params[key] = value

        response = get(self._api_link, headers=headers, params=params)
        if response.status_code == 200:
            data = response.text
            data_dict = json.loads(data)
            return data_dict
        else:
            print("Ошибка при выполнении запроса.")
            return []

    def get_search_vacancies(self, search_data, n=10):
        """
        Метод для поиска вакансий по параметрам
        :param search_data: Поисковый запрос
        :param n: Количество вакансий на странице
        :return:
        Возвращает список найденных вакансий в соответствии с параметрами
        """
        return self.get_vacancies(keyword=search_data, count=n)
