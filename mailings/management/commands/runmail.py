import pytz
from django.core.mail import send_mail
from datetime import datetime, timedelta
from smtplib import SMTPException
from mailings.models import Mail, Log

import logging
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

logger = logging.getLogger(__name__)


def change_status(mail, timenow):
    if mail.status == 'CREATED':
        mail.status = 'STARTED'
        print('STARTED')
    elif mail.status == 'STARTED' and mail.end_time_last <= timenow:
        mail.status = 'COMPLETED'
        print('COMPLETED')
    mail.save()


def change_start_time(mail, time):
    if mail.start_time < time:
        if mail.period == '"DAILY"':
            mail.start_time += timedelta(days=1)
            print(mail.start_time)
        elif mail.period == 'WEEKLY':
            mail.start_time += timedelta(days=7)
        elif mail.period == 'MONTHLY':
            mail.start_time += timedelta(days=30)
        mail.save()


def my_job():
    print("Запущена рассылка")
    time_now = datetime.now(pytz.timezone(settings.TIME_ZONE))
    mails = Mail.objects.filter(mail_active=True)

    if mails:
        for mail in mails:
            change_status(mail, time_now)
            if mail.start_time <= time_now <= mail.end_time_last:
                for client in mail.clients.all():
                    try:
                        response = send_mail(
                            subject=mail.content.title,
                            message=mail.content.content,
                            from_email=settings.EMAIL_HOST_USER,
                            recipient_list=[client.email],
                            fail_silently=False
                        )
                        log = Log.objects.create(
                            last_attempt=time_now,
                            status='SUCCESS',
                            server_response=response,
                            mail=mail,
                            client=client,
                            owner=mail.owner
                        )
                        log.save()
                        print("log сохранен")
                        change_start_time(mail, time_now)
                    except SMTPException as e:
                        log = Log.objects.create(
                            last_attempt=time_now,
                            status='FAILED',
                            server_response=str(e),
                            mail=mail,
                            client=client,
                            owner=mail.owner
                        )
                        log.save()
                        print("Ошибка")
    else:
        print('Рассылок нет')


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(),"default")
        scheduler.add_job(my_job, trigger=CronTrigger(second="*/10"),  # Every 10 seconds
        id="my_job",
        max_instances=1,
        replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
        delete_old_job_executions,
        trigger=CronTrigger(
        day_of_week="mon", hour="00", minute="00"
        ), # Midnight on Monday, before start of the next work week.
        id="delete_old_job_executions",
        max_instances=1,
        replace_existing=True,
        )
        logger.info(
        "Added weekly job: 'delete_old_job_executions'."
         )
        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
