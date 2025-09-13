"""
Helper function to get soil the property
of a given location and depth
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()


base_url = os.environ.get('BASE_URL')


def get_soil_property(lattitude, longitude, depth, access_token):
    """
    Fetch the soil properties (N, P, K and pH)
    for a given location and depth
    """

    url = f'{base_url}/isdasoil/v2/soilproperty'
    params = {
        'lat': lattitude,
        'lon': longitude,
        'depth': depth,
        'property': None
    }
    
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)
    except requests.exceptions.ReadTimeout:
        print('\nRequest Timeout, Please try again')
        exit(1)
    except requests.exceptions.RequestException:
        print('\nRequest Failed. Please try again')
        exit(1)


    if response.status_code != 200:
        print('\nPlease choose another location. No soil data for deserts and waterbodies')
        exit(1)
    soil_property_data = response.json()
    return soil_property_data