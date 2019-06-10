import unittest
import datetime
from regions.toscana import Toscana

class ToscanaTest(unittest.TestCase):
    region_cls = Toscana
    air_quality = {
        'Arezzo': {'SO2': None, 'NO2': 37.33, 'CO': 1.1, 'O3': None, 'Pm10': 22.67, 'Pm2,5': 24.0, 'C6H6': 2.3},
        'Firenze': {'SO2': 0.1, 'NO2': 66.14, 'CO': 1.8, 'O3': None, 'Pm10': 57.71, 'Pm2,5': 42.0, 'C6H6': 3.35},
        'Grosseto': {'SO2': None, 'NO2': 58.0, 'CO': None, 'O3': None, 'Pm10': 28.5, 'Pm2,5': 14.0, 'C6H6': None},
        'Livorno': {'SO2': 0.9, 'NO2': 62.8, 'CO': 1.0, 'O3': None, 'Pm10': 19.0, 'Pm2,5': 18.0, 'C6H6': 1.0},
        'Lucca': {'SO2': 0.8, 'NO2': 52.5, 'CO': None, 'O3': None, 'Pm10': 68.4, 'Pm2,5': 79.5, 'C6H6': 3.3},
        'Massa-Carrara': {'SO2': None, 'NO2': 35.0, 'CO': None, 'O3': None, 'Pm10': 29.5, 'Pm2,5': 22.0, 'C6H6': None},
        'Pisa': {'SO2': None, 'NO2': 52.25, 'CO': 1.3, 'O3': None, 'Pm10': 50.25, 'Pm2,5': 47.5, 'C6H6': None},
        'Pistoia': {'SO2': None, 'NO2': 40.0, 'CO': None, 'O3': None, 'Pm10': 47.5, 'Pm2,5': 62.0, 'C6H6': None},
        'Prato': {'SO2': None, 'NO2': 69.5, 'CO': 1.6, 'O3': None, 'Pm10': 124.0, 'Pm2,5': 107.5, 'C6H6': 2.5},
        'Siena': {'SO2': None, 'NO2': 69.0, 'CO': 0.6, 'O3': None, 'Pm10': 28.5, 'Pm2,5': 35.0, 'C6H6': None}
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