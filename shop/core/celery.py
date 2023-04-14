import os

from celery import Celery

if os.path.exists('celerybeat-schedule'):
    os.remove('celerybeat-schedule')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'sync_store_to_shop': {
        'task': 'shop.task.update_books',
        'schedule': 180.0,
    },
    'sync_to_shop': {
        'task': 'shop.task.update_authors',
        'schedule': 180.0,
    },
    'check_order_statuses': {
        'task': 'shop.task.check_order_statuses',
        'schedule': 180.0,
    },

}
