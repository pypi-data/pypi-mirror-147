"""
Theme

"""

from . import ext

theme = ext.Theme()

def init_app(app):

    from . import constants

    for k in dir(constants):
        if k.upper() == k:
            default = getattr(constants, k)
            app.config.setdefault(k, default)

    theme.init_app(app)
