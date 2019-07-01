import settings
import redis
from threading import RLock
import json
import logging
import re

logger = logging.getLogger(__name__)

class Cache(object):
    """
    Class that handles the server cache
    """
    def __init__(self):
        self._server = redis.Redis(host=settings.redis['URL'], 
                                   port=settings.redis['PORT'], 
                                   password=settings.redis['PASSWORD'])
        
        self._mutex = RLock()

    class NotInCacheException(Exception):
        pass

    @property
    def full(self) -> bool:
        """
        Check if the cache is full
        :return: True if it's full, False otherwise
        """
        with self._mutex:
            info_memory = self._server.execute_command('info memory').decode('utf8')

        used_bytes = re.findall(r'used_memory:([0-9]*[.]*[0-9]+)', info_memory)[0]
        used_megabytes = int(used_bytes) / 10**6
        return used_megabytes == settings.redis['MEMORY']

    def _cache_clean(self):
        """
        Remove the oldest entry in the cache
        """
        min_date = None

        with self._mutex:
            for date in self._server.scan_iter():
                if min_date is None or date < min_date:
                    min_date = date
                
                logger.debug('Date %s will be removed', min_date)
                self._server.delete(min_date)

    def put(self, key: str, elem: str):
        """
        Puts an element in the cache
        :param key: The key where the element will be inserted
        :param elem: The element that will be inserted
        """
        if self.full:
            self._cache_clean()
        
        with self._mutex:
            self._server.set(key, elem)
        
        logger.debug('Key %s inserted', key)

    def get(self, key: str) -> dict:
        """
        Gets an element from the cache
        :param key: The key of the element in the cache
        :return: The dict representing the element in cache
        """
        result = None
        with self._mutex:
            result = self._server.get(key)
    
        if result is None:
            logger.debug('Cache miss of key %s', key)
            raise self.NotInCacheException()
        
        return result.decode('utf8')

    @property
    def keys(self) -> list:
        """
        :return: The list of cached keys
        """
        with self._mutex:
            return [x.decode('utf8') for x in self._server.keys()]

    def contains(self, key) -> bool:
        """
        Return wether a key is contained
        :param key: The tested key
        :return: True if the key is contained, False otherwise
        """
        isset = False
        with self._mutex:
            isset = self._server.exists(key)

        return isset