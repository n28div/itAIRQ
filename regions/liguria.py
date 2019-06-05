from .region import BaseRegion
from .province import BaseProvince
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from html_table_extractor.extractor import Extractor

class Liguria(BaseRegion):
    """
    Implementation of Liguria
    """
    name = "Liguria"
    
    indicator_map = {
        'c6h6': {'CodParam': 'BENZ', 'SiglaParam':'Benzene', 'table_idx': 7},
        'pm10': {'CodParam': 'PM10', 'SiglaParam':'Pm10', 'table_idx': 5},
        'pm25': {'CodParam': 'PM25', 'SiglaParam':'Pm2,5', 'table_idx': 5},
        'o3': {'CodParam': 'O300', 'SiglaParam':'Ozono', 'table_idx': 7},
        'co': {'CodParam': 'CO00', 'SiglaParam':'Monossido Carbonio', 'table_idx': 7},
        'no2': {'CodParam': 'NO20', 'SiglaParam':'Biossido Azoto', 'table_idx': 5},
        'so2': {'CodParam': 'SO20', 'SiglaParam':'Biossido Di Zolfo', 'table_idx': 5},
    }

    def __init__(self):
        super().__init__()

        # adding provinces
        self.add_province(BaseProvince(name='Genova', short_name='GE'))
        self.add_province(BaseProvince(name='Imperia', short_name='IM'))
        self.add_province(BaseProvince(name='La Spezia', short_name='SP'))
        self.add_province(BaseProvince(name='Savona', short_name='SV'))
        
    def set_indicator_value(self, day: datetime, indicator: str) -> float:
        """
        Populates the indicator specified in the provinces
        fetched data from `http://www.cartografiarl.regione.liguria.it/SiraQualAria/script/Pub3AccessoDatiAria.asp?Tipo=DatiGiorno`

        :param day: The day of interest
        :param indicator: The indicator of interest
        """
        if indicator not in self.indicator_map: return    
        
        data = {
            'Giorni': day.strftime('%d'),
            'Mesi': day.strftime('%m'),
            'Anni': day.strftime('%Y'),
            'TipoTema': 'SENSORI',
            'Tipo': 'DatiGiorno',
            'Anno': day.strftime('%Y'),
            'Mese': day.strftime('%m'),
            'Giorno': day.strftime('%d'),
            'DataIniz': day.strftime('%d/%m/%Y'),
            'CodTema': 'SENSORI'
        }

        res = requests.post('http://www.cartografiarl.regione.liguria.it/SiraQualAria/script/Pub3AccessoDatiAria13.asp',
                            data=data)
        
        soup = BeautifulSoup(res.text, 'html.parser')
        # a unique needs to be provided when a request is made, it is sent to the user in form of an hidden field
        try:
            id_richiesta = soup.find_all('input', {'name': 'Id_Richiesta'})[0]['value']
        except:
            # data for the selected day not available
            return

        map_data = self.indicator_map[indicator]
        res = requests.get('http://www.cartografiarl.regione.liguria.it/SiraQualAria/script/Pub3AccessoDatiAria131.asp',
            params = (
                ('Anno', day.strftime('%Y')),
                ('CodParam', map_data['CodParam']),
                ('SiglaParam', map_data['SiglaParam']),
                ('Azione', 'LISTA_STAZIONI'),
                ('CodTema', 'SENSORI'),
                ('DataIniz', day.strftime('%d/%m/%Y')),
                ('Id_Richiesta', id_richiesta)
            )
        )

        t = '</TR><TR>'.join(res.text.split('</TR>'))
        soup = BeautifulSoup(t, 'html.parser')
        table = soup.select('table')[0]

        extractor = Extractor(table)
        extractor.parse()
        # remove header
        table_data = extractor.return_list()[1:]
        
        if len(table_data) > 0:
            # remove any row after the first blank
            table_data = table_data[:next(idx for idx, y in enumerate(table_data) if len(y) == 0)]

            for province in self.provinces:
                values = list()
                for x in table_data:
                    if province.short_name in x[1]:
                        try:
                            values.append(float(x[map_data['table_idx']].strip()))
                        except:
                            pass 
                
                if len(values) != 0:
                    setattr(province.quality, indicator, round(float(sum(values) / len(values)), 2))

    def _fetch_air_quality_routine(self, day: datetime):
        """
        Populate the air quality of the provinces
        
        :param day: The day of which the air quality wants to be known (instance of `~datetime`)
        """
        super()._fetch_air_quality_routine(day)

        self.set_indicator_value(day, 'co')
        self.set_indicator_value(day, 'so2')
        self.set_indicator_value(day, 'no2')
        self.set_indicator_value(day, 'o3')
        self.set_indicator_value(day, 'pm10')
        self.set_indicator_value(day, 'pm25')
        self.set_indicator_value(day, 'c6h6')

        if self.on_quality_fetched is not None: self.on_quality_fetched(self)