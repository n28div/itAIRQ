import unittest
import datetime
from regions.piemonte import Piemonte

class PiemonteTest(unittest.TestCase):
    region_cls = Piemonte
    air_quality = {
        'Alessandria': {'SO2': 4.0, 'NO2': 52.67, 'CO': None, 'O3': 35.5, 'Pm10': 68.0, 'Pm2,5': 49.0, 'C6H6': 2.3},
        'Asti': {'SO2': 8.0, 'NO2': 48.33, 'CO': 1.3, 'O3': 21.5, 'Pm10': None, 'Pm2,5': None, 'C6H6': 3.3},
        'Biella': {'SO2': None, 'NO2': 46.5, 'CO': 1.0, 'O3': 40.67, 'Pm10': 31.0, 'Pm2,5': 27.0, 'C6H6': 1.65},
        'Cuneo': {'SO2': 10.0, 'NO2': 41.33, 'CO': 0.75, 'O3': 25.25, 'Pm10': 51.0, 'Pm2,5': 44.0, 'C6H6': 1.77},
        'Novara': {'SO2': 14.5, 'NO2': 47.67, 'CO': 1.32, 'O3': 34.17, 'Pm10': 76.0, 'Pm2,5': 69.0, 'C6H6': 2.72},
        'Torino': {'SO2': 13.5, 'NO2': 56.81, 'CO': 1.1, 'O3': 25.0, 'Pm10': 64.0, 'Pm2,5': 59.0, 'C6H6': 2.29},
        'Vercelli': {'SO2': 4.0, 'NO2': 45.75, 'CO': 0.9, 'O3': 28.5, 'Pm10': 59.0, 'Pm2,5': 54.0, 'C6H6': 1.9},
        'Verbano-Cusio-Ossola': {'SO2': None, 'NO2': None, 'CO': None, 'O3': None, 'Pm10': None, 'Pm2,5': None, 'C6H6': None},
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