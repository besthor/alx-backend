#!/usr/bin/env python3
""" 4-app module """
from flask import Flask, request, g
from typing import Union
from flask import Flask, request
from flask_babel import Babel
from config import Config
from routes.routes_5 import app_routes


app = Flask(__name__)
babel = Babel(app)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

app.config.from_object(Config)
app.register_blueprint(app_routes)


@babel.localeselector
def get_locale() -> Union[str, None]:
    """ get locale
    """
    locale = request.args.get('locale')
    if locale and locale in Config.LANGUAGES:
        return locale
    return request.accept_languages.best_match(Config.LANGUAGES)


def get_user() -> Union[dict, None]:
    """get user"""
    try:
        return users.get(int(request.args.get('login_as')))
    except Exception:
        return None


@app.before_request
def before_request():
    """ before request
    """
    g.user = get_user()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080")
