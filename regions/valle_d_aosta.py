from .region import BaseRegion
from .province import BaseProvince
import requests
import asyncio
import functools
import csv

class ValleDAosta(BaseRegion):
    """
    Implementation of Valle d'Aosta
    """
    name = "Valle d'Aosta"

    def __init__(self):
        super().__init__()

        # adding provinces
        self.add_province(BaseProvince(name='Aosta', short_name='AO'))

    def _fetch_air_quality_routine(self, day):
        """
        Populate the air quality of the provinces
        data is fetched from `http://www.arpa.vda.it/it/aria/la-qualit%C3%A0-dell-aria/stazioni-di-monitoraggio/inquinanti-export-dati`

        :param day: The day of which the air quality wants to be known (instance of `~datetime`)
        """
        super()._fetch_air_quality_routine(day)

        res = requests.post( 
            'http://www.arpa.vda.it/it/aria/la-qualit%C3%A0-dell-aria/stazioni-di-monitoraggio/dati-e-grafici',
            data = [
                ('exportRilev', 'si'),
                ('beginExportDate', day.strftime('%d/%m/%Y')),
                ('endExportDate', day.strftime('%d/%m/%Y')),
                ('stazioniExport[]', '4000'),
                ('stazioniExport[]', '4120'),
                ('stazioniExport[]', '4160'),
                ('stazioniExport[]', '4040'),
                ('stazioniExport[]', '4110'),
                ('stazioniExport[]', '4050'),
                ('parametriExport[]', '1000-1-1'),
                ('parametriExport[]', '1000-4-1'),
                ('parametriExport[]', '1030-1-1'),
                ('parametriExport[]', '1030-4-1'),
                ('parametriExport[]', '1040-5-1'),
                ('parametriExport[]', '1060-4-1'),
                ('parametriExport[]', '1060-5-1'),
                ('parametriExport[]', '1110-1-1'),
                ('parametriExport[]', '1110-7-3'),
                ('parametriExport[]', '1120-1-1'),
                ('parametriExport[]', '2000-1-1'),
            ]
        )
        
        header = ('parametro','statistica','scala','data','stazione','valore')
        parsed_csv = list(csv.DictReader(res.text.split('\n')[1:], fieldnames=header, delimiter=','))

        # air quality values
        province = self.provinces[0]

        so2 = [float(row['valore']) for row in parsed_csv 
                if row['parametro'] == 'Biossido di zolfo' and 
                   row['scala'] == 'Giornaliera' ]
        if len(so2) > 0: province.quality.so2 = round(sum(so2) / len(so2), 2)
        
        co = [float(row['valore']) for row in parsed_csv 
                if row['parametro'] == 'Monossido di carbonio']
        if len(co) > 0: province.quality.co = round(sum(co) / len(co), 2)
        
        o3 = [float(row['valore']) for row in parsed_csv 
                if row['parametro'] == 'Ozono' and 
                   row['scala'] == 'Giornaliera' ]
        if len(o3) > 0: province.quality.o3 = round(sum(o3) / len(o3), 2)
        
        pm10 = [float(row['valore']) for row in parsed_csv 
                if row['parametro'] == 'Polveri Pm10' and 
                   row['scala'] == 'Giornaliera' ]
        if len(pm10) > 0: province.quality.pm10 = round(sum(pm10) / len(pm10), 2)
        
        pm25 = [float(row['valore']) for row in parsed_csv 
                if row['parametro'] == 'Polveri Pm2.5' and 
                   row['scala'] == 'Giornaliera' ]
        if len(pm25) > 0: province.quality.pm25 = round(sum(pm25) / len(pm25), 2)
        
        c6h6 = [float(row['valore']) for row in parsed_csv 
                if row['parametro'] == 'Benzene' and 
                   row['scala'] == 'Giornaliera' ]
        if len(c6h6) > 0: province.quality.c6h6 = round(sum(c6h6) / len(c6h6), 2)
        
        no2 = [float(row['valore']) for row in parsed_csv 
                if row['parametro'] == 'Biossido di azoto' and 
                   row['scala'] == 'Giornaliera' ]
        if len(no2) > 0: province.quality.no2 = round(sum(no2) / len(no2), 2)

        if self.on_quality_fetched is not None: self.on_quality_fetched(self)