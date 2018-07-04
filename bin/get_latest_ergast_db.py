#!/usr/bin/env python

from datetime import datetime
from dateutil import parser
import json
import os
import requests
import shutil

url = "http://ergast.com/downloads/f1db.sql.gz"
status_file = os.path.join(os.path.dirname(__file__), "../../racing-data-munging-prv/ergast/state.json")

with open(status_file) as f:
    status = json.load(f)

resp = requests.head(url)
lastmod = resp.headers['Last-Modified']

lastmod_date = parser.parse(lastmod)
status_lastmod_date = parser.parse(status['last-modified'])

size = int(resp.headers['Content-Length'])
status_size = status['size']

if (lastmod_date > status_lastmod_date or size != status_size):
    print('Getting new ergast db');
    os.system('rm /tmp/f1db.sql')
    os.system('rm /tmp/f1db.sql.gz')

    try:
        resp = requests.get(url, stream=True)
        with open('/tmp/f1db.sql.gz', 'wb') as out_file:
            shutil.copyfileobj(resp.raw, out_file)

        os.system('gunzip /tmp/f1db.sql.gz -f')

        mysql2sqlite = os.path.join(os.path.dirname(__file__), "mysql2sqlite")
        ergastsqlite = os.path.join(os.path.dirname(__file__), "../../racing-data-munging-prv/ergast/ergast.sqlite3db")
        os.system('rm ' + ergastsqlite)
        os.system(mysql2sqlite + ' /tmp/f1db.sql | sqlite3 ' + ergastsqlite)

        status['size'] = size
        status['last-modified'] = lastmod
    except (RuntimeError, TypeError, NameError):
        pass
else:
    print('Already up to date, not refreshing')

with open(status_file, 'w') as outfile:
    json.dump(status, outfile)
