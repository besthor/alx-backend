#!/usr/bin/env python3
""" 2-app module """
from flask import Flask, request
from flask_babel import Babel
from routes.routes_2 import app_routes
from config import Config


app = Flask(__name__)
babel = Babel(app)

app.config.from_object(Config)
app.register_blueprint(app_routes)


@babel.localeselector
def get_locale() -> str:
    """ Determine best match for supported languages
    """
    return request.accept_languages.best_match(Config.LANGUAGES)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
