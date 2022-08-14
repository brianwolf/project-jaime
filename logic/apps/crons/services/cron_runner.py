import threading
import time

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from logic.apps.crons.models.cron_model import CronStatus
from logic.apps.crons.services import cron_service
from logic.libs.logger.logger import logger

_THREAD_ACTIVE = True

_SCHEDULER = BlockingScheduler()


def add_new_jobs():
    try:
        for id in cron_service.list_by_status(CronStatus.ACTIVE):

            cron = cron_service.get(id)

            global _SCHEDULER
            _SCHEDULER.add_job(
                func=cron_service.exec(cron),
                trigger=CronTrigger.from_crontab(cron.cron_expression)
            )

    except Exception as e:
        logger().error(e)


def start_threads():

    logger().info('Iniciando hilo -> crons')

    def thread_scheduler_method():
        global _SCHEDULER
        _SCHEDULER.start()

    thread_scheduler = threading.Thread(target=thread_scheduler_method)
    thread_scheduler.start()

    global _THREAD_ACTIVE
    _THREAD_ACTIVE = True

    def thread_add_job_method():
        global _THREAD_ACTIVE
        while _THREAD_ACTIVE:
            add_new_jobs()
            time.sleep(2)

    thread_add_jobs = threading.Thread(target=thread_add_job_method)
    thread_add_jobs.start()


def stop_threads():
    global _SCHEDULER, _THREAD_ACTIVE

    _SCHEDULER.shutdown()
    _SCHEDULER.remove_all_jobs()

    _THREAD_ACTIVE = False
