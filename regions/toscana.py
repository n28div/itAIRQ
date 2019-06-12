from .region import BaseRegion
from .province import BaseProvince
from datetime import datetime
import requests
from statistics import mean
import json
import re

class Toscana(BaseRegion):
    """
    Implementation of Toscana
    """
    name = "Toscana"

    def __init__(self):
        super().__init__()

        # adding provinces
        self.add_province(BaseProvince(name='Arezzo', short_name='AR'))
        self.add_province(BaseProvince(name='Firenze', short_name='FI'))
        self.add_province(BaseProvince(name='Grosseto', short_name='GR'))
        self.add_province(BaseProvince(name='Livorno', short_name='LI'))
        self.add_province(BaseProvince(name='Lucca', short_name='LU'))
        self.add_province(BaseProvince(name='Massa-Carrara', short_name='MS'))
        self.add_province(BaseProvince(name='Pisa', short_name='PI'))
        self.add_province(BaseProvince(name='Pistoia', short_name='PT'))
        self.add_province(BaseProvince(name='Prato', short_name='PO'))
        self.add_province(BaseProvince(name='Siena', short_name='SI'))
    
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
        Data is fetched from http://www.arpat.toscana.it/temi-ambientali/aria/qualita-aria/bollettini/bollettino_json/regionale/{date} where {date}
        is the date of interest in the format DD-MM-YYYY
        
        :param day: The day of which the air quality wants to be known (instance of `~datetime`)
        """
        super()._fetch_air_quality_routine(day)

        date_fmt = day.strftime('%d-%m-%Y')
        res = requests.get(f'http://www.arpat.toscana.it/temi-ambientali/aria/qualita-aria/bollettini/bollettino_json/regionale/{date_fmt}')
        res_json = json.loads(res.text)

        if len(res_json) > 0:
            for province in self.provinces:
                p_name = province.name.lower().replace('-', ' ')
                province_data = [x for x in res_json if p_name == x['PROVINCIA'].lower()]
                
                so2 = [self.extract_float(x['SO2']) for x in province_data if self.extract_float(x['SO2']) is not None]
                no2 = [self.extract_float(x['NO2']) for x in province_data if self.extract_float(x['NO2']) is not None]
                co = [self.extract_float(x['CO']) for x in province_data if self.extract_float(x['CO']) is not None]
                pm10 = [self.extract_float(x['PM10']) for x in province_data if self.extract_float(x['PM10']) is not None]
                pm25 = [self.extract_float(x['PM2dot5']) for x in province_data if self.extract_float(x['PM2dot5']) is not None]
                c6h6 = [self.extract_float(x['BENZENE']) for x in province_data if self.extract_float(x['BENZENE']) is not None]

                if len(so2) > 0: province.quality.so2 = round(mean(so2), 2)
                if len(no2) > 0: province.quality.no2 = round(mean(no2), 2)
                if len(co) > 0: province.quality.co = round(mean(co), 2)
                if len(pm10) > 0: province.quality.pm10 = round(mean(pm10), 2)
                if len(pm25) > 0: province.quality.pm25 = round(mean(pm25), 2)
                if len(c6h6) > 0: province.quality.c6h6 = round(mean(c6h6), 2)

        if self.on_quality_fetched is not None: self.on_quality_fetched(self)