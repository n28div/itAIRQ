from .region import BaseRegion
from .province import BaseProvince
from datetime import datetime
from statistics import mean
import requests
import json

class TrentinoAltoAdige(BaseRegion):
    """
    Implementation of Trentino Alto-Adige
    """
    name = "Trentino Alto-Adige"
    
    def __init__(self):
        super().__init__()

        # adding provinces
        self.add_province(BaseProvince(name='Trento', short_name='TN'))
        self.add_province(BaseProvince(name='Bolzano', short_name='BZ'))
        
    def fetch_bolzano(self, day: datetime):
        """
        Populate the air quality of the Bolzano province
        Sensor data is fetched from `http://dati.retecivica.bz.it/services/airquality/sensors?type=2`
        where `type` parameter is the day of interest: `1` for today, `2` for yesterday, no other dates
        available.
        
        :param day: The day of which the air quality wants to be known (instance of `~datetime`)
        """
        today = datetime.today()
        if (today - day).days > 1:
            # data is only available for today and yesterday
            return
        
        if day.day == today.day:
            type_param = 1
        else:
            type_param = 2

        res = requests.get('http://dati.retecivica.bz.it/services/airquality/sensors',
                           params={'type': type_param})
        res = json.loads(res.text)

        province = self.province_by_name('Bolzano')

        province.quality.co = round(mean([x['VALUE'] for x in res if x['MCODE'] == 'CO' and x['VALUE'] != -1]), 2)
        province.quality.so2 = round(mean([x['VALUE'] for x in res if x['MCODE'] == 'SO2' and x['VALUE'] != -1]), 2)
        province.quality.no2 = round(mean([x['VALUE'] for x in res if x['MCODE'] == 'NO2' and x['VALUE'] != -1]), 2)
        province.quality.o3 = round(mean([x['VALUE'] for x in res if x['MCODE'] == 'O3' and x['VALUE'] != -1]), 2)
        province.quality.pm10 = round(mean([x['VALUE'] for x in res if x['MCODE'] == 'PM10' and x['VALUE'] != -1]), 2)
        province.quality.pm25 = round(mean([x['VALUE'] for x in res if x['MCODE'] == 'PM2.5' and x['VALUE'] != -1]), 2)

    def fetch_trento(self, day: datetime):
        """
        Populate the air quality of the Trento province
        Sensor data is fetched from `https://appa.alpz.it/aria/opendata/json/{date}`
        where `{date}` is the day of interest in the format YYYY-MM-DD.
        
        :param day: The day of which the air quality wants to be known (instance of `~datetime`)
        """
        date_fmt = day.strftime('%Y-%m-%d')
        res = requests.get('https://appa.alpz.it/aria/opendata/json/%s' % date_fmt)
        res = json.loads(res.text)
        data = res['stazione']

        province = self.province_by_name('Trento')

        pm10 = list()
        pm25 = list()
        no2 = list()
        o3 = list()
        so2 = list()
        co = list()

        for station in data:
            station_data = station['dati'][date_fmt].values()
            for x in station_data:
                if 'pm10' in x: pm10.append(x['pm10'])
                if 'pm25' in x: pm25.append(x['pm25'])
                if 'no2' in x: no2.append(x['no2'])
                if 'o3' in x: o3.append(x['o3'])
                if 'so2' in x: so2.append(x['so2'])
                if 'co' in x: co.append(x['co'])

        if len(pm10) != 0: province.quality.pm10 = round(mean(pm10), 2)
        if len(pm25) != 0: province.quality.pm25 = round(mean(pm25), 2)
        if len(no2) != 0: province.quality.no2 = round(mean(no2), 2)
        if len(o3) != 0: province.quality.o3 = round(mean(o3), 2)
        if len(so2) != 0: province.quality.so2 = round(mean(so2), 2)
        if len(co) != 0: province.quality.co = round(mean(co), 2)
        
    def _fetch_air_quality_routine(self, day: datetime):
        """
        Populate the air quality of the provinces
        Sensor data is fetched from `https://www.dati.lombardia.it/resource/nicp-bhqi.json?data=2019-01-01T01:00:00.000`
        where the paramter `data` represents the date of interest.
        Information and location about each sensor can be fetched from `https://www.dati.lombardia.it/resource/t4f9-i4k5.json?provincia=BG`
        where the paramter `provincia` represents the province of interest

        :param day: The day of which the air quality wants to be known (instance of `~datetime`)
        """
        super()._fetch_air_quality_routine(day)
        
        self.fetch_trento(day)
        self.fetch_bolzano(day)
        
        if self.on_quality_fetched is not None: self.on_quality_fetched(self)