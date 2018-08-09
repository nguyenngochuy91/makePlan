#!/usr/bin/env python
''' Author       : Huy Nguyen
    Program      : Address Class
    Start        : 07/04/2018
    End          : /2018
    Dependencies : pip install geopy
                   pip install cluster
'''
# packages for location look up
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
# packages for clustering 
geolocator = Nominatim(user_agent="makePlan")

class Address(object):
    def __init__(self,address):
        self.location   = geolocator.geocode(address)
        self.latitude   = self.location.latitude
        self.longtitude = self.location.longitude
        self.address    = self.location.address
        
"""
functions : Given a list of addresses, get all the distances between them, stores in a dictionary
input     : List of addresses
output    : dictionary, key is tuple of 2 locations, value is the distance
"""
def getDistance(addresses):
    distance_map = {}
    for i in range(len(addresses)-1):
        address_i  = addresses[i].address
        location_i = (addresses[i].latitude,addresses[i].longtitude)
        for j in range(i+1,len(addresses)):
            address_j = addresses[j].address
            location_j = (addresses[j].latitude,addresses[j].longtitude)
            distance_map[(address_i,address_j)] = geodesic(location_i,location_j).miles
    return distance_map

"""
functions : Given a dictionary of distance, find a the shorstest circle that goes through each of the 
            addresses (basically TSP problem)
input     : dictionary of map
output    : route 
"""
def getRoute(distance_map):
    route = []
    distance = 0
    
