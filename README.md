# Discord Webhook Protection

 A simple Discord webhook REST API using Flask to protect Discord webhook URLs to prevent people from abusing it (spamming, deleting etc.).

## Usage

Instead of hardcoding your webhook URL in your applications and sending a lot of HTTP requests using the token in i.e. token grabbers, you can set up a webserver running this API that will do it all for you, while not exposing your webhook URL.

The API will validate and send the token information over the webhook URL provided in `config.json` .

To create new API endpoints, create a new Python file in directory `routes` and import it in `routes\__init__.py` under the line `# import here` .

## Requirements

* Python 3
* Git (optional)
* Server to host API

## Installation

1. Install repository via `$ git clone https://github.com/ecriminal/Webhook-Protection.git`
2. Install required modules using `$ pip install -r requirements.txt`
3. Edit `config.json` file
4. Start webserver via `$ py main.py`

## TODO

* Set up a MySQL database to store tokens, used to prevent dupes
* IP-address based rate limit to prevent abusers from flooding the API
