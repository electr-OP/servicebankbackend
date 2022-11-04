import requests
from urllib.parse import urlencode

def get_geometry(input):
    base_endpoint_places = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    params = {
    "key": '',
    "input": input,
    "locationbias":"point:9.0820,8.6753",
    "inputtype": "textquery",
    "fields": "place_id,formatted_address,name,geometry"
    }
    params_encoded = urlencode(params)
    places_endpoint = f"{base_endpoint_places}?{params_encoded}"
    # print(places_endpoint)
    r = requests.get(places_endpoint)
    if r.status_code in range(200, 299): 
        return r.json()
