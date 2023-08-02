#!/usr/bin/env python3
""" 1-app module """
from flask import Flask
from flask_babel import Babel
from routes.routes_1 import app_routes


app = Flask(__name__)
babel = Babel(app)


class Config(object):
    """Config class for babel"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)
app.register_blueprint(app_routes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
