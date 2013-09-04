# coding: utf-8
"""
Provides helper methods to templates
"""
import web
from config import config


template_globals = {'config': config, 'ctx': web.ctx}


class template_global(object):
    '''Decorator to register func to use in templates'''

    def __init__(self, f):
        self.f = template_globals[f.__name__] = f

    def __call__(self, *k, **kw):
        return self.f(*k, **kw)


@template_global
def asset_url(filename, with_version=True):
    '''Returns link to static file'''
    if filename.startswith('http') or filename.startswith('/'):
        return filename
    else:
        if 'static_url' in config:
            return_url = 'http://' + config.static_url
        else:
            return_url = '/static'
        return_url += '/' + filename
        if with_version:
            return_url += '?' + config.asset_version
        return return_url


# Renders without layout
render_partial = web.template.render(config.template_dir,
                                     globals=template_globals)
template_globals.update(render=render_partial)

# Renders with layout
render = web.template.render(config.template_dir,
                             globals=template_globals,
                             base='layout')
