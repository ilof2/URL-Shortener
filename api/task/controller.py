from flask import url_for
from flask_restx.utils import HTTPStatus
from flask_restx import abort
from flask_restx import Namespace, Resource
from celery.result import AsyncResult, states

from api.task.service import TaskService

api = Namespace("Task")


@api.route("/getResult/<string:result_id>")
class CalculateDistance(Resource):
    def get(self, result_id):

        task = TaskService.get_task_by_result_id(result_id)
        if not task:
            return abort(HTTPStatus.NOT_FOUND, custom="Task not found")

        empty_result = {
            "task_id": task.id,
            "status": task.status.value,
            "original_url": "",
            "short_url": ""
        }
        celery_result = AsyncResult(result_id)
        if celery_result.status != states.SUCCESS:
            return empty_result
        celery_result_data = celery_result.get()
        if not isinstance(celery_result_data, dict):
            return empty_result
        if short_url := celery_result_data.get("short_url_id"):
            celery_result_data["short_url"] = url_for("index", url_id=short_url, _external=True)
        return celery_result_data
