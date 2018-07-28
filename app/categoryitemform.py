#!/usr/bin/env python

from wtforms import Form, TextAreaField, BooleanField, StringField, \
    PasswordField, SelectField, DecimalField, validators
from flask_babel import _


class CategoryItemForm(Form):
    """ Fields map for category item form """
    name = StringField(_('name'), [validators.Length(min=4, max=25)])
    description = TextAreaField(_('description'),
                                [validators.Length(min=4, max=255)])
    price = StringField(_('price'), [validators.DataRequired()])
    category_id = SelectField(_('category'), [validators.DataRequired()],
                              coerce=int)
    brand_id = SelectField(_('brand'), [validators.DataRequired()],
                           coerce=int)
