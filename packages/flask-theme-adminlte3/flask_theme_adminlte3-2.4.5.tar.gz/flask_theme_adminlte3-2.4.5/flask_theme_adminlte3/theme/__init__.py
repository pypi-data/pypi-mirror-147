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
            if app.config['THEME_CONFIG_DEBUG'] == True:
                app.logger.debug(f'Setting Theme default {k} = {default}')
            app.config.setdefault(k, default)
        
    theme.init_app(app)
