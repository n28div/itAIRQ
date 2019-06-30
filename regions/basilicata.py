from .region import BaseRegion
from .province import BaseProvince
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from html_table_extractor.extractor import Extractor
import re
from statistics import mean

class Basilicata(BaseRegion):
    """
    Implementation of Basilicata
    """
    name = "Basilicata"
    
    indicator_map = {
        'co': 4,
        'no2': 3,
        'so2': 1,
        'o3': 8,
        'pm10': 5,
        'pm25': 6,
        'c6h6': 9
    }

    province_stations = {
        'MT': [7, 8, 10],
        'PZ': [0, 1, 2, 3, 4, 5, 6, 9, 11, 12, 13, 14]
    }

    def __init__(self):
        super().__init__()

        # adding provinces
        self.add_province(BaseProvince(name='Matera', short_name='MT'))
        self.add_province(BaseProvince(name='Potenza', short_name='PZ'))
        
    def extract_float(self, s: str) -> float:
        """
        Extract the first float from a string

        :param s: The string where the float will be extracted
        :return: The float, if any found, or None
        """
        f = re.findall(r'([0-9]*[.]*[0-9]+)', s)
        return float(f[0]) if len(f) > 0 else None

    def _fetch_air_quality_routine(self, day: datetime):
        """
        Populate the air quality of the provinces
        Fetches data from `http://www.arpab.it/aria/qa.asp`

        :param day: The day of which the air quality wants to be known (instance of `~datetime`)
        """
        super()._fetch_air_quality_routine(day)

        res = requests.get('http://www.arpab.it/aria/qa.asp',
            params=[
                ('giorno', day.strftime('%d/%m/%Y'))
            ]
        )

        soup = BeautifulSoup(res.text, 'html.parser')
        table = soup.select_one('.tabellenav')

        if table is not None:
            extractor = Extractor(table)
            extractor.parse()
            table_data = extractor.return_list()[1:]

            for province in self.provinces:
                province_rows = [x for idx, x in enumerate(table_data) 
                                 if idx in self.province_stations[province.short_name]]
                
                for indicator, key in self.indicator_map.items():
                    values = [self.extract_float(x[key]) for x in province_rows
                              if self.extract_float(x[key]) is not None]
                    
                    if len(values) > 0:
                        setattr(province.quality, indicator, round(mean(values), 2))

        if self.on_quality_fetched is not None: self.on_quality_fetched(self)