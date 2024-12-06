# -*- coding: utf-8; -*-
"""
Wutta Demo config extensions
"""

from wuttjamaican.conf import WuttaConfigExtension


class WuttaDemoConfig(WuttaConfigExtension):
    """
    Config extension for Wutta Demo
    """
    key = 'wuttademo'

    def configure(self, config):

        # app info
        config.setdefault(f'{config.appname}.app_title', "Wutta Demo")
        config.setdefault(f'{config.appname}.app_dist', "Wutta-Demo")

        # app model
        config.setdefault(f'{config.appname}.model_spec', 'wuttademo.db.model')

        # web app menu
        config.setdefault(f'{config.appname}.web.menus.handler_spec',
                          'wuttademo.web.menus:WuttaDemoMenuHandler')

        # web app libcache
        #config.setdefault('tailbone.static_libcache.module', 'wuttademo.web.static')
