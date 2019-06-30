import unittest
import datetime
from regions.campania import Campania

class CampaniaTest(unittest.TestCase):
    region_cls = Campania
    air_quality = {
        'Avellino': {'SO2': 4.28, 'NO2': 13.66, 'CO': 1.54, 'O3': 64.35, 'Pm10': 27.47, 'Pm2,5': 14.3, 'C6H6': 0.48},
        'Salerno': {'SO2': 9.25, 'NO2': 14.74, 'CO': 0.61, 'O3': 56.97, 'Pm10': 16.54, 'Pm2,5': 10.21, 'C6H6': 0.79},
        'Napoli': {'SO2': 3.35, 'NO2': 19.89, 'CO': 0.73, 'O3': 53.41, 'Pm10': 30.12, 'Pm2,5': 19.19, 'C6H6': 1.09},
        'Caserta': {'SO2': 8.25, 'NO2': 17.16, 'CO': 0.64, 'O3': 59.4, 'Pm10': 21.46, 'Pm2,5': 14.77, 'C6H6': 0.63},
        'Benevento': {'SO2': None, 'NO2': 12.63, 'CO': None, 'O3': 65.7, 'Pm10': 25.84, 'Pm2,5': 17.13, 'C6H6': None}
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