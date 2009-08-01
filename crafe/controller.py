import gettext
import web
import os
from web.contrib.template import render_jinja

urls = ( '/', 'GenericPage',
        r'/(hello)', 'GenericPage',)

app = web.application(urls, globals())
base_render = render_jinja('templates', extensions = ['jinja2.ext.i18n'],
                           encoding = 'utf-8',
                           globals = {
                               # TODO: Put a good default title and description
                               'head_title': _('Crafe - Find a home'),
                               'head_description': _('Description of Crafe'),
                               'js_srcs': [],
                               'css_srcs': [],
                           })

# Used for Jinja2 i18n extension.
curdir = os.path.abspath(os.path.dirname(__file__))
localedir = curdir + '/i18n'
# TODO: Choose the right language based on cookies / Accept-Language
lang = gettext.translation('messages', localedir, languages=['en_US'])
base_render._lookup.install_gettext_translations(lang)


class GenericPage:
    def GET(self, page_name='index'):
        return getattr(base_render, page_name)({'page_name': page_name})


if __name__ == "__main__":
    app.run()
