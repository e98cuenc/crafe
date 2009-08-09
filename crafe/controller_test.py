import logging
from nose import tools
from paste import fixture
import simplejson as json

import controller
from server import testing


app = None

def setup():
    global app
    controller.start_application('test')
    app = fixture.TestApp(controller.app.wsgifunc())

def test_index():
    r = app.get('/')
    testing.parse_http_response(r, 'text/html')
    # r.mustcontain('foo')

def test_css():
    for css_url in ['/css/screen.css']:
        r = app.get(css_url)
        testing.parse_http_response(r, 'text/css')

def test_js():
    for js_url in ['/js/index.js']:
        r = app.get(js_url)
        testing.parse_http_response(r, 'text/javascript')

def test_ajax():
    ajax_urls = ['/ajax/load-rules?name=loquo']
    for ajax_url in ajax_urls:
        r = app.get(ajax_url)
        testing.parse_http_response(r, 'application/json')

def test_ajax_load_rules():
    r = app.get('/ajax/load-rules?name=loquo')
    json = testing.parse_http_response(r, 'application/json')
    tools.assert_equal(json['name'], 'loquo')
