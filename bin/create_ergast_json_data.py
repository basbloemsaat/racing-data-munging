#!/usr/bin/env python

import json
import os
from pathlib import Path
import sqlite3

from pprint import pprint
from dumper import dump

ergastsqlite = os.path.join(os.path.dirname(
    __file__), "../../racing-data-munging-prv/ergast/ergast_sqlite3.db")
uri = 'file:' + ergastsqlite + '?mode=ro'

db = sqlite3.connect(uri, uri=True)
db.isolation_level = None


def save_to_json(data, json_file):
    path = os.path.join(os.path.dirname(__file__),
                        "../data/ergast/", json_file)
    print('saving ' + path)
    with open(path, 'w') as outfile:
        json.dump(data, outfile)


def exec_query(query, args=[], json_file=None):
    c = db.cursor()
    c.execute(query, args)
    names = [d[0] for d in c.description]
    rows = [dict(zip(names, row)) for row in c.fetchall()]

    if json_file:
        save_to_json(rows, json_file)
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
    path_name = os.path.join(os.path.dirname(
        __file__), "../data/ergast/seasons/", str(season_year))
    p = Path(path_name)
    p.mkdir(
        mode=0o755,
        parents=True,
        exist_ok=True
    )

    season_overview = {}

    season_overview['driver_standings'] = exec_query(
        query='''
            SELECT 
                d.driverRef
                , d.forename
                , d.surname
                , d.nationality
                , SUM(re.points) AS points
                , SUM(CASE WHEN position=1 THEN 1 ELSE 0 END) as wins
                , SUM(CASE WHEN position IN (1,2,3) THEN 1 ELSE 0 END) AS podiums
            FROM
                drivers d
                JOIN results re ON re.driverId = d.driverId
                JOIN races ra ON ra.raceId = re.raceId
                
            WHERE ra.year = ?
            GROUP BY driverRef
            ORDER BY SUM(re.points) DESC
        '''
        , args = [season_year]
    )

    season_overview['constructor_standings'] = exec_query(
        query='''
            SELECT 
                constructorRef
                , t.name
                , t.nationality
                , SUM(re.points) AS points
                , SUM(CASE WHEN position=1 THEN 1 ELSE 0 END) AS wins
                , SUM(CASE WHEN position IN (1,2,3) THEN 1 ELSE 0 END) AS podiums
            FROM
                constructors t
                JOIN results re ON re.constructorId = t.constructorId
                JOIN races ra ON ra.raceId = re.raceId
            WHERE ra.year = ?
            GROUP BY constructorRef
            ORDER BY SUM(re.points) DESC
        '''
        , args = [season_year]
    )

    save_to_json(season_overview, 'seasons/' + str(season_year) + '/overview.json')

drivers = exec_query(
    query='''
        SELECT 
            d.driverId, d.driverRef, d.forename, d.surname, d.dob as date_of_birth, d.nationality, d.url
        FROM 
            drivers d
    '''
)

for driver in drivers:
    driver_id = driver['driverId']
    del driver['driverId']

    driver_years_active = exec_query(
        '''
            SELECT 
                ra.year
                , count(DISTINCT re.raceId) as races
                , SUM(CASE WHEN position=1 THEN 1 ELSE 0 END) as wins
                , SUM(CASE WHEN position IN (1,2,3) THEN 1 ELSE 0 END) podiums
            FROM 
                races ra
                LEFT JOIN results re ON re.raceId = ra.raceId
            WHERE re.driverId = ?
            GROUP BY ra.year
        ''',
        [driver_id]
    )

    driver['years_active'] = driver_years_active

save_to_json(drivers, 'drivers.json')

constructors = exec_query(
    query='''
        SELECT 
            c.constructorId, c.constructorRef, c.name, c.nationality, c.url
        FROM constructors c
    '''
)

for constructor in constructors:
    constructor_id = constructor['constructorId']
    del constructor['constructorId']

    constructor_years_active = exec_query(
        '''
            SELECT 
                ra.year
                , count(DISTINCT re.raceId) as races
                , SUM(CASE WHEN position=1 THEN 1 ELSE 0 END) as wins
                , SUM(CASE WHEN position IN (1,2,3) THEN 1 ELSE 0 END) podiums
            FROM 
                races ra
                LEFT JOIN results re ON re.raceId = ra.raceId
            WHERE re.constructorId = ?
            GROUP BY ra.year
        ''',
        [constructor_id]
    )

    constructor['years_active'] = constructor_years_active

save_to_json(constructors, 'constructors.json')
