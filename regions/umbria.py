from .region import BaseRegion
from .province import BaseProvince
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from html_table_extractor.extractor import Extractor
import re
from statistics import mean

class Umbria(BaseRegion):
    """
    Implementation of Umbria
    """
    name = "Umbria"

    def __init__(self):
        super().__init__()

        # adding provinces
        self.add_province(BaseProvince(name='Perugia', short_name='PG'))
        self.add_province(BaseProvince(name='Terni', short_name='TR'))
        
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
        Data is fetched from http://www.arpa.umbria.it/monitoraggi/aria/Default.aspx
        
        :param day: The day of which the air quality wants to be known (instance of `~datetime`)
        """
        super()._fetch_air_quality_routine(day)

        date_fmt = day.strftime('%d/%m/%Y')
        data = {
            '__EVENTTARGET': 'ctl00$Content$txtData',
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            '__VIEWSTATE': '/wEPDwUKMTUzNjEyNDUzNw9kFgJmD2QWAgIBD2QWAmYPZBYEAgsPZBYEAgEPFgIeC18hSXRlbUNvdW50AgMWBmYPZBYEAgEPDxYCHgdWaXNpYmxlaGQWAmYPFQEIMDkvMDQvMThkAgIPFQEZJm5ic3A7PC9wPg0KPHA+Jm5ic3A7PC9wPmQCAQ9kFgQCAQ9kFgJmDxUBCDA1LzA1LzE5ZAICDxUBwgFOZWxsYSBnaW9ybmF0YSBvZGllcm5hIGNpIHNvbm8gc3RhdGUgZGVsbGUgZGlmZmljb2x0JmFncmF2ZTsgdGVjbmljaGUgaW4gbWVyaXRvIGFsbGEgcHViYmxpY2F6aW9uZSBhdXRvbWF0aWNhIGRlaSBkYXRpIGRpIHNhYmF0byA0LiBMJ2luY29udmVuaWVudGUgdmVyciZhZ3JhdmU7IHJpc29sdG8gYWwgcGkmdWdyYXZlOyBwcmVzdG8uPC9wPmQCAg9kFgQCAQ9kFgJmDxUBCDE5LzAyLzE5ZAICDxUBhwM8c3Ryb25nPk1hbnV0ZW56aW9uZSBzdHJ1bWVudGF6aW9uZSAyMDE5PC9zdHJvbmc+PGJyIC8+RGFsIDE4IGZlYmJyYWlvIGFsIHByaW1vIG1hcnpvIHNvbm8gcHJldmlzdGUgbGUgb3BlcmF6aW9uaSBkaSBtYW51dGVuemlvbmUgcGVyaW9kaWNoZSAoYW5udWFsaSkgZGVsbGEgc3RydW1lbnRhemlvbmUgaW5zdGFsbGF0YSBuZWxsYSByZXRlIGRpIG1vbml0b3JhZ2dpby4gUGVyIHF1ZXN0byBtb3Rpdm8gcG90cmViYmVybyB2ZXJpZmljYXJzaSBkZWxsZSBpbnRlcnJ1emlvbmkgbmVsIHJpbGV2YW1lbnRvIGRlaSBkYXRpIHJlbGF0aXZpIGFnbGkgc3RydW1lbnRpIGluIG1hbnV0ZW56aW9uZS4mbmJzcDs8L3A+DQo8cD4mbmJzcDs8L3A+DQo8cD4mbmJzcDs8L3A+DQo8cD4mbmJzcDs8L3A+ZAIDDw8WBB4LUG9zdEJhY2tVcmwFK2FyY2hpdmlvTm90aXppZS5hc3B4P2NvZGljZVBhZ2luYT1SUk0mem9uYT0fAWdkZAIPD2QWAmYPZBYCAgEPEA8WBh4NRGF0YVRleHRGaWVsZAUETm9tZR4ORGF0YVZhbHVlRmllbGQFAklkHgtfIURhdGFCb3VuZGdkEBUPGVBlcnVnaWEgLSBQYXJjbyBDb3J0b25lc2UcUGVydWdpYSAtIFBvbnRlIFNhbiBHaW92YW5uaRRQZXJ1Z2lhIC0gRm9udGl2ZWdnZSBDaXR0w6AgZGkgQ2FzdGVsbG8gLSBDLiBDYXN0ZWxsbxpHdWJiaW8gLSBQaWF6emEgNDAgTWFydGlyaRFNYWdpb25lIC0gTWFnaW9uZRZGb2xpZ25vIC0gUG9ydGEgUm9tYW5hEFRvcmdpYW5vIC0gQnJ1ZmEZU3BvbGV0byAtIFBpYXp6YSBWaXR0b3JpYRJUZXJuaSAtIEJvcmdvIFJpdm8PVGVybmkgLSBDYXJyYXJhEVRlcm5pIC0gTGUgR3JhemllD0FtZWxpYSAtIEFtZWxpYRNOYXJuaSAtIE5hcm5pIFNjYWxvE09ydmlldG8gLSBDaWNvbmlhIDIVDwMzXzEDM18yBDNfNjkDM183AzNfMwMzXzYDM180AzNfNQUzXzIwNQM3XzEDN18yAzdfMwM3XzUDN180AzdfNhQrAw9nZ2dnZ2dnZ2dnZ2dnZ2dkZGT1g28Bzs2KuJM0nGhoW/nLrR4W/HpnjtjYCY1FCtl6eA==',
            '__VIEWSTATEGENERATOR': 'A373F38E',
            '__PREVIOUSPAGE': '5rDzdOLdhSojgNkWU0aySKgUcCP-WXzqaXaRNPbAb-Ekcs1vVl_yJf9liwnKWXEk15jl_Z8YIAJ86zswapmkHfDz2MMg9vQnDDQypfObingUmLuVVTMztw73FN9-55lI0',
            '__EVENTVALIDATION': '/wEdABshO2HSLC4Irl9HO+xCVg8wb8C3weGBaOLrENr46Y99cTPW5fmNeTa451MZa8LXyblcbg/Uqmez9yXP+xSTfXC/S9OqRU0oWDv+cbRkqcKtAqcsJFHEnZTzh0X+kVeLa7e4rr9jBld/uVqJpfp464tKRYmvyX4i1bjLFIfxIkw0G+o0YQNlnq4u76x5pwotKnDgEO4xErwMzPYvPwScdqOGIUgWeFC3y966dlr8RsY+JYzWFz2lgCufNhmaoE94Y/QiRS7TDGhtA/xOb3OYxEB522qpZQfWwl21Nv1xVarGgMm6hUuJGOA6Q4Ko1E4M+sQ9CZ53jxit2DF58lu5QFtr6x1PlqI+jgkEbNYTNUujYRbbFs2N4TjG5zEZ4xduFBkrD27kcj09V7bJX/igStyEnNJs5SuXPSKM2cTNsffB6XcH17ma9zwqai6CNsf9Og0ZPzjdX2zFoASErgXLJvie8NzsH8t7duXHZk9hbS9Vs21a/4yX1BpSDSioiW1gxr+tUHjFeS1m0yjnOD9kwBYX4jCmBywb7GNFZX8+9J5ux+74SyM4niEhJdJF38T+LG4OdFP/T/wCCiwNou/IvjveW95PGaK16TIOdZz/XYSt3Q==',
            'ctl00$Content$txtData': date_fmt,
            'ctl00$Content$Grafico1$cboStazioni': '3_1',
            'ctl00$Content$Grafico1$cboInquinante': 'SO224H'
        }
        res = requests.post('http://www.arpa.umbria.it/monitoraggi/aria/Default.aspx', data=data)

        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            
            html_table = soup.select_one('#ctl00_Content_TabellaDati')
            extractor = Extractor(html_table)
            extractor.parse()
            table = extractor.return_list()[2:]

            html_table = soup.select_one('#ctl00_Content_TabellaDatiAltreStazioni')
            extractor = Extractor(html_table)
            extractor.parse()
            table.extend(extractor.return_list()[2:])

            for province in self.provinces:
                province_rows = [x for x in table if x[0].split(' - ')[0].lower() == province.name.lower()]

                so2 = [self.extract_float(x[1]) for x in province_rows if self.extract_float(x[1]) is not None]
                no2 = [self.extract_float(x[3]) for x in province_rows if self.extract_float(x[3]) is not None]
                co = [self.extract_float(x[4]) for x in province_rows if self.extract_float(x[4]) is not None]
                pm10 = [self.extract_float(x[7]) for x in province_rows if self.extract_float(x[7]) is not None]
                pm25 = [self.extract_float(x[9]) for x in province_rows if self.extract_float(x[9]) is not None]
                o3 = [self.extract_float(x[5]) for x in province_rows if self.extract_float(x[5]) is not None]
                c6h6 = [self.extract_float(x[7]) for x in province_rows if self.extract_float(x[7]) is not None]

                if len(so2) > 0: province.quality.so2 = round(mean(so2), 2)
                if len(no2) > 0: province.quality.no2 = round(mean(no2), 2)
                if len(co) > 0: province.quality.co = round(mean(co), 2)
                if len(pm10) > 0: province.quality.pm10 = round(mean(pm10), 2)
                if len(pm25) > 0: province.quality.pm25 = round(mean(pm25), 2)
                if len(o3) > 0: province.quality.o3 = round(mean(o3), 2)
                if len(c6h6) > 0: province.quality.c6h6 = round(mean(c6h6), 2)

        if self.on_quality_fetched is not None: self.on_quality_fetched(self)