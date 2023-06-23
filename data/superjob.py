from abc_api import JobParser

from requests import *
import os
import json


class SuperJob(JobParser):
    __api_key = os.getenv('SJ_API_KEY')
    _api_link = "https://api.superjob.ru/2.0/vacancies"

    def __str__(self):
        return "superjob.ru"

    def get_vacancies_api(self, **kwargs):
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
