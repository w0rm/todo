#!/usr/bin/env python
'''
This is the main executable file
that runs application in development server or wsgi mode
'''

# Add current directory to path
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import web
from config import config
from urls import urls


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

# Custom error pages in production
if config.environment == 'production':
    import template
    app.internalerror = lambda: web.internalerror(template.render.error(500))
    app.notfound = lambda: web.notfound(template.render.error(404))

if __name__ == '__main__':
    if config.environment != 'test':
        app.run()
else:
    application = app.wsgifunc()
