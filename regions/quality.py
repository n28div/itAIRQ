from typing import Dict

class AirQuality(object):
    """
    Class that represents the values that a province could provide
    """
    so2 = None
    no2 = None
    co = None
    o3 = None
    pm10 = None
    pm25 = None
    c6h6 = None

    def __str__(self) -> str:
        return '< SO2:%f NO2:%f CO:%f O3:%f Pm10:%f Pm2,5:%f C6H6:%f >' % (
            self.so2,
            self.no2,
            self.co,
            self.o3,
            self.pm10,
            self.pm25,
            self.c6h6
        )

    def asdict(self) -> Dict[str, str]:
        """
        :returns: The object as a dict
        """
        return {
            'SO2': self.so2,
            'NO2': self.no2,
            'O3': self.o3,
            'Pm10': self.pm10,
            'Pm2,5': self.pm25,
            'C6H6': self.c6h6
        }
