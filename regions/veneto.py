from .region import BaseRegion
from .province import BaseProvince
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from html_table_extractor.extractor import Extractor

class Veneto(BaseRegion):
    """
    Implementation of Veneto
    """
    name = "Veneto"
    
    indicator_map = {
        'co': 14,
        'no2': 3,
        'so2': 11,
        'o3': 10,
        'pm10': 6,
    }

    def __init__(self):
        super().__init__()

        # adding provinces
        self.add_province(BaseProvince(name='Belluno', short_name='BL'))
        self.add_province(BaseProvince(name='Padova', short_name='PD'))
        self.add_province(BaseProvince(name='Rovigo', short_name='RO'))
        self.add_province(BaseProvince(name='Treviso', short_name='TV'))
        self.add_province(BaseProvince(name='Venezia', short_name='VE'))
        self.add_province(BaseProvince(name='Verona', short_name='VR'))
        self.add_province(BaseProvince(name='Vicenza', short_name='VI'))

    def indicator_value(self, table_data: list, indicator: str) -> float:
        """
        Calculates the mean of the indicator specified

        :param table_data: Parsed table data
        :param indicator: The indicator of interest
        :return: The average value of the indicator
        """
        values = list()
        if indicator in self.indicator_map:
            values = [float(x[self.indicator_map[indicator]]) for x in table_data if x[self.indicator_map[indicator]].isdigit()]
        
        if len(values) > 0:
            return round(float(sum(values) / len(values)), 2)
        else:
            return None

    def _fetch_air_quality_routine(self, day: datetime):
        """
        Populate the air quality of the provinces
        Fetches data from `http://www.arpa.veneto.it/arpavinforma/bollettini/aria/aria_dati_validati_storico.php`

        :param day: The day of which the air quality wants to be known (instance of `~datetime`)
        """
        for province in self.provinces: 
            data = {
                'provincia': province.name.lower(),
                'giorno': day.strftime('%d'),
                'mese': day.strftime('%m'),
                'anno': day.strftime('%Y'),
                'Vai': 'Visualizza il bollettino'
            }
            
            response = requests.post('http://www.arpa.veneto.it/arpavinforma/bollettini/aria/aria_dati_validati_storico.php', data=data)
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.select_one('#ariadativalidati table')

            if table:
                extractor = Extractor(table)
                extractor.parse()
                table_data = extractor.return_list()[3:]

                province.quality.co = self.indicator_value(table_data, 'co')
                province.quality.so2 = self.indicator_value(table_data, 'so2')
                province.quality.no2 = self.indicator_value(table_data, 'no2')
                province.quality.o3 = self.indicator_value(table_data, 'o3')
                province.quality.pm10 = self.indicator_value(table_data, 'pm10')
                province.quality.pm25 = self.indicator_value(table_data, 'pm25')
                province.quality.c6h6 = self.indicator_value(table_data, 'c6h6')

        if self.on_quality_fetched is not None: self.on_quality_fetched(self)