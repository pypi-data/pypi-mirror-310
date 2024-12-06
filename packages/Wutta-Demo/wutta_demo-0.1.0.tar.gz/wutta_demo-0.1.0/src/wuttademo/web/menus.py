# -*- coding: utf-8; -*-
"""
Wutta Demo Menu
"""

from wuttaweb import menus as base


class WuttaDemoMenuHandler(base.MenuHandler):
    """
    Wutta Demo menu handler
    """

    def make_menus(self, request, **kwargs):

        # TODO: override this if you need custom menus...

        # menus = [
        #     self.make_products_menu(request),
        #     self.make_admin_menu(request),
        # ]

        # ...but for now this uses default menus
        menus = super().make_menus(request, **kwargs)

        return menus
