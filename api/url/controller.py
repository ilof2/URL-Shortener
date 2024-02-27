from flask_restx import Namespace, Resource

from api import db
from api.url.service import URLService
from api.url.celery_tasks import get_short_url
from api.task.service import TaskService

api = Namespace("URL")
url_parser = api.parser()
url_parser.add_argument('url', location='args', type=str, required=True)


@api.route("/")
class GenerateShortUrl(Resource):

    @api.expect(url_parser)
    def post(self):
        args = url_parser.parse_args()
        url = args['url']
        if url.find("http://") != 0 and url.find("https://") != 0:
            url = "http://" + url

        result = {
            "result_id": None
        }
        with db.session.begin():
            task_service = TaskService(autocommit=False, session=db.session)
            url_service = URLService(autocommit=False, session=db.session)

            url_object = url_service.get_by_old_url(url)
            if url_object:
                result["result_id"] = url_object.task.result_id
                return result
            task = task_service.create_task()
            url_object = url_service.create(url, task.id)
            celery_result = get_short_url.delay(url_object.id)
            task.result_id = celery_result.id

        result["result_id"] = celery_result.id
        return result
