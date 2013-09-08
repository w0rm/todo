# coding: utf-8
'''
This file is for configuration storage
To override configurations, simply create siteconfig.py file,
and define your overrides in "config" dictionary
'''

import os
import web
import urlparse

# Default config
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

# Update database from os.environ
if 'DATABASE_URL' in os.environ:
    url = urlparse.urlparse(os.environ['DATABASE_URL'])
    config.database = dict(
        dbn=url.scheme,
        user=url.username,
        db=url.path[1:],
        password=url.password,
        host=url.hostname,
        port=url.port,
    )

# Update environment from os.environ
if 'WEBPY_ENV' in os.environ:
    config.environment = os.environ['WEBPY_ENV']


# Set directories
config.rootdir = os.path.abspath(os.path.dirname(__file__))
config.update(
    static_dir=config.get('static_dir', config.rootdir + '/static'),
    template_dir=config.get('templates_dir', config.rootdir + '/templates'),
)


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
