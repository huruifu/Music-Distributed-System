"""
SFU CMPT 756
Sample application---playlist service.
"""

# Standard library modules
import logging
import random
import sys

# Installed packages
from flask import Blueprint
from flask import Flask
from flask import request
from flask import Response

from prometheus_flask_exporter import PrometheusMetrics

import requests

import simplejson as json

# Local modules

# Integer value 0 <= v < 100, denoting proportion of
# calls to `get_song` to return 500 from
PERCENT_ERROR = 50

# The application

app = Flask(__name__)

metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Playlist process')

db = {
    "name": "http://cmpt756db:30002/api/v1/datastore",
    "endpoint": [
        "read",
        "write",
        "delete",
        "update"
    ]
}

bp = Blueprint('app', __name__)


@bp.route('/health')
@metrics.do_not_track()
def health():
    return Response("", status=200, mimetype="application/json")


@bp.route('/readiness')
@metrics.do_not_track()
def readiness():
    return Response("", status=200, mimetype="application/json")

@bp.route('/<playlist_id>', methods=['GET'])
def get_playlist(playlist_id):
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    payload = {"objtype": "playlist", "objkey": playlist_id}
    url = db['name'] + '/' + db['endpoint'][0]
    response = requests.get(
        url,
        params=payload,
        headers={'Authorization': headers['Authorization']})
    return (response.json())

@bp.route('/', methods=['POST'])
def create_playlist():
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    try:
        content = request.get_json()
        playlist_name = content["playlist_name"]
        music_id_list = content['music_id_list']
    except Exception:
        return Response(json.dumps({"message": "error reading arguments"}), status=400)
    url = db['name'] + '/' + db['endpoint'][1]
    response = requests.post(
        url,
        json={"objtype": "playlist", "playlist_name": playlist_name, "music_id_list": music_id_list},
        headers={'Authorization': headers['Authorization']})
    return (response.json())

@bp.route('/<playlist_id>', methods=['DELETE'])
def delete_playlist(playlist_id):
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    url = db['name'] + '/' + db['endpoint'][2]
    response = requests.delete(
        url,
        params={"objtype": "playlist", "objkey": playlist_id},
        headers={'Authorization': headers['Authorization']})
    return (response.json())

@bp.route('playlist-name/<playlist_id>', methods=['PUT'])
def update_playlist_name(playlist_id):
    """_summary_
    Args:
        playlist_id (string): uuid of playlist
    Returns:
        object: an object containing status code
    """
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}), status=401,
                        mimetype='application/json')
    try:
        content = request.get_json()
        playlist_name = content['playlist_name']
    except Exception:
        return json.dumps({"message": "error reading arguments"})
    url = db['name'] + '/' + db['endpoint'][3]
    response = requests.put(
        url,
        params={"objtype": "playlist", "objkey": playlist_id},
        json={"playlist_name": playlist_name},
        headers={'Authorization': headers['Authorization']})
    return (response.json())

@bp.route('/add_song', methods=['PUT'])
def add_music_to_playlist():
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    try:
        body = request.get_json()
        playlist_id = body['playlist_id']
        music_id = body['music_id']
    except:
        return Response(json.dumps({"error": "Unable to get params"}),
                    status=400,
                    mimetype='application/json')
    payload = {"objtype": "playlist", "objkey": playlist_id}
    url = db['name'] + '/' + db['endpoint'][0]
    response = requests.get(
        url,
        params=payload,
        headers={'Authorization': headers['Authorization']})
    if response.status_code != 200:
        return Response(json.dumps({"error": "Failed to retrieve playlist"}),
                        status=502,
                        mimetype='application/json')
    items = response.json()
    music_id_list = items['Items'][0]['music_id_list']
    if music_id not in music_id_list:
        music_id_list.append(music_id)
    payload = {"objtype": "playlist", "objkey": playlist_id}
    url = db['name'] + '/' + db['endpoint'][3]
    response = requests.put(
        url,
        params=payload,
        json={"music_id_list": music_id_list})
    return (response.json())

@bp.route('/remove_song', methods=['PUT'])
def remove_music_from_playlist():
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    try:
        body = request.get_json()
        playlist_id = body['playlist_id']
        music_id = body['music_id']
    except:
        return Response(json.dumps({"error": "Unable to get params"}),
                    status=400,
                    mimetype='application/json')
    payload = {"objtype": "playlist", "objkey": playlist_id}

    url = db['name'] + '/' + db['endpoint'][0]
    response = requests.get(
        url,
        params=payload,
        headers={'Authorization': headers['Authorization']})
    if response.status_code != 200:
        return Response(json.dumps({"error": "Failed to retrieve playlist"}),
                        status=502,
                        mimetype='application/json')
    items = response.json()
    music_id_list = items['Items'][0]['music_id_list']
    if music_id in music_id_list:
        music_id_list.remove(music_id)
    payload = {"objtype": "playlist", "objkey": playlist_id}
    url = db['name'] + '/' + db['endpoint'][3]
    response = requests.put(
        url,
        params=payload,
        json={"music_id_list": music_id_list})
    return (response.json())

# All database calls will have this prefix.  Prometheus metric
# calls will not---they will have route '/metrics'.  This is
# the conventional organization.
app.register_blueprint(bp, url_prefix='/api/v1/playlist/')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error("missing port arg 1")
        sys.exit(-1)

    p = int(sys.argv[1])
    # Do not set debug=True---that will disable the Prometheus metrics
    app.run(host='0.0.0.0', port=p, threaded=True)