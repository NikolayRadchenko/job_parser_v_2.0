from .abc_classes import JobParser

from requests import *
import json


class HeadHunter(JobParser):
    """
    Класс для работы с API сайта headhunter.ru
    """

    _api_link_vacancies = "https://api.hh.ru/vacancies"
    _api_link_employers = "https://api.hh.ru/employers/{}"

    def __str__(self):
        return "headhunter.ru"

    def get_vacancies(self, employer_id):
        params = {'employer_id': employer_id}
        response = get(self._api_link_vacancies, params=params)

        if response.status_code == 200:
            data = response.text
            data_dict = json.loads(data)
            return data_dict
        else:
            print("Ошибка при выполнении запроса:", response.status_code)
            return None

    def get_employers(self, employer_id):
        response = get(self._api_link_employers.format(employer_id))

        if response.status_code == 200:
            return json.loads(response.text)
        else:
            print("Ошибка при выполнении запроса:", response.status_code)
            return None

    def get_vacancy_data(self, data) -> list[dict]:
        values = []
        value = {}

        for item in data:
            value["id"] = item["id"]
            value["employer_id"] = item["employer"]["id"]
            value["name"] = item["name"]
            if item.get("salary", "") is not None:
                value["salary"] = f'{item.get("salary", {}).get("from", "")}' \
                                  f'{item.get("salary", {}).get("currency", "")}'
            elif item.get("salary", "") is not None:
                if item.get("salary", {}).get("from") is None:
                    value["salary"] = f'{item.get("salary", {}).get("to", "")}' \
                                      f'{item.get("salary", {}).get("currency", "")}'
            else:
                value["salary"] = "Не указана"
            if item.get("snippet", {}).get("responsibility", "") is not None:
                value["description"] = f'{item.get("snippet", {}).get("responsibility", "")[0:50]}...'
            else:
                value["description"] = "Не указано"
            value["url"] = item.get("alternate_url", "")
            values.append(value)
            value = {}

        return values
