from apscheduler.schedulers.background import BackgroundScheduler

from .models import Post


def reset_post_upvotes():
    print("Resetting post upvotes count...")

    Post.objects.all().update(upvotes_amount=0)

    print("Post upvotes count has been reseted")


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(reset_post_upvotes, "interval", seconds=5)
    scheduler.start()
