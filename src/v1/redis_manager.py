import redis
import json

class RedisManager:
    def __init__(self, host='convertible_bond-redis-1', port = 6379, db = 0):
        self.r = redis.Redis(host=host, port=port, db=db)

    def set_data(self, key, data):
        data_str = json.dumps(data,ensure_ascii=False)
        self.r.set(key, data_str.encode('utf-8'))

    def get_data(self, key):
        data_str = self.r.get(key)
        if data_str:
            return json.loads(data_str)
        else:
            return None
        

# 创建一个 RedisManager 的实例
redis_manager = RedisManager()