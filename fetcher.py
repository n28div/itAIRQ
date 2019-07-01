import settings
from datetime import datetime
from regions import regions_list
import json
import threading
from queue import PriorityQueue
import logging

logger = logging.getLogger(__name__)

class FetchRequest(object):
    """
    Class that represent the request to fetch some data and fetches it
    """
    def __init__(self, fetcher, day: datetime):
        self._fetcher = fetcher

        if day > datetime.now():
            raise ValueError('Date is in the future!')
        else:
            self._day = day

        self._thread = threading.Thread(target=self.run)

    def __str__(self) -> str:
        return "<Fetching %s>" % (self._day.strftime('%Y/%m/%d'))

    def start(self):
        """
        Starts the fetching routine
        """
        self._thread.start()

    def run(self) -> list:
        """
        Fetch air quality of each region and saves it into the cache
        """
        logger.debug('Fetching date %s', self._day.strftime('%Y/%m/%d'))
        
        regions = [r() for r in regions_list]
        air_quality = list()
            
        # fetch air quality of each region
        for r in regions:
            r.fetch_air_quality(self._day)
        
        # gather results from all regions
        for r in regions:
            # wait until region has fetched his data
            r.wait_for_quality()
            logging.info('Fetched region:%s for day:%s', r.name, self._day)
            air_quality.append({
                'name': r.name,
                'provinces': [
                    {'name': x.name, 'short': x.short_name, 'quality': x.quality.asdict()} 
                    for x in r.provinces]
            })

        self._fetcher.fetched_result(self._day, air_quality)
        
class Fetcher(object):
    """
    Object representing the handler of each day that needs to be updated
    """
    def __init__(self, cache):
        self._cache = cache
        self._thread = threading.Thread(name='Fetcher', target=self.run)
        # Request queue
        self._requests = PriorityQueue(maxsize=settings.data['MAX_CONCURENT_FETCHER'])
        
        self._pending_request_days = list()
        self._mutex = threading.RLock()

        self._thread.start()
        
    def run(self):
        """
        Demon that runs countinously to update data
        """
        while True:
            req = self._requests.get()[1]
            req.start()
            logging.info('Running request %s', req)
    
    def fetch_day(self, day: datetime):
        """
        Method used to fetch a result, if it's in cache it's update task is put in the queue
        :param day: Day requested
        """
        # Check that date fetching is not pending
        day_fmt = day.strftime('%Y%m%d')
        already_in = self._cache.contains(day_fmt)

        with self._mutex:
            if day_fmt not in self._pending_request_days:
                request = FetchRequest(self, day)
                self._requests.put_nowait((1 if already_in else 0, request))
        
        result = self._cache.get(day_fmt)
        return json.loads(result)

    def fetch_day_high_priority(self, day: datetime):
        """
        Method used to fetch a result, if it's in cache it's update task is put in the queue
        with an high priority
        :param day: Day requested
        """
        # Check that date fetching is not pending
        day_fmt = day.strftime('%Y%m%d')

        with self._mutex:
            if day_fmt not in self._pending_request_days:
                request = FetchRequest(self, day)
                self._requests.put_nowait((0, request))
        
        result = self._cache.get(day_fmt)
        return json.loads(result)

    def fetched_result(self, day: datetime, result: dict):
        """
        Method called by a FetchRequest when the data is ready

        :param day: The day fetched
        :param result: The dict representing the result
        """
        self._cache.put(day.strftime('%Y%m%d'), json.dumps(result))