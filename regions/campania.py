from .region import BaseRegion
from .province import BaseProvince
import requests
import csv
from statistics import mean
import re

class Campania(BaseRegion):
    """
    Implementation of Campania
    """
    name = "Campania"

    indicator_map = {
        'pm10': 'PM10',
        'pm25': 'PM2.5',
        'no2': 'NO2',
        'o3': 'O3',
        'co': 'CO',
        'c6h6': 'Benzene',
        'so2': 'SO2'
    }

    provices_indicator = {
        'NA': ['acerrazi', 'areaasi', 'caporale', 'epomeo', 'marconi', 'na01', 'na02', 'na06', 'na07', 'na08', 'na09', 
               'pascoli', 'pvirgiliano', 'volla'],
        'SA': ['alburni', 'merc', 'parcof', 'polla', 'sa22', 'sa23', 'solimena', 'stadio'],
        'AV': ['alighieri', 'av41', 'solofrazi', 'villaav', 'villacom'],
        'BN': ['benevcs', 'benevzi', 'bn32'],
        'CE': ['ce51', 'ce52', 'ce54', 'aversa', 'cs']
    }

    def __init__(self):
        super().__init__()

        # adding provinces
        self.add_province(BaseProvince(name='Avellino', short_name='AV'))
        self.add_province(BaseProvince(name='Salerno', short_name='SA'))
        self.add_province(BaseProvince(name='Napoli', short_name='NA'))
        self.add_province(BaseProvince(name='Caserta', short_name='CE'))
        self.add_province(BaseProvince(name='Benevento', short_name='BN'))

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
        data is fetched from `http://www.arpacampania.it/web/guest/55`

        :param day: The day of which the air quality wants to be known (instance of `~datetime`)
        """
        super()._fetch_air_quality_routine(day)

        # first check for validated data
        res = requests.get('http://cemec.arpacampania.it/meteoambientecampania/php/downloadFileDati.php',
            params= [
                ('path', f'/var/www/html/meteoambientecampania/prodotti/aria_validati/arpac_dati_centraline_%s_validati.csv' % day.strftime('%Y%m%d'))
            ]
        )

        if 'Warning' in res.text:
            res = requests.get('http://cemec.arpacampania.it/meteoambientecampania/php/downloadFileDati.php',
                params= [
                    ('path', f'/var/www/html/meteoambientecampania/prodotti/aria/arpac_dati_centraline_%s.csv' % day.strftime('%Y%m%d'))
                ]
            )
    
        data = list(csv.reader(res.text.split('\n'), delimiter=','))[1:-1]
        for province in self.provinces:
            province_data = [x for x in data 
                             if x[0].split('_')[1].lower() in self.provices_indicator[province.short_name]]

            for indicator, key in self.indicator_map.items():
                indicator_values = [self.extract_float(x[5]) for x in province_data
                                    if x[2] == key and self.extract_float(x[5]) is not None]
                
                if len(indicator_values) > 0:
                    setattr(province.quality, indicator, round(mean(indicator_values), 2))

        if self.on_quality_fetched is not None: self.on_quality_fetched(self)