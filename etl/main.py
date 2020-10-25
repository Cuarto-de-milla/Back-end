"""
This module comprises the ETL system for the "Cuarto de Milla" project, and is
in charge of processing Gas Station datasets into a clean structure and then
insert records into a database
"""

import os
import sys
import random
import requests
import traceback
import numpy as np
import pandas as pd
import sqlalchemy as db
import xmltodict as x2d
from datetime import timedelta, datetime
from timeit import default_timer as timer
from dummy import get_city_and_state_for_location


URL_SOURCES = [
    'https://publicacionexterna.azurewebsites.net/publicaciones/places',
    'https://publicacionexterna.azurewebsites.net/publicaciones/prices'
]
DB_STRING = os.environ['DATABASE_URL']
DATA_FOLDER = 'data/'
DATASET_FILES = [DATA_FOLDER + 'places.xml', DATA_FOLDER + 'prices.xml']
DF_COLS = ['place_id', 'name', 'cre_id', 'longitude', 'latitude', 'regular_price',
           'diesel_price', 'premium_price']


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


def create_price_data(record, price_type):
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
            'station_id': record['id']
        }
    else:
        return None


def extract():
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


def transform(stations_df):
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

    stations_complete_data_df[['city','state']] = stations_complete_data_df.apply(
        lambda x_df: get_city_and_state_for_location(x_df['longitude'], x_df['latitude']), axis=1, result_type = 'expand'
    )

    return stations_complete_data_df.reset_index(0).to_dict('records')


def load(stations_dict):
    """
    Loads the information in the data structure stations_dict to the database
    """
    print(f'Connecting to the database...')

    engine = db.create_engine(DB_STRING)
    metadata = db.MetaData()
    prices_table = db.Table(
        'gasoline_price', metadata, autoload=True, autoload_with=engine)
    stations_table = db.Table(
        'gasoline_station', metadata, autoload=True, autoload_with=engine)

    with engine.connect() as connection:
        print('Inserting data...')

        for record in stations_dict:
            stations_data = {
                'id': record['id'],
                'name': record['name'],
                'longitude': record['longitude'],
                'latitude': record['latitude'],
                'town': record['city'],
                'state': record['state'],
                'is_active': True,
                'status': 'ghost'
            }

            regular_price_data = create_price_data(record, 'regular')
            diesel_price_data = create_price_data(record, 'diesel')
            premium_price_data = create_price_data(record, 'premium')

            try:
                connection.execute(db.insert(stations_table), stations_data)

                if regular_price_data:
                    connection.execute(db.insert(prices_table), regular_price_data)
                if diesel_price_data:
                    connection.execute(db.insert(prices_table), diesel_price_data)
                if premium_price_data:
                    connection.execute(db.insert(prices_table), premium_price_data)
            except Exception:
                print('A problem ocurred when inserting records')
                traceback.print_exc()
                sys.exit(1)

        print('Finished inserting records')


def run():
    """
    Entry point for this module
    """
    raw_stations_df = extract()
    clean_stations_dict = transform(raw_stations_df)

    start = timer()
    load(clean_stations_dict)
    end = timer()

    print(f'Load process took {timedelta(seconds=end-start)} (HH:MM:SS)')


if __name__ == '__main__':
    run()
