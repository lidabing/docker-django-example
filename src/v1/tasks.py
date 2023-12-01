from __future__ import absolute_import
from __future__ import unicode_literals

from celery import shared_task

import v1.jisilu_data as JisiluData
from v1.redis_manager import redis_manager


@shared_task
def my_task():
    print("This is a task.")


@shared_task
def download_and_save_data():
    print("download_and_save_data")


@shared_task
def slow_task():
    print("slow_task")
    JisiluData.update_basic_bonds()
    JisiluData.update_upcoming_bonds()
    JisiluData.update_upcoming_adjust_bonds()
    JisiluData.update_proposed_adjust_bonds()
    JisiluData.update_upcoming_adjust_condition_bonds()
    JisiluData.update_expired_bonds()
    JisiluData.update_expired_bonds()
    print("slow_task")
