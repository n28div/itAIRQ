from .region import BaseRegion
from .province import BaseProvince
import requests
import csv
from statistics import mean
import re

class Puglia(BaseRegion):
    """
    Implementation of Valle d'Aosta
    """
    name = "Puglia"

    indicator_map = {
        'pm10': 'PM10',
        'pm25': 'PM2.5',
        'no2': 'NO2',
        'o3': 'O3',
        'co': 'CO',
        'c6h6': 'C6H6',
        'so2': 'SO2'
    }

    def __init__(self):
        super().__init__()

        # adding provinces
        self.add_province(BaseProvince(name='Bari', short_name='BA'))
        self.add_province(BaseProvince(name='Barletta-Andria-Trani', short_name='BT'))
        self.add_province(BaseProvince(name='Brindisi', short_name='BR'))
        self.add_province(BaseProvince(name='Foggia', short_name='FG'))
        self.add_province(BaseProvince(name='Lecce', short_name='LE'))
        self.add_province(BaseProvince(name='Taranto', short_name='TA'))

    def extract_float(self, s: str) -> float:
        """
        Extract the first float from a string

        :param s: The string where the float will be extracted
        :return: The float, if any found, or None
        """
        f = re.findall(r'([0-9]*[.]*[0-9]+)', s)
        return float(f[0]) if len(f) > 0 else None

    def _fetch_air_quality_routine(self, day):
        """
        Populate the air quality of the provinces
        data is fetched from `http://arpa.puglia.it/pentaho/ViewAction?solution=ARPAPUGLIA&path=metacatalogo&action=meta-aria.xaction`

        :param day: The day of which the air quality wants to be known (instance of `~datetime`)
        """
        super()._fetch_air_quality_routine(day)

        res = requests.get( 
            'http://www.arpa.puglia.it/pentaho/ViewAction',
            params = [
                ('DATAINIZIO', day.strftime('%Y%d%m')),
                ('DATAFINE', day.strftime('%Y%d%m')),
                ('type', 'csv'),
                (':', day.strftime('%Y')),
                ('solution', 'ARPAPUGLIA'),
                ('action', 'meta-aria.xaction'),
                ('path', 'metacatalogo')
            ]
        )
        
        parsed_csv = list(csv.reader(res.text.split('\n'), delimiter=';'))[9:]

        for province in self.provinces:
            province_data = [x for x in parsed_csv if len(x) > 2 and x[2] == province.name]
            
            for indicator, key in self.indicator_map.items():
                values = [self.extract_float(x[5]) for x in province_data 
                          if x[4] == key and self.extract_float(x[5]) is not None]
                
                if len(values) > 0:
                    setattr(province.quality, indicator, round(mean(values), 2))
        
        if self.on_quality_fetched is not None: self.on_quality_fetched(self)