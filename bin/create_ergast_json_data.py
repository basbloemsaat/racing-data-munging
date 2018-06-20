#!/usr/bin/env python

import json
import os
from pathlib import Path
import sqlite3

from pprint import pprint
from dumper import dump

ergastsqlite = os.path.join(os.path.dirname(
    __file__), "../data/ergast/ergast_sqlite3.db")
uri = 'file:' + ergastsqlite + '?mode=ro'

db = sqlite3.connect(uri, uri=True)
db.isolation_level = None


def exec_query(query, args=[], json_file=None):
    c = db.cursor()
    c.execute(query)
    names = [d[0] for d in c.description]
    rows = [dict(zip(names, row)) for row in c.fetchall()]

    if json_file:
        path = os.path.join(os.path.dirname(__file__),
                            "../data/ergast/", json_file)
        with open(path, 'w') as outfile:
            json.dump(rows, outfile)

    return rows


seasons = exec_query(
    query='''
        SELECT 
            ra.year
            , count(DISTINCT d.driverId) as winners
            , count(DISTINCT ra.raceId) as races
            , s.url
        FROM 
            seasons s 
            JOIN races ra ON ra.year=s.year
            LEFT JOIN results re ON re.raceId = ra.raceId AND re.position=1
            LEFT JOIN drivers d ON d.driverId = re.driverId
        GROUP BY ra.year
        ORDER BY ra.year
    ''',
    json_file='seasons.json'
)

for season in seasons:
    season_year = season['year']
    p = Path(
        os.path.join(os.path.dirname(__file__), "../data/ergast/seasons/", str(season_year)))
    p.mkdir(
        mode=0o666,
        parents=True,
        exist_ok=True
    )
