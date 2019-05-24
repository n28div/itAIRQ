import asyncio
from datetime import datetime
from regions.valle_d_aosta import ValleDAosta

loop = asyncio.get_event_loop()
va = ValleDAosta()

loop.run_until_complete(va.fetch_air_quality(datetime(year=2019, month=1, day=1)))

# only one province
expected_air_quality = {
    'SO2': 12.0, 
    'NO2': 43.42, 
    'O3': 53.88, 
    'Pm10': 27.8, 
    'Pm2,5': 25.0, 
    'C6H6': 2.2
}

def test_air_quality_response():
    # only one province
    province = va.provinces[0]
    air_quality = province.quality.asdict()
    
    for key in air_quality.keys():
        assert air_quality[key] == expected_air_quality[key]