from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.mail import send_mail,BadHeaderError

logger = get_task_logger(__name__)

@shared_task
def send_verification_email(subject, message,from_email, to_email):
    try:
        send_mail(subject, message, from_email, [to_email])
    except BadHeaderError:
        logger.info('Invalid header found')
    except Exception as e:
        logger.info(e)