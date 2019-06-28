import unittest
import datetime
from regions.puglia import Puglia

class PugliaTest(unittest.TestCase):
    region_cls = Puglia
    air_quality = {
        'Bari': {'SO2': None, 'NO2': 23.0, 'CO': 0.12, 'O3': 56.2, 'Pm10': 13.07, 'Pm2,5': 5.86, 'C6H6': 0.0},
        'Barletta-Andria-Trani': {'SO2': None, 'NO2': None, 'CO': None, 'O3': None, 'Pm10': None, 'Pm2,5': None, 'C6H6': None},
        'Brindisi': {'SO2': 2.78, 'NO2': 12.75, 'CO': 0.0, 'O3': 63.67, 'Pm10': 11.6, 'Pm2,5': 8.5, 'C6H6': 0.17},
        'Foggia': {'SO2': 1.0, 'NO2': 16.29, 'CO': 0.4, 'O3': 67.0, 'Pm10': 9.29, 'Pm2,5': 8.33, 'C6H6': 0.0},
        'Lecce': {'SO2': 6.5, 'NO2': 22.71, 'CO': 0.0, 'O3': 65.75, 'Pm10': 13.62, 'Pm2,5': 7.17, 'C6H6': None},
        'Taranto': {'SO2': 3.62, 'NO2': 23.1, 'CO': 0.0, 'O3': 64.0, 'Pm10': 11.1, 'Pm2,5': 10.0, 'C6H6': 0.2}
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