"""
This module comprises the ETL system for the "Cuarto de Milla" project, and is
in charge of processing Gas Station datasets into a clean structure and then
insert records into a database
"""

import os
import sys
import time
import random
import requests
import traceback
import numpy as np
import pandas as pd
import geopandas as gpd
import sqlalchemy as db
import xmltodict as x2d
import lxml.html as html
from pathlib import Path
from datetime import timedelta, datetime
from timeit import default_timer as timer
from sqlalchemy.dialects.postgresql import Insert as insert_stmt


BASE_DIR = Path(__file__).resolve().parent
URL_SOURCES = [
    'https://publicacionexterna.azurewebsites.net/publicaciones/places',
    'https://publicacionexterna.azurewebsites.net/publicaciones/prices'
]
DB_STRING = os.environ['DATABASE_URL']
STATIONS_TABLE_NAME = 'gasoline_station'
PRICES_TABLE_NAME = 'gasoline_price'
DATA_FOLDER = f'{BASE_DIR}/data'
GEO_FOLDER = f'{DATA_FOLDER}/geodata'
DATASET_FILES = [f'{DATA_FOLDER}/places.xml', f'{DATA_FOLDER}/prices.xml']
GEO_FILE = f'{GEO_FOLDER}/MEX_adm2.shp'
DF_COLS = ['place_id', 'name', 'cre_id', 'longitude', 'latitude', 'regular_price',
           'diesel_price', 'premium_price']
N_STATES = 3
N_ROWS = 2250

def get_state_prices():
    """
    Attempts to retrieve a dictionary with the states of Mexico and it prices for
    gasoline magna, premium and diesel with the following format:
    {'name_state':{'magna':18.80, 'premium':19.76, 'diesel':20.98}'name_state_2'...}
    website (deleting first any previously existing file)
    """
    url = 'http://www.gasolinamx.com/tabla-del-precio-de-la-gasolina-en-mexico'
    XPATH_STATES = '//table[@class="table table-bordered table-striped"]/tbody/tr/td/a/text()'
    XPATH_PRICES = '//table[@class="table table-bordered table-striped"]/tbody/tr/td/text()'
    try:
        response = requests.get(url)
        r = response.content.decode('utf-8')
        parsed = html.fromstring(r)
        print('Successful request')
        states = parsed.xpath(XPATH_STATES)
        prices = parsed.xpath(XPATH_PRICES)
        gas_type_prices = []

        i=0
        print('Creating dictionary...........')
        for state in states:
            j = i + 1
            k = i + 2
            state = dict(mangna=float(prices[i]), premium=float(prices[j]), diesel=float(prices[k]))
            gas_type_prices.append(state)
            i += 3
        state_prices = dict(zip(states, gas_type_prices))
        print('Dictionary completed')

        return state_prices
    except ValueError as ve:
        print('A problem ocurred in the state_prices, try again',ve)


def get_dataset(index):
    """
    Attempts to retrieve the dataset file with the specified index from the source
    website (deleting first any previously existing file)
    """
    try:
        print('Deleting previous files...')
        os.remove(DATASET_FILES[index])
    except FileNotFoundError:
        pass

    try:
        print(f'Retrieving {URL_SOURCES[index]}')
        response = requests.get(URL_SOURCES[index], allow_redirects=True)

        if response.status_code != 200:
            raise Exception(f'Could not retrieve anything from {URL_SOURCES[index]}')

        with open(DATASET_FILES[index], mode='wb') as new_file:
            new_file.write(response.content)
    except Exception as e:
        print(e)
        sys.exit(1)


def create_price_data(record, primary_key, price_type):
    """
    Creates a dictionary for the record according to the specified price type
    Returns the dictionary or None if the record doesn't have that price type
    """
    price_key = f'{price_type}_price'
    if pd.notna(record[price_key]):
        return {
            'gas_type': price_type,
            'price': record[price_key],
            'date': datetime.now(),
            'station_id': primary_key
        }
    else:
        return None


def extract():
    """
    Extract stage. Returns a tuple with:
        GeoDataFrame of retrieved stations from datasets
        GeoDataFrame of cities from local DIVA-GIS data
        GeoDataFrame of states from local DIVA-GIS data
    """
    stations_df = extract_stations()
    geo_gdf = gpd.read_file(GEO_FILE)
    return stations_df, geo_gdf


def extract_stations():
    """
    Obtains dataset files of places and prices from the source website and then
    loads it into a Pandas DataFrame, which is returned
    """
    get_dataset(0)
    get_dataset(1)

    places_and_prices = {}

    with open(DATASET_FILES[0], encoding='utf8') as dataset:
        xml_tree = x2d.parse(dataset.read())

        places_list = xml_tree['places']['place']

        for place in places_list:
            pid = int(place['@place_id'])

            if not places_and_prices.get(pid):
                places_and_prices[pid] = {}

            places_and_prices[pid]['name'] = place['name']
            places_and_prices[pid]['cre_id'] = place['cre_id']
            places_and_prices[pid]['longitude'] = place['location']['x']
            places_and_prices[pid]['latitude'] = place['location']['y']

    with open(DATASET_FILES[1], encoding='utf8') as dataset:
        xml_tree = x2d.parse(dataset.read(), force_list=('gas_price',))

        prices_list = xml_tree['places']['place']

        for price in prices_list:
            pid = int(price['@place_id'])

            if not places_and_prices.get(pid):
                places_and_prices[pid] = {}

            gas_prices = price['gas_price']

            for g_price in gas_prices:
                places_and_prices[pid][f'{g_price["@type"]}_price'] = float(
                    g_price['#text'])

    return pd.DataFrame.from_dict(places_and_prices, orient='index')


def reverse_geocode(stations_df, geo_gdf):
    """
    Performs reverse geocoding on stations_gdf against the DIVA-GIS data to obtain
    city and state information

    Returns the stations GeoDataFrame with new columns for city and state
    """
    stations_gdf = gpd.GeoDataFrame(stations_df, geometry=gpd.points_from_xy(stations_df.longitude, stations_df.latitude)).set_crs(epsg=4326)
    stations_geo_gdf = gpd.sjoin(stations_gdf, geo_gdf[['NAME_1', 'NAME_2', 'geometry']])
    stations_geo_gdf = stations_geo_gdf.rename(columns={'NAME_1': 'state', 'NAME_2': 'city'})
    return stations_geo_gdf


def get_states_with_most_rows(gdf, n):
    """
    Retrieves a list of the 'n' states with the highest count of rows
    """
    counts = gdf.groupby('state').size().reset_index(name='counts') \
            .sort_values('counts').tail(n)['state'].values

    return counts


def transform(stations_df, geo_gdf):
    """
    This function cleans the gas stations dataframe in order to obtain records
    with at least one gas type price and correct values

    It returns the representation of the cleaned dataframe as a list of dictionaries
    """
    print('Cleaning and packing data...')

    stations_complete_data_df = stations_df[stations_df['latitude'].notna() & stations_df['longitude'].notna() &
        (stations_df['regular_price'].notna() | stations_df['premium_price'].notna() | stations_df['diesel_price'].notna())].copy()

    bad_records = stations_complete_data_df[(stations_complete_data_df['regular_price'] <= 1) |
        (stations_complete_data_df['diesel_price'] <= 1) | (stations_complete_data_df['premium_price'] <= 1) |
        (stations_complete_data_df['regular_price'] >= 40) | (stations_complete_data_df['diesel_price'] >= 40) |
        (stations_complete_data_df['premium_price'] >= 40)]

    stations_complete_data_df.drop(bad_records.index, inplace=True)

    stations_complete_data_df.index.names = ['id']

    stations_geo_gdf = reverse_geocode(stations_complete_data_df, geo_gdf)

    frequent_states = get_states_with_most_rows(stations_geo_gdf, N_STATES)

    return stations_geo_gdf[stations_geo_gdf['state'].isin(frequent_states)].reset_index()[:N_ROWS].to_dict('records')


def load(stations_dict):
    """
    Loads the information in the data structure stations_dict to the database
    """
    print(f'Connecting to the database...')

    engine = db.create_engine(DB_STRING)
    metadata = db.MetaData()
    prices_table = db.Table(
        PRICES_TABLE_NAME, metadata, autoload=True, autoload_with=engine)
    stations_table = db.Table(
        STATIONS_TABLE_NAME, metadata, autoload=True, autoload_with=engine)

    with engine.begin() as connection:
        
        print('Inserting data...')

        for record in stations_dict:
            stations_data = {
                'id': record['id'],
                'name': record['name'],
                'register': record['cre_id'],
                'longitude': record['longitude'],
                'latitude': record['latitude'],
                'town': record['city'],
                'state': record['state'],
                'is_active': True,
                'status': 'ghost'
            }

            try:
                func_insert_stmt = insert_stmt(stations_table).values()
                func_prices_insert_stmt = insert_stmt(prices_table).values()
                insert_stmt.bind = engine
                result = connection.execute(func_insert_stmt.on_conflict_do_update(constraint=stations_table.primary_key, set_=stations_data), stations_data)
                pk = result.inserted_primary_key[0]
                print(result)

                regular_price_data = create_price_data(record, pk, 'regular')
                diesel_price_data = create_price_data(record, pk, 'diesel')
                premium_price_data = create_price_data(record, pk, 'premium')

                if regular_price_data:
                    connection.execute(func_prices_insert_stmt.on_conflict_do_update(constraint=prices_table.primary_key, set_=regular_price_data), regular_price_data)
                if diesel_price_data:
                    connection.execute(func_prices_insert_stmt.on_conflict_do_update(constraint=prices_table.primary_key, set_=diesel_price_data), diesel_price_data)
                if premium_price_data:
                    connection.execute(func_prices_insert_stmt.on_conflict_do_update(constraint=prices_table.primary_key, set_=premium_price_data), premium_price_data)
            except Exception:
                print('A problem ocurred when inserting records')
                traceback.print_exc()
                sys.exit(1)

        print('Finished inserting records')


def run():
    """
    Entry point for this module
    """
    raw_stations_df, geo_gdf = extract()
    clean_stations_dict = transform(raw_stations_df, geo_gdf)

    start = timer()
    load(clean_stations_dict)
    end = timer()

    print(f'Load process took {timedelta(seconds=end-start)} (HH:MM:SS)')


if __name__ == '__main__':
    run()
