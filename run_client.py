import requests
import os
from dotenv import load_dotenv
from soil_property import get_soil_property
from soil_property_classification import (
    get_nitrogen_classification,
    get_phosphorous_classification,
    get_potassium_classification,
    get_ph_classification
)
from fertilizer_recommendation import get_fertilizer_recommendation

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

groq_api_key = os.environ.get('GROQ_API_KEY')
if not groq_api_key:
    print('RuntimeError: GROQ_API_KEY not set. check the .env file')
    exit(1)

groq_api_url = os.environ.get('GROQ_API_URL')
if not groq_api_url:
    print('RuntimeError: GROQ_API_URL not set. check the .env file')
    exit(1)



def check_coordinates(lattitude, longitude):
    """
    check if the coordinates entered are within Africa
    return True if in Africa else False
    """
    if lattitude >= -35.0 and lattitude <= 37.0:
        if longitude >= -18.0 and longitude <= 52:
            return True
    return False


def run_client():
    """

    """
    lattitude = input('Enter lattitude of the location in Africa:    ').strip()
    longitude = input('Enter longitude of the location in Africa:    ').strip()
    depth = input('Enter the depth:    ').strip()


    if not (lattitude or longitude):
        print('\nError: Please enter the lattitude and longitude of the location')
        exit(1)

    try:
        lattitude = float(lattitude)
        longitude = float(longitude)
    except ValueError:
        print('\nError: Lattitude and Longitude should be decimal values')
        exit(1)

    
    is_within_africa = check_coordinates(lattitude, longitude)
    if not is_within_africa:
        print('\nError: Co-ordinates are outside Africa. Please provide a location in Africa')
        exit(1)


    depth_values = ['0-20']
    if depth not in depth_values:
        print('Error: Depth must be topsoil value (0-20cm)')
        exit(1)


    url = f'{base_url}/login'
    payload = {'username': isda_email, 'password': isda_password}
    
    try:
        response = requests.post(url, data=payload, timeout=5)
    except requests.exceptions.ReadTimeout:
        print('\nRequest Timeout, Please try again')
        exit(1)
    except requests.exceptions.RequestException:
        print('\nRequest Failed. Please try again')
        exit(1)

    if response.status_code != 200:
        print('Incorrect username or password, please try again')
    else:
        response_data = response.json()
        access_token = response_data.get('access_token')
        

    soil_property = get_soil_property(lattitude, longitude, depth, access_token)
    nitrogen_value = soil_property['property']['nitrogen_total'][0]['value']['value']
    phosphorous_value = soil_property['property']['phosphorous_extractable'][0]['value']['value']
    potassium_value = soil_property['property']['potassium_extractable'][0]['value']['value']
    pH_value = soil_property['property']['ph'][0]['value']['value']


    nitrogen_classification = get_nitrogen_classification(nitrogen_value)
    phosphorous_classification = get_phosphorous_classification(phosphorous_value)
    potassium_classification = get_potassium_classification(potassium_value)
    pH_classification = get_ph_classification(pH_value)

    results = f"""
    \nThe soil classification results are:
    - Nitrogen: {nitrogen_classification}
    - Phosphorus: {phosphorous_classification}
    - Potassium: {potassium_classification}
    - pH: {pH_classification}\n
    """
    print(results)

    soil_classification = dict()
    soil_classification['nitrogen'] = nitrogen_classification
    soil_classification['phosphorous'] = phosphorous_classification
    soil_classification['potassium'] = potassium_classification
    soil_classification['pH'] = pH_classification

   
    recommendation = get_fertilizer_recommendation(groq_api_url, groq_api_key, soil_classification)
    print(recommendation['choices'][0]['message']['content'])
    


if __name__ == '__main__':
    run_client()