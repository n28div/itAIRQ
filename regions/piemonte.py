from .region import BaseRegion
from .province import BaseProvince
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

class Piemonte(BaseRegion):
    """
    Implementation of Piemonte
    """
    name = "Piemonte"
    indicator_map = {
        'c6h6': ('BENZENE', 'a3'),
        'co': ('02', 'a3'),
        'no2': ('04', 'a1'),
        'o3': ('05', 'a3'),
        'so2': ('01', 'a4'),
        'pm10': ('PM10_BH', 'a2'),
        'pm25': ('PM2.5_BH', 'a3'),
    }

    province_rete_map = {
        'Alessandria': '11',
        'Asti': '50',
        'Biella': '64',
        'Cuneo': '22',
        'Novara': '16',
        'Torino': '13',
        'Vercelli': '15',
    }

    def __init__(self):
        super().__init__()

        # adding provinces
        self.add_province(BaseProvince(name='Alessandria', short_name='AL'))
        self.add_province(BaseProvince(name='Asti', short_name='AT'))
        self.add_province(BaseProvince(name='Biella', short_name='BI'))
        self.add_province(BaseProvince(name='Cuneo', short_name='CN'))
        self.add_province(BaseProvince(name='Novara', short_name='NO'))
        self.add_province(BaseProvince(name='Torino', short_name='TO'))
        self.add_province(BaseProvince(name='Vercelli', short_name='VC'))
        self.add_province(BaseProvince(name='Verbano-Cusio-Ossola', short_name='VB'))

    def fetch_indicator_for_province(self, day: datetime, indicator: str, province: BaseProvince) -> float:
        """
        Fetches an indicator from 
        `http://www.sistemapiemonte.it/ambiente/srqa/consultadati_giorno.shtml?param_000=02&aggr_000=0&dataInizio=01/01/2019&dataFine=01/01/2019&filtroUscita=/xsrqaReportTableFilter.jsp&recordCompleti=no&opzioniFiltro=mostraIdRete=si&tipoReportistica=0&noMM`
        where the indicator is given in the param_000, adn the date in dataInizio and dataFine

        **Verbania-Cusio-Ossola seems to have no data available!**

        :param day: Day of interest
        :param indicator: Value of interest
        :param province: The province of interest
        :returns: The value
        """
        indicator_text, indicator_html_header = self.indicator_map[indicator]
        date = day.strftime('%d/%m/%Y')

        # verbania-cusio-ossola has no data
        if province.name in self.province_rete_map:
            rete = self.province_rete_map[province.name]

            res = requests.get( 
                'http://www.sistemapiemonte.it/ambiente/srqa/consultadati_giorno.shtml',
                params = (
                    ('param_000', indicator_text),
                    ('rete', rete),
                    ('aggr_000', '0'),
                    ('dataInizio', date),
                    ('dataFine', date),
                    ('filtroUscita', '/xsrqaReportTableFilter.jsp'),
                    ('recordCompleti', 'no'),
                    ('opzioniFiltro', 'mostraIdRete=no'),
                    ('tipoReportistica', '0'),
                    ('noMM', ''),
                )
            )

            # parse the html
            soup = BeautifulSoup(res.text, 'html.parser')
            values = list()
            for x in soup.find_all('td', {'headers': indicator_html_header}):
                f = re.findall(r'[-+]?\d*\.\d+|\d+', x.text)
                
                if len(f) == 1:
                    values.append(float(f[0]))
            
            if len(values) > 0:
                return round(sum(values) / len(values), 2)
            else:
                return None

    def fetch_indicator(self, day: datetime, indicator: str):
        """
        Fetches an indicator from 
        `http://www.sistemapiemonte.it/ambiente/srqa/consultadati_giorno.shtml?param_000=BENZENE&rete=11&aggr_000=0&dataInizio=01/05/2019&dataFine=01/05/2019&filtroUscita=/xsrqaReportTableFilter.jsp&recordCompleti=no&opzioniFiltro=mostraIdRete=no&tipoReportistica=0&noMM`
        where the indicator is given in the param_000, adn the date in dataInizio and dataFine

        **Verbania-Cusio-Ossola seems to have no data available!**

        :param day: Day of interest
        :param indicator: Value of interest
        """
        values = [self.fetch_indicator_for_province(day, indicator, p) for p in self.provinces]

        for i, elem in enumerate(self.provinces):
            setattr(elem.quality, indicator, values[i])

    def _fetch_air_quality_routine(self, day: datetime):
        """
        Populate the air quality of the provinces

        :param day: The day of which the air quality wants to be known (instance of `~datetime`)
        """
        for x in self.indicator_map.keys():
            self.fetch_indicator(day, x)

        if self.on_quality_fetched is not None: self.on_quality_fetched(self)