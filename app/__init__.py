#!/usr/bin/env python

from flask import Flask, request, render_template, g
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
babel = Babel(app)
ma = Marshmallow(app)


from app import routes, models, categoryitemform, util  # noqa


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500
