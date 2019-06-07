from flask import Flask, request, jsonify, abort, url_for
import settings
from datetime import datetime
from regions import regions_list
from regions.quality import AirQuality
from statistics import mean

app = Flask(__name__)
app.secret_key = settings.flask['SECRET_KEY']

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

def region_air_quality(date: datetime, regions: list) -> list:
    """
    :param regions: Regions of interest
    :return: A list of dict representing the air quality of each region
    """
    response = list()

    if date > datetime.now():
        raise ValueError('Date is in the future!')

    regions = [r() for r in regions]

    # fetch air quality of each region
    for r in regions:
        r.fetch_air_quality(date)
    
    # gather results from all regions
    for r in regions:
        # wait until region has fetched his data
        r.wait_for_quality()

        region_res = dict()
        region_res['name'] = r.name
        region_res['href'] = absolute_url_for('regional_data', date, region_name=r.name.lower())
        # set provinces quality
        region_res['provinces'] = [
            {
                'name': p.name, 
                'short': p.short_name,
                'quality': p.quality.asdict(), 
                'href': absolute_url_for('provincial_data', 
                                         date,
                                         region_name=r.name.lower(),
                                         province_name=p.short_name.lower())
            } 
            for p in r.provinces
        ]
        
        response.append(region_res)

    return response

@app.route('/api/v1/<int:year>/<int:month>/<int:day>/', methods=['GET'])
def national_data(year, month, day):
    """
    Endpoint for national data
    """
    response = list()
    date = datetime(year=year, month=month, day=day)

    # get quality of all region
    try:
        regions = region_air_quality(date, regions_list)
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
    region = next((x for x in regions_list if x.name.lower() == region_name), None)
    if region is None:
        abort(404)
    
    # Get the quality of the region
    return jsonify(region_air_quality(date, [region])[0])

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
        region = region_air_quality(date, [region])[0]
    except ValueError:
        abort(400) # date is in the future

    province = next(
        (p for p in region['provinces'] if p['name'].lower() == province_name or p['short'].lower() == province_name), 
         None)

    if province is None: abort(404)
    
    return jsonify(province)


if __name__ == '__main__':
    app.run(debug=settings.DEBUG)