import logging
from uuid import uuid4

from .models import URL, db

logger = logging.getLogger()


class URLService:
    """URL operations"""
    def __init__(self, autocommit: bool = True, session=None):
        self.autocommit = autocommit
        self.session = session or db.session

    @staticmethod
    def get_by_id(url_id):
        return URL.query.filter_by(id=url_id).first()

    @staticmethod
    def get_by_old_url(old_url) -> URL | None:
        url_object = URL.query.filter_by(old_url=old_url).first()
        return url_object

    @staticmethod
    def _url_gen() -> str:
        """ You can change the URL generation algorithm on any you want """
        return str(uuid4())

    def generate_new_url(self, url_id: int):
        new = self._url_gen()
        URL.query.filter_by(id=url_id).update({"short_url": new})
        if self.autocommit:
            self.session.commit()
        return new


    def create(self, url: str, task_id: int):
        url_object = URL(old_url=url, task_id=task_id)
        self.session.add(url_object)
        self.session.flush()
        print(url_object.id)
        if self.autocommit:
            self.session.commit()
        return url_object
