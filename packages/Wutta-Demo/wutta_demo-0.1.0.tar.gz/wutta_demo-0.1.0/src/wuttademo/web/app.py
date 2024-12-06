# -*- coding: utf-8; -*-
"""
Wutta Demo web app
"""

from wuttaweb import app as base


def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    # prefer Wutta Demo templates over wuttaweb
    settings.setdefault('mako.directories', [
        'wuttademo.web:templates',
        'wuttaweb:templates',
    ])

    # make config objects
    wutta_config = base.make_wutta_config(settings)
    pyramid_config = base.make_pyramid_config(settings)

    # bring in the rest of Wutta Demo
    pyramid_config.include('wuttademo.web.static')
    pyramid_config.include('wuttademo.web.subscribers')
    pyramid_config.include('wuttademo.web.views')

    return pyramid_config.make_wsgi_app()
