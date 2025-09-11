import requests
import os
import sys
from dotenv import load_dotenv
from soil_property import get_soil_property

load_dotenv()


base_url = os.environ.get('BASE_URL')
if not base_url:
    print('RuntimeError: BASE_URL not set. check the .env file')
    exit(1)

isda_email = os.environ.get('ISDA_EMAIL')
if not isda_email:
    print('RuntimeError: ISDA_EMAIL not set. check the .env file')
    exit(1)

isda_password = os.environ.get('ISDA_PASSWORD')
if not isda_password:
    print('RuntimeError: ISDA_PASSWORD not set. check the .env file')
    exit(1)



lattitude = input('Enter lattitude of the location in Africa:    ').strip()
longitude = input('Enter longitude of the location in Africa:    ').strip()

if not (lattitude or longitude):
    print('\nError: Please enter the lattitude and longitude of the location')
    exit(1)

try:
    lattitude = float(lattitude)
    longitude = float(longitude)
except ValueError:
    print('\nError: Lattitude and Longitude should be decimal values')


url = f'{base_url}/login'
payload = {'username': isda_email, 'password': isda_password}
response = requests.post(url, data=payload, timeout=5)

if response.status_code != 200:
    print('Incorrect username or password, please try again')
else:
    response = response.json()
    access_token = response.get('access_token')
    

soil_property = get_soil_property(lattitude, longitude, access_token)
#print(soil_property)



