import json
import os


class JSONSaver:
    def __init__(self, filename):
        self.__filename = filename

        os.chdir(os.path.abspath(".."))
        folder_path = os.path.abspath("job_parser/data")
        self.file_path = os.path.join(folder_path, filename)

    @property
    def file(self):
        return self.__filename

    @file.setter
    def file(self, name):
        self.__filename = name

    def add_vacancy(self, vacancy_data):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(vacancy_data, file, indent=2, ensure_ascii=False)
        return self.file_path

    def get_vacancies(self, platform, **kwargs):
        with open(self.file_path, 'r') as file:
            return self.printjson(json.load(file))

    def remove_vacancy(self, vacancy_id):
        with open(self.file, 'r') as f:
            lines = f.readlines()

        with open(self.file, 'w') as f:
            for line in lines:
                vacancy = json.loads(line)
                if vacancy.get('id') != vacancy_id:
                    f.write(line)

    def printjson(self, data_dict):
        print(json.dumps(data_dict, indent=2, ensure_ascii=False))
