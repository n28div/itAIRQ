from .province import BaseProvince
from datetime import datetime
from typing import List
import threading
from time import sleep

class BaseRegion(object):
    """
    Represents an italian region (Marche, Sicilia...)
    """
    name = None
    _provinces = list()
    on_quality_fetched = None

    def __init__(self, name:str=None):
        """
        :param name: The region's name
        :raises TypeError: The param name is not specified
        """
        if self.name is None:
            if name is None: 
                raise TypeError('name of the region not set')
            else:
                self.name = name

        self._thread = threading.Thread(target=self._fetch_air_quality_routine)

    def __str__(self) -> str:
        return '<Region %s - %d provinces>' % (self.name, len(self.provinces))

    @property
    def provinces(self) -> List[BaseProvince]: 
        return self._provinces
    
    def province_by_name(self, name) -> BaseProvince:
        for p in self.provinces:
            if p.name == name:
                return p

    def add_province(self, province:BaseProvince):
        """
        :raises TypeError: `province` is not subclass of `~province.BaseProvince`
        :raises ValueError: The province is already present
        """
        if isinstance(province, BaseProvince):
            if province in self.provinces:
                raise ValueError('province %s is already present' % province)
            else:
                self.provinces.append(province)
        else:
            raise TypeError('province must subclass BaseProvice')

    def fetch_air_quality(self, day:datetime):
        """
        Launch the thread that fetches the air quality

        :param day: The day of which the air quality wants to be known (instance of `~datetime`)
        """
        if not isinstance(day, datetime):
            raise TypeError('day should be a datetime instance')
        
        if not self._thread.is_alive():
            self._thread._args = (day,)
            self._thread.start()

    def wait_for_quality(self):
        """
        Waits until the fetching air quality routine has stopped
        """
        self._thread.join()

    def _fetch_air_quality_routine(self, day):
        """
        Fetches and sets the variabile quality

        :param day: The day of which the air quality wants to be known (instance of `~datetime`)
        """
        raise NotImplementedError