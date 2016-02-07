#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# (c) 2016 Critizr

import requests
from requests.auth import HTTPBasicAuth
#import logging; log = logging.getLogger(__name__)

API_ENDPOINT = "https://api.sncf.com/v1/"

__author__ = u'Critizr'
"""
Coverage :
GET /coverage	List of the areas covered by SNCF API
GET /coverage/region_id	Information about a specific region

Public transportation objects : List of the public transport objects of a region
GET /coverage/region_id/collection_name	Collection of objects of a region
GET /coverage/region_id/collection_name/object_id	Information about a specific region

Journeys : Compute journeys
GET /coverage/resource_path/journeys	List of journeys
GET /journeys	List of journeys

Route Schedules : Compute route schedules for a given resource
GET /coverage/resource_path/route_schedules	List of the route schedules
Stop Schedules : Compute stop schedules for a given resource
GET /coverage/resource_path/stop_schedules	List of the stop schedules
Departures : List of the next departures for a given resource
GET /coverage/resource_path/departures	List of the departures
Arrivals : List of the next departures for a given resource
GET /coverage/resource_path/arrivals	List of the arrivals
Places/Autocomplete : Search in the datas
GET /coverage/places	List of objects
Places nearby : List of objects near an object or a coord
GET /coverage/resource_path/places_nearby	List of objects near the resource
GET /coverage/lon;lat/places_nearby	List of objects near the resource
"""


class SNCF(object):
    """SNCF V1 API wrapper"""

    def __init__(self, api_key=None, default_max_count=50):
        """Sets up the api object"""
        self.api_key = api_key

        self.default_max_count = default_max_count
        # Set up endpoints
        self.base_requester = self.Requester(api_key,default_max_count)
    
    class Requester(object):
        """Api requesting object"""
        def __init__(self, api_key=None,default_max_count=50):
            """Sets up the api object"""
            self.api_key = api_key
            self.default_max_count = default_max_count
            self.multi_requests = list()

        def GET(self, path, params={}, **kwargs):
            """GET request that returns processed data"""
            params = params.copy()
            params['count']=self.default_max_count
            # Continue processing normal requests
            headers = self._create_headers()
            url = '{API_ENDPOINT}{path}'.format(
                API_ENDPOINT=API_ENDPOINT,
                path=path
            )

            _log(url)
            result = _get(url,self.api_key, headers=headers, params=params)
            return result

        def _create_headers(self):
            """Get the headers we need"""
            headers = {}
            return headers

    def coverage(self,region_id=""):
    	return self.base_requester.GET('coverage/sncf/{region_id}'.format(region_id=region_id))
    	
    def public_transportation_objects(self,collection_name,region_id=None,object_id=""):
    	if region_id:
    		return self.base_requester.GET('coverage/sncf/{region_id}/{collection_name}/{object_id}'.format(region_id=region_id,collection_name=collection_name,object_id=object_id))
    	return self.base_requester.GET('coverage/sncf/{collection_name}/{object_id}'.format(region_id=region_id,collection_name=collection_name,object_id=object_id))

    def journeys(self,datetime, params={}):
    	params['datetime'] = datetime.strftime('%Y%m%dT%H%M%S')
    	return self.base_requester.GET('journeys/',params)

    def route_schedules(self,resource_path,from_datetime,params={}):
    	params['from_datetime'] = from_datetime.strftime('%Y%m%dT%H%M%S')
    	return self.base_requester.GET('coverage/sncf/{resource_path}/route_schedules'.format(resource_path=resource_path),params)

    def stop_schedules(self,resource_path,from_datetime,params={}):
    	params['from_datetime'] = from_datetime.strftime('%Y%m%dT%H%M%S')
    	return self.base_requester.GET('coverage/sncf/{resource_path}/stop_schedules'.format(resource_path=resource_path),params)

    def departures(self,resource_path,from_datetime,params={}):
    	params['from_datetime'] = from_datetime.strftime('%Y%m%dT%H%M%S')
    	return self.base_requester.GET('coverage/sncf/stop_areas/{resource_path}/departures'.format(resource_path=resource_path),params)

    def arrivals(self,resource_path,from_datetime,params={}):
    	params['from_datetime'] = from_datetime.strftime('%Y%m%dT%H%M%S')
    	return self.base_requester.GET('coverage/sncf/stop_areas/{resource_path}/arrivals'.format(resource_path=resource_path),params)

    def places_autocomplete(self,query,params={}):
    	params['q']=query
    	return self.base_requester.GET('coverage/sncf/places',params)

    def places_nearby(self,resource_path=None,position = None,params={}):
    	if resource_path:
    		return self.base_requester.GET('coverage/sncf/{resource_path}/places_nearby'.format(resource_path=resource_path),params)
    	return self.base_requester.GET('coverage/sncf/{lat};{lon}/places_nearby'.format(lat=position[0],lon=position[1]),params)


"""
Network helper functions
"""

def _log(msg):
	#log('SNCF API CLIENT : {message}'.format(message=msg))
    print 'SNCF API CLIENT : {message}'.format(message=msg)

def _get(url, api_key, headers={}, params=None):
    """GET data from an endpoint"""
    try:
        response = requests.get(url, headers=headers, params=params, auth=HTTPBasicAuth(api_key, ''))
        return _process_response(response)
    except requests.exceptions.RequestException as e:
        _log('Network exception')

def _process_response(response):
    """Make the request and handle exception processing"""
    # Read the response as JSON
    try:
        data = response.json()
    except ValueError:
        _log('Invalid Response')

    # Default case, Got proper response
    if response.status_code == 200:
        return data
    _log('Response Status KO, '+str(response.status_code))
    return None
        

