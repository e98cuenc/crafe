import controller
from nose import tools
from paste import fixture
import logging


def setup():
    controller.set_test_mode()

def teardown():
    pass

def test_index():
    app = fixture.TestApp(controller.app.wsgifunc())
    r = app.get('/')
    tools.assert_equal(r.status, 200)
    tools.assert_equal(r.header('Content-Type'), 'text/html')
    # r.mustcontain('foo')

def test_css():
    app = fixture.TestApp(controller.app.wsgifunc())
    for css_url in ['/css/screen.css']:
        r = app.get(css_url)
        tools.assert_equal(r.status, 200)
        tools.assert_equal(r.header('Content-Type'), 'text/css')

def test_js():
    app = fixture.TestApp(controller.app.wsgifunc())
    for js_url in ['/js/index.js']:
        r = app.get(js_url)
        tools.assert_equal(r.status, 200)
        tools.assert_equal(r.header('Content-Type'), 'text/javascript')
