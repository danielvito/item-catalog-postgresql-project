#!/usr/bin/env python

from flask_babel import _
import os
basedir = os.path.abspath(os.path.dirname(__file__))

POSTGRES = {
    'user': 'catalog',
    'pw': 'catalog',
    'db': 'catalog',
    'host': 'localhost',
    'port': '5432',
}


class Config(object):
    """ App configuration """
    CLIENT_SECRET_JSON = os.path.join(basedir, 'client_secrets.json')
    LANGUAGES = ['en', 'es']
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES  # noqa
    SQLALCHEMY_TRACK_MODIFICATIONS = True
