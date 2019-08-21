from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from flightbooking.apps.flights.emails import send_reminder_email

logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(hour='*/24')),
    name="send_reminder_email_task",
    ignore_result=True)
def task_send_reminder_email():
    """sends an email when user books a flight"""
    send_reminder_email()
    logger.info("Sent reminder email")