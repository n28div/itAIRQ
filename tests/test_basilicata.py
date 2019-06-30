import unittest
import datetime
from regions.basilicata import Basilicata

class BasilicataTest(unittest.TestCase):
    region_cls = Basilicata
    air_quality = {
        'Matera': {'SO2': 6.5, 'NO2': 21.0, 'CO': 0.0, 'O3': 66.33, 'Pm10': None, 'Pm2,5': None, 'C6H6': 0.33},
        'Potenza': {'SO2': 5.89, 'NO2': 9.38, 'CO': 0.0, 'O3': 69.86, 'Pm10': 7.67, 'Pm2,5': 4.2, 'C6H6': 0.14}
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