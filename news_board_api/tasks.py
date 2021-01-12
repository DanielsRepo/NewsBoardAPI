from apscheduler.schedulers.background import BackgroundScheduler

from .models import Post


def reset_post_upvotes():
    print("Resetting post upvotes count...")

    for post in Post.objects.all():
        post.upvotes_amount = 0
        post.save()

    print("Post upvotes count has been reseted")


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(reset_post_upvotes, "interval", days=1)
    scheduler.start()
