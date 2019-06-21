import unittest
import datetime
from regions.abruzzo import Abruzzo

class AbruzzoTest(unittest.TestCase):
    region_cls = Abruzzo
    air_quality = {
        'Chieti': {'SO2': None, 'NO2': 14.0, 'CO': 0.62, 'O3': 74.0, 'Pm10': 15.67, 'Pm2,5': 8.5, 'C6H6': 0.93},
        'L\'Aquila': {'SO2': 1.0, 'NO2': 48.5, 'CO': 1.07, 'O3': 80.5, 'Pm10': 13.0, 'Pm2,5': 10.0, 'C6H6': 0.37},
        'Pescara': {'SO2': 0.0, 'NO2': 43.5, 'CO': 0.9, 'O3': 79.5, 'Pm10': 37.75, 'Pm2,5': 15.0, 'C6H6': 0.76},
        'Teramo': {'SO2': None, 'NO2': 63.5, 'CO': 1.9, 'O3': None, 'Pm10': 17.0, 'Pm2,5': 11.0, 'C6H6': 1.0}
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