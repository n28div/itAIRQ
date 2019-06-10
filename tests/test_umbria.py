import unittest
import datetime
from regions.umbria import Umbria

class UmbriaTest(unittest.TestCase):
    region_cls = Umbria
    air_quality = {
        'Perugia': {'SO2': None, 'NO2': 56.67, 'CO': 0.5, 'O3': 60.5, 'Pm10': 21.0, 'Pm2,5': 17.67, 'C6H6': 21.0},
        'Terni': {'SO2': 7.0, 'NO2': 53.8, 'CO': 0.5, 'O3': 73.67, 'Pm10': 36.4, 'Pm2,5': 33.0, 'C6H6': 36.4}
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