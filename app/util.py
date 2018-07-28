#!/usr/bin/env python

from flask import make_response
import pprint
import inspect


class Util:
    """ Set of useful functions available to the app """

    def print(variable, indent=6, width=1):
        """
        Generate a formatted output to any variable
        """
        if hasattr(variable, '__dict__'):
            print(pprint.pformat(vars(variable), indent=indent, width=width))
        else:
            pp = pprint.PrettyPrinter(indent=indent)
            pp.pprint(variable)

    def custom_make_response(text, code):
        """
        Custom response
        """
        response = make_response(text, code)
        response.headers['Content-Type'] = 'application/json'
        return response
