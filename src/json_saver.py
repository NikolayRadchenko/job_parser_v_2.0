import json
import os


class JSONSaver:
    """
    Класс для работы с данными и файлами в формате JSON
    filename - названия файла для работы с ним
    """
    def __init__(self, filename):
        self.__filename = filename

        os.chdir(os.path.abspath(".."))
        folder_path = os.path.abspath("data")
        self.file_path = os.path.join(folder_path, filename)

    @property
    def file(self):
        return self.__filename

    @file.setter
    def file(self, name):
        self.__filename = name

    def add_vacancy(self, vacancy_data):
        """
        Метод для записи JSON данных в файл
        """
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(vacancy_data, file, indent=2, ensure_ascii=False)
        return self.file_path

    def get_vacancies(self):
        """
        Метод для получения JSON данных из файла
        """
        with open(self.file_path, 'r', encoding="utf-8") as file:
            return self.printjson(json.load(file))

    def remove_vacancy(self, vacancy_id, platform):
        """
        Метод для удаления вакансии из JSON файла
        """
        with open(self.file_path, encoding="utf8") as file:
            data = json.load(file)
            if platform == "headhunter.ru":
                data['items'] = list(
                    filter(
                        lambda x: x.get('id') not in vacancy_id,
                        data.get('items', [])
                    )
                )
            elif platform == "superjob.ru":
                data['objects'] = list(
                    filter(
                        lambda x: x.get('id') not in vacancy_id,
                        data.get('objects', [])
                    )
                )
        with open(self.file_path, "w", encoding="utf8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    def printjson(self, data_dict):
        """
        Метод для удобного отображения JSON данных
        """
        print(json.dumps(data_dict, indent=2, ensure_ascii=False))
