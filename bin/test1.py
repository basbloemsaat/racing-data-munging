#!/usr/bin/env python

import requests
from pprint import pprint
from dumper import dump

from datetime import datetime
from dateutil import parser

import shutil


url = "https://a.fsdn.com/sd/logo.png"
# url = "http://ergast.com/downloads/f1db.sql.gz"

resp = requests.head(url)
pprint(resp.headers)
pprint(resp.headers['Last-Modified'])

# dump(resp.headers)

lastmod = parser.parse(resp.headers['Last-Modified'])
size = int(resp.headers['Content-Length'])

pprint(lastmod)
pprint(size)

resp = requests.get(url, stream=True)
with open('/tmp/f1db.sql.gz', 'wb') as out_file:
    shutil.copyfileobj(resp.raw, out_file)

