import requests


class AuthenticationError(Exception):
    """ AuthenticationError raised when an error occcures while authenticating user.

    AuthenticationError Exception is raised,
    when an error occurrs in the Discord JSON API response,
    when trying to authenticate user through
    authorization token.

    Args:
        Exception (str, str, int): authorization token, API response, HTTP response code
    """
    pass


class DiscordUser:

    def __init__(self, token, auth=True):
        self.token = token
        self.headers = {
            'Authorization': self.token,
            'Content-Type': 'application/json'
        }

        if auth:
            self.authenticate()

    def authenticate(self) -> None:
        """ Authenticate user.

        Authenticates user through the authorization token
        and as sets object attributes from the JSON API response body.

        Raises:
            AuthenticationError: if an error occurs while trying to authenticate user
        """
        res = requests.get('https://discordapp.com/api/v8/users/@me', headers=self.headers)

        if res.status_code != 200:
            raise AuthenticationError(self.token, res.text, res.status_code)

        for k, v in res.json().items():
            self.__setattr__(k, v)

    def __getattr__(self, item: object) -> object:
        return self[item]
