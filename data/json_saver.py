import json


class JSONSaver:
    def __init__(self, filename):
        self.__filename = filename

    @property
    def file(self):
        return self.__filename

    @file.setter
    def file(self, name):
        self.__filename = name

    def insert(self, data):
        with open(self.file, "r", encoding='utf-8') as f:
            file_data = json.load(f)
        file_data.append(data)
        with open(self.file, "w", encoding='utf-8') as f:
            json.dump(file_data, f)
