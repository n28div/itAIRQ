from flask import Flask, request, jsonify, abort, url_for, Response
import settings
from datetime import datetime, timedelta
from regions import regions_list
from regions.quality import AirQuality
from statistics import mean
import redis
import json
import threading
import re
import logging
from flask_apscheduler import APScheduler

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = settings.flask['SECRET_KEY']

redis_server = redis.Redis(host=settings.redis['URL'], 
                           port=settings.redis['PORT'], db=settings.redis['DB'])
redis_mutex = threading.Lock()

class NotInCacheException(Exception):
    pass

def absolute_url_for(url_name: str, date, **values) -> str:
    """
    Calculate the absolute url for url_name joined with values

    :param url_name: The url name
    :param **values: The values required by url_for
    :return: The absolute url
    """
    with app.app_context():
        day = date.strftime('%d')
        month = date.strftime('%m')
        year = date.strftime('%Y')
        return request.url_root[:-1] + url_for(url_name, day=day, month=month, year=year, **values)

def fetch_region_air_quality(date:datetime) -> list:
    """
    Fetch air quality of each region and saves it into the cache running the routine in a separate thread

    :param date: The date of interest
    :return: A list of dict representing the air quality of each region    
    """
    def runtime(date):
        if date > datetime.now():
            raise ValueError('Date is in the future!')

        regions = [r() for r in regions_list]

        air_quality = list()
        
        # fetch air quality of each region
        for r in regions:
            r.fetch_air_quality(date)
        
        # gather results from all regions
        for r in regions:
            # wait until region has fetched his data
            r.wait_for_quality()
            logging.info('Fetched %s', r.name)
            air_quality.append({
                'name': r.name,
                'provinces': [
                    {'name': x.name, 'short': x.short_name, 'quality': x.quality.asdict()} 
                    for x in r.provinces]
            })

        # check if cache is full
        today_fmt = datetime.now().strftime('%Y%m%d')
        yesterday_fmt = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
        beforeyesterday_fmt = (datetime.now() - timedelta(days=2)).strftime('%Y%m%d')
        with redis_mutex:
            info_memory = redis_server.execute_command('info memory').decode('utf8')
            used_bytes = re.findall(r'used_memory:([0-9]*[.]*[0-9]+)', info_memory)[0]
            used_megabytes = int(used_bytes) / 10**6

            if used_megabytes >= settings.redis['MEMORY']:
                # a result needs to be deleted
                min_date = None
                for date in redis_server.scan_iter():
                    if min_date is None or (date < min_date and date != today_fmt and date != yesterday_fmt and date != beforeyesterday_fmt):
                        min_date = date
                
                redis_server.delete(min_date)

        date_fmt = date.strftime('%Y%m%d')
        with redis_mutex:
            redis_server.set(date_fmt, json.dumps(air_quality))

    thread = threading.Thread(target=runtime, args=(date,))
    thread.start()

def get_regions_air_quality(date: datetime, regions: list) -> list:
    """
    :param regions: Regions of interest
    :return: A list of dict representing the air quality of each region
    """
    response = list()

    if date > datetime.now():
        raise ValueError('Date is in the future!')

    # Check if requested date is available in cache otherwise start fetching it and throw exception
    with redis_mutex:
        regions_dict = redis_server.get(date.strftime('%Y%m%d'))
        
    if regions_dict is None:
        fetch_region_air_quality(date)
        raise NotInCacheException()
    else:
        regions = json.loads(regions_dict)

    for r in regions:
        r['href'] = absolute_url_for('regional_data', date, region_name=r['name'].lower())
        # set provinces quality
        for p in r['provinces']:
            p['href'] = absolute_url_for('provincial_data', 
                                         date,
                                         region_name=r['name'].lower(),
                                         province_name=p['short'].lower())

    return regions

@app.route('/api/v1/<int:year>/<int:month>/<int:day>/', methods=['GET'])
def national_data(year, month, day):
    """
    Endpoint for national data
    """
    response = list()
    date = datetime(year=year, month=month, day=day)

    # get quality of all region
    try:
        regions = get_regions_air_quality(date, regions_list)
    except NotInCacheException:
        return Response(status=202)
    except ValueError:
        abort(400)

    return jsonify(regions)

@app.route('/api/v1/<int:year>/<int:month>/<int:day>/<string:region_name>')
def regional_data(year, month, day, region_name):
    """
    Endpoint for regional data
    """
    date = datetime(year=year, month=month, day=day)    
    
    region_name = region_name.lower()
    chosen_region = next((x for x in regions_list if x.name.lower() == region_name), None)
    if chosen_region is None:
        abort(404)
    
    try:
        region = get_regions_air_quality(date, [chosen_region])[0]
    except NotInCacheException:
        return Response(status=202)
    except ValueError:
        abort(400)

    return jsonify(region)

@app.route('/api/v1/<int:year>/<int:month>/<int:day>/<string:region_name>/<string:province_name>')
def provincial_data(year, month, day, region_name, province_name):
    """
    Endpoint for province data
    """
    date = datetime(year=year, month=month, day=day)

    region_name = region_name.lower()
    region = next((x for x in regions_list if x.name.lower() == region_name), None)
    if region is None:
        abort(404)
    
    # Get the quality of the region
    try:
        region = get_regions_air_quality(date, [region])[0]
    except NotInCacheException:
        return Response(status=202)
    except ValueError:
        abort(400) # date is in the future

    province = next(
        (p for p in region['provinces'] if p['name'].lower() == province_name or p['short'].lower() == province_name), 
         None)

    if province is None: abort(404)
    
    return jsonify(province)

# Scheduled jobs
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

@scheduler.task('interval', id='refresh_data', seconds=settings.data['REFRESH_INTERVAL'])
def refresh_regions_data():
    """
    Refresh data about today, yesterday and the day before yesterday
    """
    days = [
        datetime.now(),
        datetime.now() - timedelta(days=1),
        datetime.now() - timedelta(days=2)
    ]

    logging.info('Refreshing data')
    
    for day in days:
        fetch_region_air_quality(day)

if __name__ == '__main__':
    app.run(debug=settings.DEBUG)