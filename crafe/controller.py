import gettext
import web
import os
from web.contrib.template import render_jinja

import configuration

urls = ( '/', 'GenericPage',
        r'/(css|js|img)/(.*)', 'StaticFile',
        r'/favicon.ico', 'StaticFavicon')

app = web.application(urls, globals())
base_render = render_jinja('templates', extensions = ['jinja2.ext.i18n'],
                           encoding = 'utf-8',
                           globals = {
                               # TODO: Put a good default title and description
                               'head_title': _('Crafe - Find a home'),
                               'head_description': _('Description of Crafe'),
                               'js_srcs': [],
                               'css_srcs': [],
                               'version': configuration.STATIC_CONTENT_VERSION,
                           })

# Used for Jinja2 i18n extension.
curdir = os.path.abspath(os.path.dirname(__file__))
localedir = os.path.join(curdir, 'i18n')
# TODO: Choose the right language based on cookies / Accept-Language
lang = gettext.translation('messages', localedir, languages=['en_US'])
base_render._lookup.install_gettext_translations(lang)


class GenericPage:
    """Renders a page that uses base_render template."""

    def GET(self, page_name='index'):
        return getattr(base_render, page_name)({'page_name': page_name})


class StaticFile:
    """Serve a static file.
    
    This method should not be used in production, you should instead serve the
    file from the frontend webserver (nginx). It's however useful to emulate
    this for development without nginx.
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
        content_type = 'application/octet-stream'
        dot_position = filename.rfind('.')
        if dot_position >= 0:
            file_extension = filename[dot_position + 1:]
            if file_extension in supported_content_types:
                content_type = supported_content_types[file_extension]

        web.header('Content-Type', content_type)
        return open(os.path.join('static', dirname, filename), 'rb').read()


class StaticFavicon(StaticFile):
    def GET(self):
        return StaticFile.GET(self, 'img', 'favicon.ico')


if __name__ == "__main__":
    app.run()
