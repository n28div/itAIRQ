from .region import BaseRegion
from .province import BaseProvince
from sodapy import Socrata
from datetime import datetime
import json

class Lombardia(BaseRegion):
    """
    Implementation of Lombardia
    """
    name = "Lombardia"
    
    indicator_map = {
        'co': 'Monossido di Carbonio',
        'no2': 'Ossidi di Azoto',
        'so2': 'Biossido di Zolfo',
        'o3': 'Ozono',
        'pm10': 'PM10 (SM2005)',
        'pm25': 'Particelle sospese PM2.5',
        'c6h6': 'Benzene'
    }

    def __init__(self):
        super().__init__()

        # adding provinces
        self.add_province(BaseProvince(name='Bergamo', short_name='BG'))
        self.add_province(BaseProvince(name='Brescia', short_name='BS'))
        self.add_province(BaseProvince(name='Como', short_name='CO'))
        self.add_province(BaseProvince(name='Cremona', short_name='CR'))
        self.add_province(BaseProvince(name='Lecco', short_name='LC'))
        self.add_province(BaseProvince(name='Lodi', short_name='LO'))
        self.add_province(BaseProvince(name='Mantova', short_name='MN'))
        self.add_province(BaseProvince(name='Milano', short_name='MI'))
        self.add_province(BaseProvince(name='Monza e della Brianza', short_name='MB'))
        self.add_province(BaseProvince(name='Pavia', short_name='PV'))
        self.add_province(BaseProvince(name='Sondrio', short_name='SO'))
        self.add_province(BaseProvince(name='Varese', short_name='VA'))

    def get_sensors_value(self, sensor_id: int, values: list) -> list:
        """
        Get the values of the the station specified
        
        :param sensor_id: The station id
        :param values: The values of all stations
        :return: The values measured by that station
        """
        return [float(x['valore']) for x in values if x['idsensore'] == sensor_id and x['stato'] == 'VA']

    def indicator_value(self, stations: list, values: list, indicator: str) -> list:
        """
        Aggregate data from values and stations about the indicator of interest

        :param stations: The stations of interest
        :param values: The values of every station in the region
        :indicator: The indicator needed (must be a key of the indicator_map)
        :return: The average value of indicator
        """
        indicator_key = self.indicator_map[indicator]
        indicator_values = list()

        for station in stations:
            if station['nometiposensore'] == indicator_key:
                vals = self.get_sensors_value(station['idsensore'], values)

                if len(vals) > 0:
                    indicator_values.append(float(sum(vals) / len(vals)))

        return None if len(indicator_values) == 0 else round(sum(indicator_values) / len(indicator_values), 2)

    def _fetch_air_quality_routine(self, day: datetime):
        """
        Populate the air quality of the provinces
        Sensor data is fetched from `https://www.dati.lombardia.it/resource/nicp-bhqi.json?data=2019-01-01T01:00:00.000`
        where the paramter `data` represents the date of interest.
        Information and location about each sensor can be fetched from `https://www.dati.lombardia.it/resource/t4f9-i4k5.json?provincia=BG`
        where the paramter `provincia` represents the province of interest

        :param day: The day of which the air quality wants to be known (instance of `~datetime`)
        """
        # calculate date
        super()._fetch_air_quality_routine(day)

        start_date = day.strftime('%Y-%m-%dT00:00.000')
        
        today = datetime.now()
        if day.day == today.day and day.month == today.month and day.year == today.year: 
            end_date = day.strftime('%Y-%m-%dT%I:00:00.000') 
        else:
            end_date = day.strftime('%Y-%m-%dT23:59:59.000') 

        # requests are made through the official socrata wrapper
        client = Socrata("www.dati.lombardia.it", None)
        sensors_data = client.get('nicp-bhqi', limit=10**10,
                                  where="data between '%s' and '%s'" % (start_date, end_date))

        for province in self.provinces:
            sensors_info = client.get('t4f9-i4k5', provincia=province.short_name, limit=10**10)

            province.quality.co = self.indicator_value(sensors_info, sensors_data, 'co')
            province.quality.so2 = self.indicator_value(sensors_info, sensors_data, 'so2')
            province.quality.no2 = self.indicator_value(sensors_info, sensors_data, 'no2')
            province.quality.o3 = self.indicator_value(sensors_info, sensors_data, 'o3')
            province.quality.pm10 = self.indicator_value(sensors_info, sensors_data, 'pm10')
            province.quality.pm25 = self.indicator_value(sensors_info, sensors_data, 'pm25')
            province.quality.c6h6 = self.indicator_value(sensors_info, sensors_data, 'c6h6')

        if self.on_quality_fetched is not None: self.on_quality_fetched(self)