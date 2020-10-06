from flask import Flask

from routes import routes

from core import config_object as config

def main():
    try:
        app = Flask(__name__)
        app.register_blueprint(routes)
        app.run(port=config.webserver_port, debug=False)
    except Exception as e:
        print(f'An error occurred: {e}')


if __name__ == '__main__':
    main()
