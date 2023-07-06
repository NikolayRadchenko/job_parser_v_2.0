from abc import ABC, abstractmethod


class JobParser(ABC):
    """

    Абстрактный класс для работы с API сайтов поиска вакансий
    """
    @abstractmethod
    def get_vacancies(self, employer_id):
        """
        Метод для подключения к API и получения вакансий
        """
        pass
