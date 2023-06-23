from abc_api import JobParser

from requests import *
import json


class HeadHunter(JobParser):

    _api_link = "https://api.hh.ru/vacancies"

    def __str__(self):
        return "headhunter.ru"

    def get_vacancies(self, **kwargs):
        params = {}
        for key, value in kwargs.items():
            params[key] = value

        response = get(self._api_link, params=params)

        if response.status_code == 200:
            data = response.text
            data_dict = json.loads(data)
            return data_dict
        else:
            print("Ошибка при выполнении запроса:", response.status_code)
            return None

    def get_search_vacancies(self, search_data, n=10):
        return self.get_vacancies(text=search_data, per_page=n)
