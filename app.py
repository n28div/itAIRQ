from flask import Flask, request, jsonify, abort
import settings
from datetime import datetime
from regions import regions_list
from regions.quality import AirQuality

app = Flask(__name__)
app.secret_key = settings.flask['SECRET_KEY']

@app.route('/api/v1/national', methods=['GET'])
def national_data():
    """
    Endpoint for national data
    """
    response = list() # response is a list of JSON object
    
    if 'date' in request.args:
        date = datetime.strptime(request.args['date'], '%Y-%m-%d')

        if date > datetime.now(): abort(400)
    else:
        date = datetime.now()

    # Create all the regions instances
    regions = [r() for r in regions_list]

    # Ask to all the regions to fetch the data
    for r in regions:
        r.fetch_air_quality(date)
    
    # gather results from all regions
    for r in regions:
        r.wait_for_quality()
        region_res = dict()
        region_res['name'] = r.name
        region_res['provinces'] = [{'name': p.name, 'short': p.short_name} for p in r.provinces]
        region_quality = dict()

        air_quality = [p.quality for p in r.provinces]
        attributes = air_quality[0].__dict__.keys()

        for attribute in attributes:
            attributes_values = [getattr(q, attribute) for q in air_quality]
            # remove None values, if present
            attributes_values = [x for x in attributes_values if x is not None]

            if len(attributes_values) > 0:
                region_quality[attribute] = round(sum(attributes_values) / len(attributes_values), 2)
            else:
                region_quality[attribute] = None
            
        region_res['quality'] = region_quality
        response.append(region_res)

    return jsonify(response)

@app.route('/api/v1/<string:region_name>')
def regional_data(region_name):
    """
    Endpoint for regional data
    """
    region_name = region_name.lower()
    region = next((x for x in regions_list if x.name.lower() == region_name), None)
    if region is None:
        abort(404)
    else:
        # istantiate region
        region = region()

    if 'date' in request.args:
        date = datetime.strptime(request.args['date'], '%Y-%m-%d')
        if date > datetime.now(): abort(400)
    else:
        date = datetime.now()

    # Get the quality of the region
    region.fetch_air_quality(date)
    region.wait_for_quality()

    response = [
        {'name': p.name, 'short': p.short_name, 'quality': p.quality.asdict()}
        for p in region.provinces
    ]
    
    return jsonify(response)

@app.route('/api/v1/<string:region_name>/<string:province_name>')
def provincial_data(region_name, province_name):
    """
    Endpoint for province data
    """
    region_name = region_name.lower()
    region = next((x for x in regions_list if x.name.lower() == region_name), None)
    if region is None:
        abort(404)
    else:
        # istantiate region
        region = region()

    if 'date' in request.args:
        date = datetime.strptime(request.args['date'], '%Y-%m-%d')
        if date > datetime.now(): abort(400)
    else:
        date = datetime.now()

    # Get the quality of the region
    region.fetch_air_quality(date)
    region.wait_for_quality()

    province = next(
        (p for p in region.provinces if p.name == province_name or p.short_name == province_name), 
        None)

    if province is None: abort(404)
    
    response = {
        'name': province.name,
        'short': province.short_name,
        'quality': province.quality.asdict()
    }
    
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=settings.DEBUG)