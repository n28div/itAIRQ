from .province import BaseProvince
import asyncio
from datetime import datetime
from typing import List

class BaseRegion(object):
    """
    Represents an italian region (Marche, Sicilia...)
    """
    name = None
    _provinces = list()

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

    async def fetch_air_quality(self, day:datetime):
        """
        Populate the air quality of the provinces

        :param day: The day of which the air quality wants to be known (instance of `~datetime`)
        """
        if not isinstance(day, datetime):
            raise TypeError('day should be a datetime instance')

        loop = asyncio.get_event_loop()
        tasks = list()

        for p in self.provinces:
            tasks.append(loop.create_task(p.fetch_air_quality(day)))

        loop.run_until_complete(tasks)
