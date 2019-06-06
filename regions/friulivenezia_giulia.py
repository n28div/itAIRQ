from .region import BaseRegion
from .province import BaseProvince
from sodapy import Socrata
from datetime import datetime
import json
from statistics import mean

class FriuliVeneziaGiulia(BaseRegion):
    """
    Implementation of FriuliVeneziaGiulia
    """
    name = "FriuliVeneziaGiulia"
    
    indicator_map = {
        'co': {'key': 't274-vki6', 'param': 'media_mobile_8h_max'},
        'no2': {'key': 'ke9b-p6z2', 'param': 'media_oraria_max'},
        'so2': {'key': '2zdv-x7g2', 'param': 'media_giornaliera'},
        'o3': {'key': '7vnx-28uy', 'param': 'media_oraria_max'},
        'pm10': {'key': '94k8-siin', 'param': 'media_giornaliera'},
        'pm25': {'key': 'd63p-pqpr', 'param': 'media_giornaliera'}
    }

    def __init__(self):
        super().__init__()

        # adding provinces
        self.add_province(BaseProvince(name='Gorizia', short_name='GO'))
        self.add_province(BaseProvince(name='Pordenone', short_name='PN'))
        self.add_province(BaseProvince(name='Trieste', short_name='TS'))
        self.add_province(BaseProvince(name='Udine', short_name='UD'))
        
    def indicator_value(self, indicator: str, day: datetime) -> list:
        """
        Populate provinces indicator

        :indicator: The indicator needed (must be a key of the indicator_map)
        :day: The day of interest
        :return: The average value of indicator
        """
        date_fmt = day.strftime('%Y-%m-%dT00:00.000')
        key = self.indicator_map[indicator]['key']
        param = self.indicator_map[indicator]['param']
        
        client = Socrata("www.dati.friuliveneziagiulia.it", None)
        sensors_data = client.get(key, 
                                  limit=10**10,
                                  data_misura=date_fmt)

        for province in self.provinces:
            values = [x for x in sensors_data if x['rete'] == province.name and x['dati_insuff'] == 'False']
            
            if len(values) != 0:
                float_values = [float(x[param]) for x in values]
                setattr(province.quality, indicator, round(mean(float_values), 2))          

    def _fetch_air_quality_routine(self, day: datetime):
        """
        Populate the air quality of the provinces
        Sensor data is fetched from `https://www.dati.friuliveneziagiulia.it/browse?q=Aria&sortBy=relevance`.
        
        :param day: The day of which the air quality wants to be known (instance of `~datetime`)
        """
        # calculate date
        super()._fetch_air_quality_routine(day)
        
        self.indicator_value('co', day)
        self.indicator_value('no2', day)
        self.indicator_value('so2', day)
        self.indicator_value('o3', day)
        self.indicator_value('pm10', day)
        self.indicator_value('pm25', day)
        
        if self.on_quality_fetched is not None: self.on_quality_fetched(self)