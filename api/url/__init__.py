BASE_ROUTE = "shorturl"


def register_routes(api, root="api"):
    from api.url.controller import api as url_api
    api.add_namespace(url_api, path=f"/{root}/{BASE_ROUTE}")
