from django.apps import AppConfig
import redis


class V1Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'v1'

    def ready(self):
        r = redis.Redis(host='convertible_bond-redis-1', port=6379, db=0)  # 你的 Redis 服务器地址
        # 尝试获取锁
        if r.setnx('ready_executed_v1', 1):
            from .tasks import slow_task
            # 设置锁的过期时间为 120 秒，防止死锁
            r.expire('ready_executed_v1', 120)

            print("V1Config ready")
            slow_task.apply_async()