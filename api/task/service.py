from .models import Task
from api import db


class TaskService:
    """Task operations"""
    def __init__(self, autocommit: bool = True, session=None):
        self.autocommit: bool = autocommit
        self.session = session or db.session

    def create_task(self):
        task = Task()
        self.session.add(task)
        self.session.flush()
        if self.autocommit:
            self.session.commit()
        return task

    @staticmethod
    def get_task_by_result_id(result_id) -> Task | None:
        return Task.query.filter_by(result_id=result_id).first()

    def update_status(self, task_id, status):
        Task.query.filter_by(id=task_id).update({"status": status})
        if self.autocommit:
            self.session.commit()
