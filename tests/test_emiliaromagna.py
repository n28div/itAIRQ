import unittest
import datetime
from regions.emiliaromagna import EmiliaRomagna

class EmiliaRomagnaTest(unittest.TestCase):
    region_cls = EmiliaRomagna
    air_quality = {
        'Bologna': {'SO2': None, 'NO2': 32.29, 'CO': 1.3, 'O3': 21.5, 'Pm10': 48.86, 'Pm2,5': 35.0, 'C6H6': 2.35},
        'Rimini': {'SO2': None, 'NO2': 48.6, 'CO': 1.6, 'O3': 48.0, 'Pm10': 33.75, 'Pm2,5': 22.5, 'C6H6': 2.4},
        'Ferrara': {'SO2': None, 'NO2': 38.4, 'CO': 0.9, 'O3': 12.75, 'Pm10': 54.0, 'Pm2,5': 44.33, 'C6H6': 3.1},
        'Forlì-Cesena': {'SO2': None, 'NO2': 50.75, 'CO': 1.1, 'O3': 17.0, 'Pm10': 41.4, 'Pm2,5': 40.5, 'C6H6': 2.3},
        'Modena': {'SO2': None, 'NO2': 35.5, 'CO': 1.45, 'O3': 13.5, 'Pm10': 58.5, 'Pm2,5': 46.67, 'C6H6': 3.1},
        'Parma': {'SO2': None, 'NO2': 37.0, 'CO': 1.6, 'O3': 15.67, 'Pm10': 56.5, 'Pm2,5': 40.67, 'C6H6': 3.0},
        'Piacenza': {'SO2': None, 'NO2': 36.0, 'CO': 1.1, 'O3': 31.5, 'Pm10': 46.4, 'Pm2,5': 42.0, 'C6H6': 2.7},
        'Ravenna': {'SO2': 14.0, 'NO2': 40.4, 'CO': 1.5, 'O3': 15.0, 'Pm10': 57.75, 'Pm2,5': 43.0, 'C6H6': 3.2},
        'Reggio Emilia': {'SO2': None, 'NO2': 31.6, 'CO': 1.2, 'O3': 30.0, 'Pm10': 49.8, 'Pm2,5': 40.0, 'C6H6': 3.3}
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