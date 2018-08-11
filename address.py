#!/usr/bin/env python
''' Author       : Huy Nguyen
    Program      : Address Class
    Start        : 07/04/2018
    End          : /2018
    Dependencies : pip(3) install tsp
                   pip install pandas
'''
# packages for location look up
import requests
# packages for tsp


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
        

