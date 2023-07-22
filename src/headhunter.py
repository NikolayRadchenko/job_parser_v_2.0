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
        """
        Метод для получения вакансий с сайта headhanter.ru
        """
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
        """
        Метод для получения информации об избранных работодателях с сайта headhanter.ru
        """
        response = get(self._api_link_employers.format(employer_id))

        if response.status_code == 200:
            return json.loads(response.text)
        else:
            print("Ошибка при выполнении запроса:", response.status_code)
            return None

    def get_vacancy_data(self, data) -> list[list]:
        """
        Метод для приведения полученной информации о вакансиях с сайта headhanter.ru в удобный формат
        """
        values = []
        value = []

        for item in data:
            value.append(item["id"])
            value.append(item["employer"]["id"])
            value.append(item["name"])
            if item.get("salary", "") is not None:
                value.append(f'{item.get("salary", {}).get("from", "")}{item.get("salary", {}).get("currency")[:-3]}')
            elif item.get("salary", "") is not None:
                if item.get("salary", {}).get("from") is None:
                    value.append(f'{item.get("salary", {}).get("to", "")}{item.get("salary", {}).get("currency")[:-3]}')
            else:
                value.append("Не указана")
            if item.get("snippet", {}).get("responsibility", "") is not None:
                value.append(f'{item.get("snippet", {}).get("responsibility", "")[0:50]}...')
            else:
                value.append("Не указано")
            value.append(item.get("alternate_url", ""))
            values.append(value)
            value = []

        return values

    def get_employer_data(self, data) -> list[dict]:
        """
        Метод для приведения полученной информации о работодателях с сайта headhanter.ru в удобный формат
        """
        values = []

        values.append(data["id"])
        values.append(data["name"])
        values.append(data.get("site_url", ""))
        values.append(data.get("open_vacancies", ""))
        values.append(data.get("alternate_url", ""))

        return values
