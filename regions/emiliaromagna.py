from .region import BaseRegion
from .province import BaseProvince
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from html_table_extractor.extractor import Extractor
import re
from statistics import mean

class EmiliaRomagna(BaseRegion):
    """
    Implementation of Emilia-Romagna
    """
    name = "Emilia-Romagna"

    def __init__(self):
        super().__init__()

        # adding provinces
        self.add_province(BaseProvince(name='Bologna', short_name='BO'))
        self.add_province(BaseProvince(name='Rimini', short_name='RN'))
        self.add_province(BaseProvince(name='Ferrara', short_name='FE'))
        self.add_province(BaseProvince(name='Forlì-Cesena', short_name='FC'))
        self.add_province(BaseProvince(name='Modena', short_name='MO'))
        self.add_province(BaseProvince(name='Parma', short_name='PR'))
        self.add_province(BaseProvince(name='Piacenza', short_name='PC'))
        self.add_province(BaseProvince(name='Ravenna', short_name='RA'))
        self.add_province(BaseProvince(name='Reggio Emilia', short_name='RE'))
        
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
        Populate the air quality of the provinces.
        Data is fetched from https://www.arpae.it/qualita-aria/bollettino-qa/{date} where {date}
        is the date of interest in the format YYYYMMDD
        
        :param day: The day of which the air quality wants to be known (instance of `~datetime`)
        """
        super()._fetch_air_quality_routine(day)

        date_fmt = day.strftime('%Y%m%d')
        res = requests.get(f'https://www.arpae.it/qualita-aria/bollettino-qa/{date_fmt}')

        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            table_rows = '\n'.join([str(x) for x in soup.select('.tabella table tbody tr')])
            big_table = f'<table>{table_rows}</table>'
            extractor = Extractor(big_table)
            extractor.parse()
            table = extractor.return_list()

            for province in self.provinces:
                province_rows = [x for x in table if x[0] == province.short_name]

                so2 = [self.extract_float(x[9]) for x in province_rows if self.extract_float(x[9]) is not None]
                no2 = [self.extract_float(x[4]) for x in province_rows if self.extract_float(x[4]) is not None]
                co = [self.extract_float(x[8]) for x in province_rows if self.extract_float(x[8]) is not None]
                pm10 = [self.extract_float(x[2]) for x in province_rows if self.extract_float(x[2]) is not None]
                pm25 = [self.extract_float(x[3]) for x in province_rows if self.extract_float(x[3]) is not None]
                o3 = [self.extract_float(x[6]) for x in province_rows if self.extract_float(x[6]) is not None]
                c6h6 = [self.extract_float(x[7]) for x in province_rows if self.extract_float(x[7]) is not None]

                if len(so2) > 0: province.quality.so2 = round(mean(so2), 2)
                if len(no2) > 0: province.quality.no2 = round(mean(no2), 2)
                if len(co) > 0: province.quality.co = round(mean(co), 2)
                if len(pm10) > 0: province.quality.pm10 = round(mean(pm10), 2)
                if len(pm25) > 0: province.quality.pm25 = round(mean(pm25), 2)
                if len(o3) > 0: province.quality.o3 = round(mean(o3), 2)
                if len(c6h6) > 0: province.quality.c6h6 = round(mean(c6h6), 2)

        if self.on_quality_fetched is not None: self.on_quality_fetched(self)