import gettext
import logging
import os
import simplejson as json
import web
from web import utils
from web.contrib import template

import configuration
import utils as my_utils


_test_mode = False
urls = ( '/', 'GenericPage',
        r'/(css|js|img)/(.*)', 'StaticFile',
         '/favicon.ico', 'StaticFavicon',
         '/ajax/load-rules', 'AjaxLoadRules')
app = web.application(urls, globals())
base_render = template.render_jinja(
    'templates', extensions = ['jinja2.ext.i18n'], encoding = 'utf-8',
    globals = {
       # TODO: Put a good default title and description
       'head_title': gettext.gettext('Crafe - Find a home'),
       'head_description': gettext.gettext('Description of Crafe'),
       'js_srcs': ['http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js', '/js/index.js'],
       'css_srcs': ['/css/screen.css'],
       'version': configuration.STATIC_CONTENT_VERSION,
    })

# TODO: This doesn't work if it gets in a function (?!)
# Used for Jinja2 i18n extension.
curdir = os.path.abspath(os.path.dirname(__file__))
localedir = os.path.join(curdir, 'i18n')
# TODO: Choose the right language based on cookies / Accept-Language
lang = gettext.translation('messages', localedir, languages=['en_US'])
base_render._lookup.install_gettext_translations(lang)


class GenericPage:
    """Renders a page that uses base_render template."""

    def GET(self, page_name='index'):
        web.header('Content-Type', 'text/html')
        return getattr(base_render, page_name)({'page_name': page_name})


class StaticFile:
    """Serve a static file.

    This method should not be used in production, you should instead serve the
    file from the frontend webserver (nginx). It's however useful to emulate
    this for development without nginx.

    TODO: It can be very useful to plug here a JS compiler and a CSS compressor
    and let nginx do caching of these files. For that I need to find a python
    JS / CSS compressor and add some Cache headers.
    """

    def GET(self, dirname, filename):
        supported_content_types = {
            'css': 'text/css',
            'js': 'text/javascript',
            'ico': 'image/ico',
            'png': 'image/png',
            'jpg': 'image/jpeg',
            'gif': 'image/gif',
        }
        content_type = supported_content_types.get(
            my_utils.get_extension(filename), 'application/octet-stream')
        web.header('Content-Type', content_type)
        return open(os.path.join('static', dirname, filename), 'rb').read()


class StaticFavicon(StaticFile):
    def GET(self):
        return StaticFile.GET(self, 'img', 'favicon.ico')


class AjaxLoadRules:
    def GET(self):
        user_data = web.input()
        if 'name' not in user_data:
            raise utils.BadRequest()

        name = my_utils.safestr(user_data['name'])
        web.header('Content-Type', 'application/json')
        return json.dumps({'address': 'address of %s' % name, 'description': 'Nice flat'})


def set_test_mode(test_mode=True):
    _test_mode = test_mode


def is_test():
    """Returns True if we are in a testing environment.

    We can't detect if we're in a test environment using
    web.ctx.env['paste.testing'] because we want to know if we're in a test
    environment before we start a web server (to accelerate the tests).
    """
    return _test_mode


if (not is_test()) and __name__ == "__main__":
    app.run()
