import os
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_board.settings")

app = Celery("news_board")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "reset_upvotes": {
        "task": "news_board_api.tasks.reset_upvotes",
        "schedule": crontab(minute=0, hour=0),
    },
}
