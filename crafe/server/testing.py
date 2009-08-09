from nose import tools
import simplejson as json


def parse_http_response(http_response, expected_content_type=None):
    """Parses and validates an HTTP response.

    This function will run a linter on the HTTP content. The linter is chosen
    by the Content-Type in the HTTP response. It will raise an exception
    (dependent on the linter) if the response is not strictly valid.

    It also checks that the HTTP Status in the response is 200, and the
    Content-Type matches the expected_content_type.

    Args:
        http_response: (paste.fixtures.Response) HTTP response to parse.
        expected_content_type: (str) Expected Content-Type of the HTTP
            response.
    Returns:
        Object representing the parsed body in the HTTP response. The object
        returned depends on the Content-Type. It will be None if the body has
        not been parsed, either by an error or because we don't have a linter
        for this format.
    """
    linters = {
        'application/json': parse_json,
        'text/html': parse_html,
        'text/css': parse_css
    }
    tools.assert_equal(http_response.status, 200)
    if expected_content_type:
        tools.assert_equal(
            http_response.header('Content-Type'), expected_content_type)

    linter = linters.get(
        http_response.header('Content-Type'), parse_unknown_format)
    return linter(http_response.body)


def parse_unknown_format(text):
    return None


def parse_json(text):
    return json.loads(text)


def parse_html(text):
    # TODO: Add an HTML linter
    return None


def parse_css(text):
    # TODO: Add a CSS linter
    return None
