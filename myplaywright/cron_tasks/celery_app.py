import os
from celery import Celery
from celery.schedules import crontab

import cron_tasks.tasks  # noqa


celery_app = Celery("crawler_cronjob", broker=os.getenv("CELERY_BROKER_URL"))

celery_app.conf.beat_schedule = {
    "crawl-staplesca-every-midnoon": {
        "task": "cron_tasks.tasks.crawl_staplesca.crawl_staplesca_task",
        "schedule": crontab(hour=12, minute=0),
    },
}
celery_app.conf.timezone = "UTC"
