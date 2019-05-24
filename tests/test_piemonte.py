from datetime import datetime
from regions.piemonte import Piemonte

r = Piemonte()
r.fetch_air_quality(datetime(year=2019, month=1, day=1))
r.wait_for_quality()

expected_air_quality = {
    'Alessandria': {'SO2': 4.0, 'NO2': 52.67, 'O3': 35.5, 'Pm10': 68.0, 'Pm2,5': 49.0, 'C6H6': 2.3},
    'Asti': {'SO2': 8.0, 'NO2': 48.33, 'O3': 21.5, 'Pm10': None, 'Pm2,5': None, 'C6H6': 3.3},
    'Biella': {'SO2': None, 'NO2': 46.5, 'O3': 40.67, 'Pm10': 31.0, 'Pm2,5': 27.0, 'C6H6': 1.65},
    'Cuneo': {'SO2': 10.0, 'NO2': 41.33, 'O3': 25.25, 'Pm10': 51.0, 'Pm2,5': 44.0, 'C6H6': 1.77},
    'Novara': {'SO2': 14.5, 'NO2': 47.67, 'O3': 34.17, 'Pm10': 76.0, 'Pm2,5': 69.0, 'C6H6': 2.72},
    'Torino': {'SO2': 13.5, 'NO2': 56.81, 'O3': 25.0, 'Pm10': 64.0, 'Pm2,5': 59.0, 'C6H6': 2.29},
    'Vercelli': {'SO2': 4.0, 'NO2': 45.75, 'O3': 28.5, 'Pm10': 59.0, 'Pm2,5': 54.0, 'C6H6': 1.9},
    'Verbano-Cusio-Ossola': {'SO2': None, 'NO2': None, 'O3': None, 'Pm10': None, 'Pm2,5': None, 'C6H6': None}
}


def test_air_quality_response():
    for province in r.provinces:
        quality = province.quality.asdict()
        expected = expected_air_quality[province.name]

        for key in expected.keys():
            assert quality[key] == expected[key]
