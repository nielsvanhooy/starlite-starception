from starlite import Starlite, TestClient, get

from starlite_starception import StarceptionMiddleware
from starlite_starception.exception_handler import install_error_handler


@get("/")
def view() -> None:
    raise TypeError('Oops')


debug_app = Starlite(
    debug=True,
    route_handlers=[view],
    middleware=[StarceptionMiddleware])

release_app = Starlite(
    debug=False,
    route_handlers=[view],
    middleware=[StarceptionMiddleware])

no_middleware_debug_app = Starlite(
    debug=True,
    route_handlers=[view],
)

no_middleware_release_app = Starlite(
    debug=False,
    route_handlers=[view],
)


def test_middleware_renders_html_page_in_debug_mode() -> None:
    client = TestClient(debug_app, raise_server_exceptions=False)
    response = client.get('/', headers={'accept': 'text/html'})
    assert '<body>' in response.text
    assert 'Oops' in response.text


def test_middleware_renders_html_page_with_handler_installed_in_debug_mode() -> None:
    install_error_handler()
    client = TestClient(no_middleware_debug_app, raise_server_exceptions=False)
    response = client.get('/', headers={'accept': 'text/html'})
    assert '<body>' in response.text
    assert 'Oops' in response.text


def test_middleware_renders_plain_text_page_with_handler_installed_in_release_mode() -> None:
    install_error_handler()
    client = TestClient(no_middleware_release_app, raise_server_exceptions=False)
    response = client.get('/', headers={'accept': 'text/html'})
    assert 'Internal Server Error' in response.text


def test_middleware_renders_plain_text_page_in_debug_mode_for_non_html() -> None:
    client = TestClient(debug_app, raise_server_exceptions=False)
    response = client.get('/', headers={'accept': 'text/plain'})
    assert '<body>' not in response.text
    assert 'Oops' in response.text


def test_middleware_renders_plain_text_in_release_mode() -> None:
    client = TestClient(release_app, raise_server_exceptions=False)
    response = client.get('/', headers={'accept': 'text/html'})
    assert 'Internal Server Error' in response.text
