
def register_routes(api, root="api"):
    from api.url import register_routes as attach_url_api
    from api.task import register_routes as attach_task_api

    attach_url_api(api, root)
    attach_task_api(api, root)
