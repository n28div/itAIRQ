from .region import BaseRegion
from .province import BaseProvince
from datetime import datetime
import requests
import json
import re
from statistics import mean

class Abruzzo(BaseRegion):
    """
    Implementation of Abruzzo
    """
    name = "Abruzzo"

    indicator_map = {
        'pm10': 'PM10#MEDIA_GIORNO',
        'pm25': 'PM2_5#MEDIA_GIORNO',
        'c6h6': 'BEN#MEDIA_GIORNO',
        'no2': 'NO2#MAX_MEDIA_ORARIA_IN_GIORNO',
        'so2': 'SO2#MAX_MEDIA_ORARIA_IN_GIORNO',
        'co': 'CO#MAX_MEDIA_8ORE_IN_GIORNO',
        'o3': 'O3#MAX_MEDIA_8ORE_IN_GIORNO'
    }

    def __init__(self):
        super().__init__()

        # adding provinces
        self.add_province(BaseProvince(name='Chieti', short_name='CH'))
        self.add_province(BaseProvince(name="L'Aquila", short_name='AQ'))
        self.add_province(BaseProvince(name='Pescara', short_name='PE'))
        self.add_province(BaseProvince(name='Teramo', short_name='TE'))
        
    def extract_float(self, s: str) -> float:
        """
        Extract the first float from a string

        :param s: The string where the float will be extracted
        :return: The float, if any found, or None
        """
        f = re.findall(r'([0-9]*[.]*[0-9]+)', s)
        return float(f[0]) if len(f) > 0 else None

    def set_province_indicator(self, province: BaseProvince, values: list):
        """
        Populate air quality of a province
        
        :param province: The province of interest
        :param values: The values from the stations of that province
        """
        for indicator, mapped in self.indicator_map.items():
            indicator_values = list()

            for v in values:
                if mapped in v['storico'] and len(v['storico'][mapped]) > 0:
                    indicator_val = self.extract_float(v['storico'][mapped][0]['valore'])
                    if indicator_val is not None:
                        indicator_values.append(indicator_val)

            if len(indicator_values) > 0:
                setattr(province.quality, indicator, round(mean(indicator_values), 2))

    def _fetch_air_quality_routine(self, day: datetime):
        """
        Populate the air quality of the provinces.
        Data is fetched from 'https://sira.artaabruzzo.it/server/{date}.json' where {date}
        is the date of interest in the format YYYYMMDD
        Data about the sensors position is fetched from `https://sira.artaabruzzo.it/server/arta.json`
        
        :param day: The day of which the air quality wants to be known (instance of `~datetime`)
        """
        super()._fetch_air_quality_routine(day)

        res = requests.get('https://sira.artaabruzzo.it/server/arta.json')
        sensors_location = json.loads(res.text)['stazioni']

        date_fmt = day.strftime("%Y%m%d")
        res = requests.get(f'https://sira.artaabruzzo.it/server/{date_fmt}.json')
        
        if res.status_code == 200:
            sensors_values = json.loads(res.text)['stazioni']

            for p in self.provinces:
                province_sensors = [x['codice'] for x in sensors_location if x['prov'] == p.short_name] 
                province_values = [x for x in sensors_values if x['stazione'] in province_sensors]
                self.set_province_indicator(p, province_values)

        if self.on_quality_fetched is not None: self.on_quality_fetched(self)