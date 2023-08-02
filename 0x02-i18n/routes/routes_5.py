#!/usr/bin/env python3
"""Basic route task 5"""
from typing import Union
from flask import Blueprint, render_template, g


app_routes = Blueprint('app_routes', __name__)


@app_routes.route('/', methods=["GET"], strict_slashes=False)
def home():
    """ Home page """
    return render_template('5-index.html', user=g.user)
