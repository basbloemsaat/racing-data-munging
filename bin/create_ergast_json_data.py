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


def query2json(query, args=[], json_file=None):
    c = db.cursor()
    c.execute(query)

    result = c.fetchall()

    if json_file:
        path = os.path.join(os.path.dirname(__file__),
                            "../data/ergast/", json_file)
        with open(path, 'w') as outfile:
            json.dump(result, outfile)

    return result


seasons = query2json(
    query='''
        SELECT s.year, s.url, count(r.raceId) as races
        FROM 
            seasons s
            JOIN races r ON r.year=s.year
        GROUP BY s.year
    ''',
    json_file='seasons.json'
)

for season in seasons:
    season_year = season[0]
    p = Path(
        os.path.join(os.path.dirname(__file__), "../data/ergast/seasons/", str(season_year)))
    p.mkdir(
        mode=0o666,
        parents=True,
        exist_ok=True
    )
