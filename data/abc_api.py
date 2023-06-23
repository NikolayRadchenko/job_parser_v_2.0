from abc import ABC, abstractmethod


class JobParser(ABC):
    @abstractmethod
    def get_vacancies(self):
        pass
