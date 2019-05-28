import unittest
import datetime
from regions.lombardia import Lombardia

class LombardiaTest(unittest.TestCase):
    region_cls = Lombardia
    air_quality = {
        'Bergamo': {'SO2': 1.46, 'NO2': 65.84, 'O3': 6.75, 'Pm10': 71.29, 'Pm2,5': 60.2, 'C6H6': 1.73},
        'Brescia': {'SO2': 1.51, 'NO2': 74.89, 'O3': 15.02, 'Pm10': 58.8, 'Pm2,5': 56.5, 'C6H6': 1.9},
        'Como': {'SO2': 2.91, 'NO2': 112.43, 'O3': 11.7, 'Pm10': 66.67, 'Pm2,5': 66.0, 'C6H6': 1.3},
        'Cremona': {'SO2': 1.76, 'NO2': 64.94, 'O3': 6.09, 'Pm10': 68.4, 'Pm2,5': 52.5, 'C6H6': 2.4},
        'Lecco': {'SO2': 1.52, 'NO2': 54.65, 'O3': 27.0, 'Pm10': 54.4, 'Pm2,5': 35.0, 'C6H6': 1.1},
        'Lodi': {'SO2': 4.13, 'NO2': 59.42, 'O3': 7.72, 'Pm10': 69.33, 'Pm2,5': 54.5, 'C6H6': 1.1},
        'Mantova': {'SO2': 2.08, 'NO2': 61.57, 'O3': 8.41, 'Pm10': 64.67, 'Pm2,5': 56.5, 'C6H6': 2.0},
        'Milano': {'SO2': 3.31, 'NO2': 91.31, 'O3': 5.89, 'Pm10': 93.29, 'Pm2,5': 74.33, 'C6H6': 2.88},
        'Monza e della Brianza': {'SO2': None, 'NO2': 67.03, 'O3': 5.65, 'Pm10': 88.0, 'Pm2,5': 55.0, 'C6H6': None},
        'Pavia': {'SO2': 3.24, 'NO2': 63.15, 'O3': 8.77, 'Pm10': 72.0, 'Pm2,5': 56.67, 'C6H6': 1.35},
        'Sondrio': {'SO2': 3.32, 'NO2': 74.0, 'O3': 20.22, 'Pm10': 53.0, 'Pm2,5': 65.0, 'C6H6': 1.65},
        'Varese': {'SO2': 1.63, 'NO2': 69.95, 'O3': 11.51, 'Pm10': 71.25, 'Pm2,5': 70.0, 'C6H6': None},
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