#!/usr/bin/env python3
""" Module for trying out Babel i18n """
from datetime import datetime
from flask_babel import Babel, _, format_datetime
import flask_babel
from flask import Flask, render_template, request, g
import pytz
from typing import Union

app = Flask(__name__, template_folder='templates')
babel = Babel(app)


class Config(object):
    """ Configuration Class for Babel """

    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> Union[dict, None]:
    """ Returns a user dictionary or
    None if the ID cannot be found or
    if login_as was not passed.
    """

    try:
        login_as = request.args.get("login_as")
        user = users[int(login_as)]
    except Exception:
        user = None

    return user


@app.before_request
def before_request():
    """ Operations that happen before any request """
    user = get_user()
    g.user = user


@app.route('/', methods=['GET'], strict_slashes=False)
def hello_world() -> str:
    """Renders a Basic Template for Babel Implementation"""
    timezone = get_timezone()
    tz = pytz.timezone(timezone)
    current_time = datetime.now(tz)
    current_time = format_datetime(datetime=current_time)
    return render_template("index.html", current_time=current_time)


@babel.localeselector
def get_locale() -> str:
    """Select a language translation to use for that request"""
    locale = request.args.get("locale")
    if locale and locale in app.config['LANGUAGES']:
        return locale

    if g.user:
        locale = g.user.get("locale")
        if locale and locale in app.config['LANGUAGES']:
            return locale

    locale = request.headers.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale

    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone() -> str:
    """
    1 Find timezone parameter in URL parameters
    2 Find time zone from user settings
    3 Default to UTC
    """
    try:
        if request.args.get("timezone"):
            timezone = request.args.get("timezone")
            tz = pytz.timezone(timezone)

        elif g.user and g.user.get("timezone"):
            timezone = g.user.get("timezone")
            tz = pytz.timezone(timezone)
        else:
            timezone = app.config["BABEL_DEFAULT_TIMEZONE"]
            tz = pytz.timezone(timezone)

    except pytz.exceptions.UnknownTimeZoneError:
        timezone = "UTC"

    return timezone


if __name__ == "__main__":
    app.run()
