import requests


class InvalidToken(Exception):
    pass


class DiscordUser:

    def __init__(self, token):
        self.token = token
        self.headers = {
            'Authorization': self.token,
            'Content-Type': 'application/json'
        }

        res = requests.get('https://discordapp.com/api/v8/users/@me', headers=self.headers)
        
        if res.status_code != 200:
            raise InvalidToken('Invalid token \'%s\'' % self.token)

        for k, v in res.json().items():
            self.__setattr__(k, v)

    def __getattr__(self, item: object) -> object:
        return self[item]
