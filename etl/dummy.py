"""
This module creates mock data
"""

import random


def get_city_and_state_for_location(longitude, latitude):
    """
    Returns mock information to the city and state fields of a pair of coordinates
    in form of a tuple:  (city, state)
    """
    city_vs_state = {
        'Ecatepec': 'México',
        'Guadalajara': 'Jalisco',
        'Juárez': 'Chihuahua',
        'Zapopan': 'Jalisco',
        'Nezahualcóyotl': 'México',
        'Chihuahua': 'Chihuahua',
        'Mérida': 'Yucatán',
        'Tlalnepantla': 'México',
        'Delicias': 'Chihuahua'
    }

    return random.choice(list(city_vs_state.items()))