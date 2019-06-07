import unittest
import datetime
from regions.veneto import Veneto

class VenetoTest(unittest.TestCase):
    region_cls = Veneto
    air_quality = {
       'Belluno': {'SO2': 9.0, 'NO2': 53.5, 'CO': None, 'O3': 45.67, 'Pm10': 23.33, 'Pm2,5': None, 'C6H6': None},
       'Padova': {'SO2': 6.75, 'NO2': 62.12, 'CO': None, 'O3': 9.14, 'Pm10': 97.29, 'Pm2,5': None, 'C6H6': None},
       'Rovigo': {'SO2': 7.0, 'NO2': 56.5, 'CO': None, 'O3': 6.0, 'Pm10': 64.0, 'Pm2,5': None, 'C6H6': None},
       'Treviso': {'SO2': 3.0, 'NO2': 56.6, 'CO': None, 'O3': 14.0, 'Pm10': 58.0, 'Pm2,5': None, 'C6H6': None},
       'Venezia': {'SO2': 3.0, 'NO2': 72.71, 'CO': 2.0, 'O3': 6.6, 'Pm10': 81.25, 'Pm2,5': None, 'C6H6': None},
       'Verona': {'SO2': 3.0, 'NO2': 62.2, 'CO': None, 'O3': 31.75, 'Pm10': 61.8, 'Pm2,5': None, 'C6H6': None},
       'Vicenza': {'SO2': None, 'NO2': 67.0, 'CO': None, 'O3': 41.0, 'Pm10': 62.67, 'Pm2,5': None, 'C6H6': None},
    }

    def test_air_quality(self):
        date = datetime.datetime(year=2019, month=1, day=1)

        region = self.region_cls()
        region.fetch_air_quality(date)
        region.wait_for_quality()

        for province in region.provinces:
            quality = province.quality.asdict()
            expected = self.air_quality[province.name]

            for key in expected.keys():
                self.assertEqual(quality[key], expected[key])

if __name__ == '__main__':
    unittest.main()