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
import requests
from geopy.distance import geodesic
# packages for tsp
import tsp 


class Address(object):
    def __init__(self,address):
        self.address  = address
        self.response = self.getResponse()
        self.status   = self.response["status"]
        if self.status =="OK":
            self.error      = None
            self.results    = self.response["results"]
            self.location   = self.results[0]["geometry"]["location"]
            self.latitude   = self.location["lat"]
            self.longtitude = self.location["lng"]
        else:
            self.error      = self.status
    def getResponse(self):
        address = "+".join(self.address.split())
        return requests.get("https://maps.googleapis.com/maps/api/geocode/json?address={}".format(address)).json()
        
"""
functions : Given a list of addresses, get all the distances between them, stores in a dictionary
input     : List of addresses
output    : dictionary for name, (key: a number, value: address), a distance matrix
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
"""
functions : Giving the route, output it nicely as a map
input     : route, cost
output    : map (string)
"""
def beautify(route):
    route = [str(r) for r in route]
    return "-->".join(route)

if __name__ == '__main__':
    addresses= []
    print ("welcome to makePlan app!!!!!! \n")
    while True:
        try:
            address = input("Please input our address of interest or type N/n for stop:\n")
        except:
            address = raw_input("Please input our address of interest or type N/n for stop:\n")
        if address in "Nn":
            break
        else:
            address = Address(address)
            while address.error:
                try:
                    address = input("Please input a correct address of interest ^^:\n")
                except:
                    address = raw_input("Please input a correct address of interest ^^:\n")
            addresses.append(address)
    # getting the distance and name
    address_name,distance_matrix = getDistance(addresses)
    # get the route and total distance
    cost, route                  = TSPOpt(address_name,distance_matrix)
    print ("The route is {}, and the total distance is {}".format(beautify(route),cost))
