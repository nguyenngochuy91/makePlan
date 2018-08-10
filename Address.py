#!/usr/bin/env python
''' Author       : Huy Nguyen
    Program      : Address Class
    Start        : 07/04/2018
    End          : /2018
    Dependencies : pip install geopy
                   pip install tsp
                   pip install pandas
'''
# packages for location look up
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
# packages for tsp
import tsp 

geolocator = Nominatim(user_agent="makePlan")

class Address(object):
    def __init__(self,address):
        self.location   = geolocator.geocode(address)
        if self.location:
            self.latitude   = self.location.latitude
            self.longtitude = self.location.longitude
            self.address    = self.location.address
        else:
            print ("Address not found")
        
"""
functions : Given a list of addresses, get all the distances between them, stores in a dictionary
input     : List of addresses
output    : dictionary, (key: a number, value: address), a distance matrix
"""
def getDistance(addresses):
    distance_matrix = {}
    address_name    =  {}
    for i in range(len(addresses)-1):
        address_i  = addresses[i].address
        location_i = (addresses[i].latitude,addresses[i].longtitude)
        address_name[i] = address_i
        distance_matrix[(i,i)] = 0
        for j in range(i+1,len(addresses)):
            location_j = (addresses[j].latitude,addresses[j].longtitude)
            distance_matrix[(i,j)]=(geodesic(location_i,location_j).miles)
            distance_matrix[(j,i)]=(geodesic(location_i,location_j).miles)
    return address_name,distance_matrix

"""
functions : Given a dictionary of distance, find a the shorstest circle that goes through each of the 
            addresses (basically TSP problem). This will provide optimal solution for up to 23 nodes
input     : address_name,distance_matrix
output    : route , cost
"""
def TSPOpt(address_name,distance_matrix):
    cost,route = tsp.tsp(range(len(address_name)),distance_matrix)
    return (cost,[address_name[r] for r in route])
    
"""
functions : Given a dictionary of distance, find a the shorstest circle that goes through each of the 
            addresses (basically TSP problem). This will provide approx solution
input     : address_name,distance_matrix
output    : route, cost
"""
def TSPApprox(address_name,distance_matrix):
    route = []
    distance = 0