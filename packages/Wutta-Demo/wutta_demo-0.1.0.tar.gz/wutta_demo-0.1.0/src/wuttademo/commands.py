# -*- coding: utf-8; -*-
"""
Wutta Demo commands
"""

import typer

from wuttjamaican.cli import make_typer


wuttademo_typer = make_typer(
    name='wuttademo',
    help="Wutta Demo -- "
)


@wuttademo_typer.command()
def install(
        ctx: typer.Context,
):
    """
    Install the Wutta Demo app
    """
    config = ctx.parent.wutta_config
    app = config.get_app()
    install = app.get_install_handler(pkg_name='wuttademo',
                                      app_title="Wutta Demo",
                                      pypi_name='Wutta-Demo',
                                      egg_name='Wutta_Demo')
    install.run()
