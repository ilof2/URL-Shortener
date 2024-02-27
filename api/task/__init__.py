BASE_ROUTE = "task"


def register_routes(api, root="api"):
    from api.task.controller import api as task_api
    api.add_namespace(task_api, path=f"/{root}/{BASE_ROUTE}")