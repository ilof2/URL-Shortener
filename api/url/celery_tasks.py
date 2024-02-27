import logging

from celery import shared_task

from .service import URLService
from api.task.models import StatusEnum as TaskStatus
from api.task.service import TaskService

logger = logging.getLogger()


@shared_task(ignore_result=False)
def get_short_url(url_id):
    task_service = TaskService()
    task = task_service.create_task()
    short_url_service = URLService()
    logger.info("url_id " + str(url_id))
    URL = short_url_service.get_by_id(url_id)
    logger.info(URL)
    if not URL:
        logger.error(f"ShortUrl with id {url_id} not found")
        task_service.update_status(task.id, TaskStatus.FAILED)
        return {
            "task_id": task.id,
            "status": TaskStatus.FAILED.value,
            "short_url_id": "",
            "original_url": ""
        }
    new_url = short_url_service.generate_new_url(URL.id)
    result = {
        "task_id": task.id,
        "status": TaskStatus.DONE.value,
        "short_url_id": new_url,
        "original_url": URL.old_url
    }
    task_service.update_status(task.id, TaskStatus.DONE)
    return result
