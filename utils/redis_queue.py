# --*--coding:utf-8--*--
import redis_utils

config = {
    "vip_queue_name": "vip_queue",
    "queue_name": "queue"
}

loop_status = True
redis_queue_timeout = 0


class RedisQueue(object):
    def __init__(self):
        self.redis_conn = redis_utils.get_redis_conn()

    @property
    def get_queue(self):
        while loop_status:
            queue_content = self.redis_conn.blpop([config.get('vip_queue_name'), config.get('queue_name')], redis_queue_timeout)[1]
            print queue_content

    def insert_queue(self, content):
        try:
            self.redis_conn.rpush(config.get('queue_name'), content)
        except:
            pass

    def insert_vip_queue(self, content):
        try:
            self.redis_conn.rpush(config.get('vip_queue_name'), content)
        except:
            pass


if __name__ == "__main__":
    obj = RedisQueue()
    obj.insert_vip_queue("zhangsan@email.com")
    obj.insert_queue("1111")
    obj.insert_queue("2122")
    obj.get_queue