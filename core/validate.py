import re
import base64

from core.discord.utils import DISCORD_EPOCH, snowflake_epoch


class Validate:

    @staticmethod
    def token(token: str) -> bool:
        """ Validate Discord authorization token

        Validates Discord authorization token
        by debunking it using regex string matching and
        b64 snowflake to epoch parsing and validation.

        Args:
            token (str): token to validate

        Returns:
            bool: token is valid
        """
        regex = re.match(r'^[\w-]{24}\.[\w-]{6}\.[\w-]{27}|mfa\.[\w-]{84}$', token)

        if regex is None:
            return False

        if token.startswith('mfa') is False:
            b64_snowflake = token.split('.')[0]

            try:
                snowflake = base64.b64decode(b64_snowflake.encode()).decode()
            except Exception:
                return False

            if snowflake.isdigit() is False:
                return False

            created_at_epoch = snowflake_epoch(int(snowflake))

            if created_at_epoch < DISCORD_EPOCH:
                return False

        return True
