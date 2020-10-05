import re


class Validate:

    @staticmethod
    def token(token: str, auth: bool = False) -> bool:
        """ Validate Disocrd token
        
        Validates Discord authorization token with
        regex string matching and authentication (optional).

        Args:
            token (str): token to validate
            auth (bool, optional): do authentication validation. Defaults to False.

        Returns:
            bool: token is valid
        """
        if re.match(r'^[\w-]{24}\.[\w-]{6}\.[\w-]{27}|mfa\.[\w-]{84}$', token) is None:
            return False

        # TODO: add auth validation
        if auth:
            pass

        return True
