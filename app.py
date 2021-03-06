import settings
from flask import Flask, request, jsonify, abort, url_for, Response, render_template
from flask_cors import CORS
from cache import Cache
from fetcher import Fetcher
from datetime import datetime, timedelta
from regions import regions_list
from regions.quality import AirQuality
from statistics import mean
import json
import threading
import re
import logging
from flask_apscheduler import APScheduler
from datetime import datetime

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = settings.flask['SECRET_KEY']
# Setup cors header
CORS(app)

cache = Cache()
fetcher = Fetcher(cache)

def absolute_url_for(url_name: str, date: datetime, **values) -> str:
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

def filter_regions(regions: list, wanted_regions: list) -> list:
    """
    Filters out the unwanted regions

    :param regions: All the regions
    :param wanted_regions: A list of wanted regions
    :return: The air quality of the wanted regions
    """
    wanted_regions_names = [x.name.lower() for x in wanted_regions]
    filtered = [x for x in regions if x['name'].lower() in wanted_regions_names]
    return filtered

def append_absolute_url(regions: list, date:datetime) -> list:
    """
    Append the absolute url to each region
    :param regions: The list of region
    :param date: The date of interest
    :return: A new list with the newly added informations
    """
    for region in regions:
        region['href'] = absolute_url_for('regional_data', 
            date, 
            region_name=region['name'])

        for province in region['provinces']:
            province['href'] = absolute_url_for('provincial_data', 
                date, 
                region_name=region['name'],
                province_name=province['short'])
    
    return regions

# Scheduled jobs
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
scheduler_last_run = None

@scheduler.task('interval', id='refresh_data', seconds=settings.data['REFRESH_INTERVAL'])
def refresh_regions_data():
    """
    Refresh data about today, yesterday and the day before yesterday
    """
    scheduler_last_run = datetime.now()
    days = [
        datetime.now(),
        datetime.now() - timedelta(days=1),
        datetime.now() - timedelta(days=2)
    ]

    logging.info('Refreshing data')
    
    for day in days:
        fetcher.fetch_day_high_priority(day)

@app.route('/', methods=['GET'])
def index():
    """
    Index HTML page with informations about the status
    """
    context = {
        'available_dates': [datetime.strptime(x, '%Y%m%d') for x in sorted(cache.keys)],
        'available_regions': sorted([x.name for x in regions_list]),
        'last_automatic_update': scheduler_last_run,
        'pending_updates': fetcher.pending
    }
    return render_template('index.html', **context)

@app.route('/api/v1/dates', methods=['GET'])
def dates():
    """
    Endpoint available dates
    """
    return jsonify([datetime.strptime(x, '%Y%m%d').strftime('%Y-%m-%d') for x in cache.keys])

@app.route('/api/v1/<int:year>/<int:month>/<int:day>', methods=['GET'])
def national_data(year, month, day):
    """
    Endpoint for national data
    """
    date = datetime(year=year, month=month, day=day)

    # get quality of all region
    try:
        regions = append_absolute_url(fetcher.fetch_day(date), date)
    except cache.NotInCacheException:
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
        regions = append_absolute_url(fetcher.fetch_day(date), date)
        region = filter_regions(regions, [chosen_region])[0]
    except cache.NotInCacheException:
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
    chosen_region = next((x for x in regions_list if x.name.lower() == region_name), None)
    if chosen_region is None:
        abort(404)
    
    # Get the quality of the region
    try:
        regions = append_absolute_url(fetcher.fetch_day(date), date)
        region = filter_regions(regions, [chosen_region])[0]
    except cache.NotInCacheException:
        return Response(status=202)
    except ValueError:
        abort(400) # date is in the future

    province = next(
        (p for p in region['provinces'] 
         if p['name'].lower() == province_name.lower() or
            p['short'].lower() == province_name.lower()), 
         None)

    if province is None: abort(404)
    
    return jsonify(province)

if __name__ == '__main__':
    app.run(debug=settings.DEBUG)