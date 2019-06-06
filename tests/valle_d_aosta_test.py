import unittest
import datetime
from regions.valle_d_aosta import ValleDAosta

class ValleDAostaTest(unittest.TestCase):
    region_cls = ValleDAosta
    air_quality = {
        'Aosta': {'SO2': 12.0, 'NO2': 43.42, 'CO': 0.8, 'O3': 53.88, 'Pm10': 27.8, 'Pm2,5': 25.0, 'C6H6': 2.2},    
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