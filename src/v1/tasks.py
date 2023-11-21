from __future__ import absolute_import, unicode_literals
from celery import shared_task
from v1.redis_manager import redis_manager
import v1.jisilu_data as JisiluData

@shared_task
def my_task():
    print("This is a task.")
    
    
@shared_task
def download_and_save_data():
    print('download_and_save_data')
    

@shared_task
def slow_task():
    print('slow_task')
    JisiluData.update_basic_bonds()
    print('slow_task')