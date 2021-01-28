# from apscheduler.schedulers.background import BackgroundScheduler
from celery import shared_task

from .models import Post


@shared_task
def reset_upvotes():
    Post.reset_upvotes()


# def start():
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(Post.reset_upvotes, "interval", days=1)
#     scheduler.start()
