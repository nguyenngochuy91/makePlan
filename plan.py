#!/usr/bin/env python
''' Author       : Huy Nguyen
    Program      : Make Plan program
    Start        : 07/04/2018
    End          : /2018
    Dependencies : pip(3) install tsp
                   pip install pandas
'''
# packages for tsp
import tsp 
from address import Address
from math import cos, asin, sqrt


"""
functions : take in input of addresses and parse in as Address type
input     : N/A
output    : list of Address
"""
def parseInput(address_type):
    addresses= []
    while True:
        # get in the address name
        try:
            address_name = input("Please input name of the attractions of interest or type N/n for stop:\n")
        except:
            address_name = raw_input("Please input name of the attractions of interest or type N/n for stop:\n")  
        # stop if user is done
        if address_name in "Nn":
            break
        else:
            try:
                address = input("Please input our address of interest: \n")
            except:
                address = raw_input("Please input our address of interest: \n")
            address = Address(address,address_name,address_type)
            while address.error:
                try:
                    print (address.error)
                    address = input("Please input a correct address of {} ^^:\n".format(address_name))
                except:
                    address = raw_input("Please input a correct address of {} ^^:\n".format(address_name))
                address = Address(address,address_name,address_type)
            addresses.append(address)
    return addresses
"""
functions : given long,lat of 2 points, find the distance in miles
input     : coordinates
output    : distance
"""
def distance(location_i,location_j):
    lat1 = location_i[0]
    lon1 = location_i[1]
    lat2 = location_j[0]
    lon2 = location_j[1]    
    p = 0.017453292519943295     #Pi/180
    a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 3,959 *2 * asin(sqrt(a))
"""
functions : Given a list of addresses, get all the distances between them, stores in a dictionary
input     : list of Address type
output    : dictionary for name, (key: a number, value: Address), a distance matrix
"""
def getDistance(addresses):
    distance_matrix = {}
    address_name    =  {}
    for i in range(len(addresses)):
        address_i  = addresses[i]
        location_i = (address_i.latitude,address_i.longtitude)
        address_name[i] = address_i
        distance_matrix[(i,i)] = 0
        for j in range(len(addresses)):
            if i ==j:
                continue
            location_j = (addresses[j].latitude,addresses[j].longtitude)
            distance_matrix[(i,j)]=distance(location_i,location_j)
            distance_matrix[(j,i)]=distance(location_i,location_j)
    return address_name,distance_matrix

"""
functions : Given a dictionary of distance, find a the shorstest circle that goes through each of the 
            addresses (basically TSP problem). This will provide optimal solution for up to 23 nodes
input     : address_name,distance_matrix
output    : route , cost
"""
def TSPOpt(address_name,distance_matrix):
    cost,route = tsp.tsp(range(len(address_name)),distance_matrix)
    path       = [address_name[r].name for r in route]
    path.append(address_name[route[0]].name)
    return (cost,path)
    

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
    return " --> ".join(route)

if __name__ == '__main__':
    print ("{}\n".format("*"*180))
    print ("Welcome to makePlan app!!!!!! \n")
    # input list of attractions
    print ("Please input the addresses of actractions (name of the place, followed by address)")
    attractions = parseInput("attraction")
    # input list of restaurants
#    print ("Please input the addresses of restaurants (name of the place, followed by address)")
#    restaurants = parseInput("restaurant")
    # getting the distance and name
    # print ([item.address for item in addresses])
    address_name,distance_matrix = getDistance(attractions)
#    print ("distance_matrix",distance_matrix)
#    print ("address_name",address_name)
    # get the route and total distance
    cost, route                  = TSPOpt(address_name,distance_matrix)
    print ("How many addresses:",len(route))
    print ("The route is {}\n".format(beautify(route)))
    print ("The total distance: {}\n".format(cost))
    