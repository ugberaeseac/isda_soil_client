import os
import requests
from dotenv import load_dotenv

load_dotenv()

base_url = os.environ.get('BASE_URL')


def get_soil_property(lattitude, longitude, access_token):
    lattitude = lattitude
    longitude = longitude

    url = f'{base_url}/isdasoil/v2/layers'
    headers = {
        'Authorization': f'Bearer {access_token}'
        }
    
    response = requests.get(url, headers=headers)
    soil_property_data = response.json()
    return soil_property_data