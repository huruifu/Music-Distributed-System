"""
SFU CMPT 756
Sample STANDALONE application---playlist service.
"""

# Standard library modules
from crypt import methods
import csv
import logging
import os
import sys
import uuid

# Installed packages
from flask import Blueprint
from flask import Flask
from flask import request

# Local modules
# import unique_code

# The path to the file (CSV format) containing the sample data
DB_PATH = '/data/playlist.csv'
MUSIC_DB_PATH = '/data/music.csv'

# The unique exercise code
# The EXER environment variable has a value specific to this exercise
# ucode = unique_code.exercise_hash(os.getenv('EXER'))

# The application

app = Flask(__name__)

bp = Blueprint('app', __name__)

database = {}

music_db = {}
            
def read_list(list_str):
    s = list_str[1:-1]
    return s.split(',')

def load_db():
    global database
    with open(DB_PATH, 'r') as inp:
        rdr = csv.reader(inp)
        next(rdr)  # Skip header line
        for name, musics, uuid in rdr:
            musics = read_list(musics)
            database[id] = (name, uuid, musics)

def load_music_db():
    global music_db
    with open(MUSIC_DB_PATH, 'r') as inp:
        rdr = csv.reader(inp)
        next(rdr)  # Skip header line
        for artist, songtitle, id in rdr:
            music_db[id] = (artist, songtitle)

@bp.route('/health')
def health():
    return ""


@bp.route('/readiness')
def readiness():
    return ""

@bp.route('/m_id=<music_id>', methods=['GET'])
def get_music_with_id(music_id):
    global music_db
    if music_id in music_db:
        value = music_db[music_id]
        response = {
            "Count": 1,
            "Items":
                [{'Artist': value[0],
                  'SongTitle': value[1],
                  'music_id': music_id}]
        }
    else:
        response = {
            "Count": 0,
            "Items": []
        }
        return app.make_response((response, 404))
    return response

@bp.route('/', methods=['GET'])
def list_all():
    global database
    response = {
        "Count": len(database),
        "Items":
            [{"playlist_name": value, "playlist_id": id}
             for id, value in database.items()]
    }
    return response


@bp.route('/', methods=['POST'])
def create_list():
    global database
    try:
        content = request.get_json()
        playlist_name = content['playlist_name']
        uid = content['uid']
        musics = []
    except Exception:
        return app.make_response(
            ({"Message": "Error reading arguments"}, 400)
            )
    playlist_id = str(uuid.uuid4())
    database[playlist_id] = (playlist_name, uid, musics)


@bp.route('/shutdown', methods=['GET'])
def shutdown():
    # From https://stackoverflow.com/questions/15562446/how-to-stop-flask-application-without-using-ctrl-c # noqa: E501
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return {}


app.register_blueprint(bp, url_prefix='/api/v1/playlist/')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error("missing port arg 1")
        sys.exit(-1)

    load_db()
    load_music_db()
    # app.logger.error("Unique code: {}".format(ucode))
    app.logger.info("app is now working ...")
    p = int(sys.argv[1])
    app.run(host='0.0.0.0', port=p, threaded=True)