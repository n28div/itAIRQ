import unittest
import datetime
from regions.liguria import Liguria

class LiguriaTest(unittest.TestCase):
    region_cls = Liguria
    air_quality = {
        'Genova': {'SO2': 9.17, 'NO2': 60.1, 'CO': 0.98, 'O3': 17.0, 'Pm10': 36.33, 'Pm2,5': 30.25, 'C6H6': 2.03},
        'Imperia': {'SO2': None, 'NO2': None, 'CO': None, 'O3': None, 'Pm10': None, 'Pm2,5': None, 'C6H6': None},
        'La Spezia': {'SO2': None, 'NO2': 72.0, 'CO': None, 'O3': None, 'Pm10': 16.0, 'Pm2,5': None, 'C6H6': 1.6},
        'Savona': {'SO2': 5.6, 'NO2': 42.83, 'CO': 1.0, 'O3': 52.5, 'Pm10': 41.83, 'Pm2,5': 40.8, 'C6H6': 1.99},
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