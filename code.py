#!/usr/bin/env python
'''
This is the main executable file
that runs application in development server or wsgi mode
'''


import os
import sys
import web
from config import config
from urls import urls
from template import render

# Add current directory to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# App initialization
app = web.application(urls, globals())

# Database initialization
db = web.database(**config.database)

# Session initialization
if web.config.get('_session') is None:
    # this is required to work with reloader
    web.config._session = web.session.Session(
        app,
        web.session.DBStore(db, 'sessions'),
    )


# Save session and db in web.ctx
def ctx_hook():
    web.ctx.session = web.config._session
    web.ctx.db = db

app.add_processor(web.loadhook(ctx_hook))

app.notfound = lambda: web.notfound(render.error(404, 'Not Found'))

# Custom error pages in production
if config.environment == 'production':
    app.internalerror = lambda: web.internalerror(
        render.error(500, 'Internal Server Error'))


if __name__ == '__main__':
    if config.environment != 'test':
        app.run()
else:
    application = app.wsgifunc()
