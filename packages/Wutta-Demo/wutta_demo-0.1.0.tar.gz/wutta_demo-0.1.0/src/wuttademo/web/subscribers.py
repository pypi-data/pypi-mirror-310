# -*- coding: utf-8; -*-
"""
Pyramid event subscribers
"""

import wuttademo


def add_wuttademo_to_context(event):
    renderer_globals = event
    renderer_globals['wuttademo'] = wuttademo


def includeme(config):
    config.include('wuttaweb.subscribers')
    config.add_subscriber(add_wuttademo_to_context, 'pyramid.events.BeforeRender')
