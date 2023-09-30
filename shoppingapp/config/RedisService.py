# encoding: utf-8
'''
 @author: 我不是大佬 
 @contact: 2869210303@qq.com
 @wx; safeseaa
 @qq; 2869210303
 @file: RedisService.py
 @time: 2023/8/23 17:40
  '''

import redis

### redis的相关配置
REDIS_CONFIG = {
    "host": 'localhost',
    "port": 6379,
    "db": 0,
    "password": 'zhao'
}


### redis服务类
class RedisService:
    host = 'localhost'
    port = 6379
    db = 0,
    password = 'zhao'

    @staticmethod
    def getConnection():
        return redis.Redis(host=RedisService.host, port=RedisService.port, db=0, password=RedisService.password)

    @staticmethod
    def getDict(key):
        ### result = {key.decode(): value.decode() for key, value in result.items()}
        return {key.decode(): value.decode() if isinstance(key, bytes) and isinstance(value, bytes)
        else value for key, value in RedisService.getConnection().hgetall(key).items()}

    @staticmethod
    def setDict(key, value, seconds=24 * 60 * 60):
        """
        seconds：过期时间
        """
        # 将None转换为空字符串
        r = RedisService.getConnection()
        r.hmset(key, {k: v if v is not None else '' for k, v in value.items()})
        r.expire(key, seconds)

    ### 清空所有的缓存数据
    @staticmethod
    def flushall():
        RedisService.getConnection().flushall()

    @staticmethod
    def delete(key):
        RedisService.getConnection().delete(key)

    @staticmethod
    def set(name, value, ex=None, px=None, nx=False, xx=False):
        return RedisService.getConnection().set(name, value, ex, px, nx, xx)
    @staticmethod
    def get(key):
        return RedisService.getConnection().get(key)