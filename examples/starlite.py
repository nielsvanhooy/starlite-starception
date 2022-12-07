from starlite import Starlite, get

from starlite_starception import StarceptionMiddleware


@get("/")  # type: ignore
def view() -> None:
    raise TypeError('Oops')


app = Starlite(debug=True, route_handlers=[view], middleware=[StarceptionMiddleware])
