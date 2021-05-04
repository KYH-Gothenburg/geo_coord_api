from flask import Flask, request, json
import random
from geo_bounding import country_bounding_boxes

app = Flask(__name__)

def api_error(error_msg):
    return app.response_class(
        response=json.dumps({'error': error_msg}),
        status=400,
        mimetype='application/json'
    )


@app.route('/api/v1.0/coords', methods=['GET'])
def get_coords():
    country = request.args.get('country')
    if not country:
        return api_error('You must provide a country code.')
    else:
        country = country.upper()

    num_steps = request.args.get('num_steps')

    if not num_steps:
        num_steps = 10
    else:
        try:
            num_steps = abs(int(num_steps))
        except ValueError:
            return api_error(f'Argument num_steps must be an integer value. You passed {num_steps}.')
    try:
        country_data = country_bounding_boxes[country]
    except KeyError:
        return api_error(f'Country with country code {country} does not exist.')

    south_lng = country_data[1][0]
    south_lat = country_data[1][1]
    north_lng = country_data[1][2]
    north_lat = country_data[1][3]
    lat = round(random.triangular(south_lat, north_lat), 6)
    lng = round(random.triangular(south_lng, north_lng), 6)
    coords = [f'{lng}, {lat}']
    for _ in range(num_steps-1):
        dst = 0.0001
        lat_move = random.choice([-1, 1, 0])
        lng_move = random.choice([-1, 1, 0])
        lat += dst * lat_move
        lng += dst * lng_move
        coords.append(f'{round(lng, 6)}, {round(lat, 6)}')
    return app.response_class(
        response=json.dumps({'path': coords}),
        status=200,
        mimetype='application/json'
    )


if __name__ == '__main__':
    app.run()