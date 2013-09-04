# coding: utf-8
'''
This file is for configuration storage
To override configurations, simply create siteconfig.py file,
and define your overrides in "config" dictionary
'''

import os
import web

config = web.storage(
    environment='development',
    asset_version='v00',
    database=dict(dbn='sqlite', db='db.sqlite'),
)

try:
    import siteconfig
    config.update(siteconfig.config)
except ImportError:
    pass

# Set directories
config.rootdir = os.path.abspath(os.path.dirname(__file__))
config.update(
    static_dir=config.get('static_dir', config.rootdir + '/static'),
    template_dir=config.get('templates_dir', config.rootdir + '/templates'),
)


# Update config based on current environment
if os.environ.get('WEBPY_ENV') == 'test':
    config.environment = 'test'

if config.environment == 'test':
    web.config.debug = False
    web.config.debug_sql = False
else:
    if config.environment == 'development':
        web.config.debug = True
        web.config.debug_sql = True
    elif config.environment == 'production':
        web.config.debug = False
        web.config.debug_sql = False
