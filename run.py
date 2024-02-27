from api import create_app
from api.extensions import celery_init_app


app = create_app()
celery = celery_init_app(app)
