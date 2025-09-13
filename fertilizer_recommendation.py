"""
Helper function that builds a soil classification prompt
and call GroqCloud's LLM endpoint to get a basic fertilizer
recommendation for farmers in Africa.
"""

import requests


# prompt template for 'system' role
prompt_system= """
You are an agronomist specialist and assistant. Use ONLY these fertilizer options and their nutrient coverage:
- Urea (46-0-0) -> supplies N (high)
- Ammonium Sulfate (21-0-0) -> supplies N (high)
- Single Super Phosphate -> supplies P (moderate)
- Triple Super Phosphate -> supplies P (high)
- Muriate of Potash -> supplies K (high)
- Sulphate of Potash -> supplies K (high)
- Lime -> adjusts pH (raises)

Give clear and simple recommendations for farmers in Africa.
"""

# prompt template for 'user' role
prompt = """
The soil classification results are:
- Nitrogen: {}
- Phosphorus: {}
- Potassium: {}
- pH: {}

Provide a basic fertilizer recommendation for this soil, based only on the allowed fertilizers.
"""


def get_fertilizer_recommendation(groq_api_url, groq_api_key, soil_classification):
    """
    Build and send request to GroqCloud LLM based on the
    provided soil classifications to get fertilizer recommendation
    """

    # extract the soil properties and parse it with prompt to LLM
    nitrogen = soil_classification.get('nitrogen')
    phosphorous = soil_classification.get('phosphorous')
    potassium = soil_classification.get('potassium')
    ph = soil_classification.get('pH')
    prompt_user = prompt.format(nitrogen, phosphorous, potassium, ph)

    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {groq_api_key}'
    }

    payload = {
        'model': 'llama-3.3-70b-versatile',
        'messages': [
            {
                'role': 'system',
                'content': prompt_system 
            },
            {
                'role': 'user',
                'content': prompt_user
            }
        ],
    }


    # catch ReadTimeout or generic request errors to avoid crashes
    try:
        response = requests.post(groq_api_url, headers=headers, json=payload, timeout=5)
    except requests.exceptions.ReadTimeout:
        print('\nRequest Timeout, Please try again')
        exit(1)
    except requests.exceptions.RequestException:
        print('\nRequest Failed. Please try again')
        exit(1)


    # check status code for invalid credentials
    # on success, return JSON response
    if response.status_code == 200:
        return response.json()
    else:
        print('\nUnknown LLM request URL: Please check the URL for typos')
        exit(1)
