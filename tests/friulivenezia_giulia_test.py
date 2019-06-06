import unittest
import datetime
from regions.friulivenezia_giulia import FriuliVeneziaGiulia

class FriuliVeneziaGiuliaTest(unittest.TestCase):
    region_cls = FriuliVeneziaGiulia
    air_quality = {
        'Gorizia': {'SO2': 3.16, 'NO2': 47.56, 'CO': None, 'O3': 61.81, 'Pm10': 22.1, 'Pm2,5': 21.8, 'C6H6': None},
        'Pordenone': {'SO2': None, 'NO2': 42.84, 'CO': None, 'O3': 48.04, 'Pm10': 44.19, 'Pm2,5': None, 'C6H6': None},
        'Trieste': {'SO2': 8.1, 'NO2': 58.24, 'CO': 0.48, 'O3': None, 'Pm10': 17.9, 'Pm2,5': 12.25, 'C6H6': None},
        'Udine': {'SO2': 0.28, 'NO2': 50.71, 'CO': None, 'O3': 51.71, 'Pm10': 30.02, 'Pm2,5': 34.5, 'C6H6': None},
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