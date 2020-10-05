import json


class Config:

    def __init__(self, path='./config.json'):
        self.path = path

        with open(self.path, 'r', errors='ignore', encoding='UTF-8') as file:
            content = file.read()

        config = json.loads(content)

        for k, v in config.items():
            self.__setattr__(k, v)

    def __getattr__(self, item: object) -> object:
        return self.get(item)
