from .quality import AirQuality
from datetime import datetime

class BaseProvince(object):
    """
    Class representing an italian province (Milano, Roma...)
    """
    name = None
    short_name = None
    quality = None

    def __init__(self, name:str=None, short_name:str=None):
        """
        :param name: The region's name (Roma, Milano, Torino...)
        :param name: The region's name (RM, MI, TO...)
        :raises TypeError: The param name or long_name is not specified
        """
        if self.name is None:
            if name is None: 
                raise TypeError('name of the region not set')
            else:
                self.name = name

        if self.short_name is None:
            if short_name is None: 
                raise TypeError('short_name of the region not set')
            else:
                self.short_name = short_name

        self.quality = AirQuality()

    async def fetch_air_quality(self, day:datetime):
        """
        Populate the air quality of the provinces

        :param day: The day of which the air quality wants to be known (instance of `~datetime`)
        """
        raise NotImplementedError