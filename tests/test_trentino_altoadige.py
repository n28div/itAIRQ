import unittest
import datetime
from regions.trentino_altoadige import TrentinoAltoAdige

class TrentinoAltoAdigeTest(unittest.TestCase):
    region_cls = TrentinoAltoAdige
    air_quality = {
        'Trento': {'SO2': 3.83, 'NO2': 48.73, 'CO': 1.04, 'O3': 20.93, 'Pm10': 44.38, 'Pm2,5': 46.24, 'C6H6': None},
        'Bolzano': {'SO2': None, 'NO2': None, 'CO': None, 'O3': None, 'Pm10': None, 'Pm2,5': None, 'C6H6': None},
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