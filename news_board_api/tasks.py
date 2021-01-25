from apscheduler.schedulers.background import BackgroundScheduler

from .models import Post


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(Post.reset_upvotes, "interval", days=1)
    scheduler.start()
