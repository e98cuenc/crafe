import controller
from nose import tools
from paste import fixture


def setup():
    controller.set_test_mode()

def teardown():
    pass

def test_index():
    middleware = []
    app = fixture.TestApp(controller.app.wsgifunc(*middleware))
    r = app.get('/')
    tools.assert_equal(r.status, 200)
    # r.mustcontain('foo')
