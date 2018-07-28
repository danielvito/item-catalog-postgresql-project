#!/usr/bin/env python

from app import app, db
from app.models import User, Brand, Category, CategoryItem


@app.shell_context_processor
def make_shell_context():
    """
    Enable shell command for the application with the following variables
    """
    return {'db': db, 'User': User, 'Brand': Brand, 'Category': Category,
            'CategoryItem': CategoryItem}
