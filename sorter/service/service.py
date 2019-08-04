import requests
import time
import json
from sorter.service.param_exception import ParamNotFound
from sorter.service.request_exception import RequestError


class ServiceAPI:
    URL = 'https://api.opencagedata.com/geocode/v1/json'
    
    def __init__(self):
        self.__api_key = None
        self.current_request_data = None
    
    def get_request(self, params):
        request = requests.get(url=URL, params=params)
        status = request.json()['status']
        if status['code'] != 200:
            raise RequestError("ERROR:" + status['message'])
        # Condition of the free trial of the service: I can use API one time per second
        time.sleep(1.1)
        return request
    
    def set_api_key(self, key):
        self.__api_key = key
        
    def check_api_key(self):
        params = {
            "key": self.__api_key
        }        
        try:
            self.get_request(params)
        except RequestError as error:
            raise error
        
        
    def update_data(self, lat, lon):
        if not lat or not lon:
            raise ParamNotFound("ERROR: Parametrs: lat and/or lon not found.")
        try:
            self.current_request_data = get_request(
                {
                    "q": str(lat) + ' ' + str(lon),
                    "key": self.__api_key
                }
            )
        except RequestError as e:
            raise e
        
    def get_country(self):
        try:
            country = self.current_request_data.json()['results'][0]['components']['country']
        except KeyError:
            country = None
            
        return country
    
    def get_city(self):
        try:
            city = self.current_request_data.json()['results'][0]['components']['city']
        except KeyError:
            city = None
            
        return city
    
    
    