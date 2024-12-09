"""
@date: 12/9/24
@author: Madison Davidson, Casie Peng
@PID: mzddie, casiepeng
@assignment: Class Project
"""
# this will allow this program to interpret JSON object. See example JSON:http://dazzlepod.com/ip/128.173.239.242.json
import json

# the tools needed to access a URL and get data.
import requests

# allows operations such opening a default browser at a given URL
import webbrowser, os

# for pausing our requests to a web service that takes IP and returns latitude,longitude
import time

# scapy is an extensive networking library for python. We are going to be using its 'traceroute()'
from scapy.layers.inet import socket
from scapy.layers.inet import traceroute

# this is to plot our lat/long data onto Google Maps  https://pypi.org/project/gmplot/
from gmplot import gmplot   

# adding for arguments
import sys 


if (len(sys.argv) != 2):
    hostname = "mn.gov"
else:
    hostname = sys.argv[1]

ip = socket.gethostbyname(hostname)
ip = requests.get('https://api.ipify.org').text # USE THIS FOR INITIAL

def find_and_plot_coordinates(ip):
    
    # tool for finding latitutde and longitude of ip address
    url = f"http://dazzlepod.com/ip/{ip}.json"
    
    # debugging the URLs
    print(url)
    response = requests.get(url)
    data = response.json()
    unique_coords = set() # stores unique lat long pairs
    lat = []
    long = []
    # making sure the wesbsite gave us lat and long
    if 'latitude' in data and 'longitude' in data:
        coords = (data['latitude'], data['longitude']) # makes a set coordinate pair

        if coords not in unique_coords:
            unique_coords.add(coords)
            lat.append(data['latitude'])
            long.append(data['longitude'])
                         
    # pausing for 2 seconds to make sure we don't get banned by 'dazzlepod.com'
    time.sleep(SLEEP_SECONDS)
            
    #calls function to plot the lats and longs
    plot_initial()
    plot_lat_long(lat, long)

def plot_initial():
    url = f"http://dazzlepod.com/ip/me.json"
    response = requests.get(url)
    data = response.json()
    lat = data['latitude']
    long = data['longitutde']
    gmplot.GoogleMapPlotter(lat, long, 3)



# plots 3 coordinates onto Google Maps - hardcoded for in-class example
def plot_lat_long(lats, longs):
   
    # the initial lat long and the zoom levels for the map (3 is zoomed out)
    gmap = gmplot.GoogleMapPlotter(42.0167, 23.1000, 3)
    
    #Handle path issue for windows, so that marker images can optionally be found using gmplot
    if ":\\" in gmap.coloricon:
        gmap.coloricon = gmap.coloricon.replace('/', '\\')
        gmap.coloricon = gmap.coloricon.replace('\\', '\\\\')
        
    
    # placing large dots on the lat longs
    # for your homework you will pass in coordinates retrieved from dazzlepod. 
    # for this in-class example, we will plot a hard-coded list of coordinates
    
    gmap.scatter( lats, longs, '#FF00FF', 
                              size = 40000, marker = False) 

        

    # get the currentdirectory
    cwd = os.getcwd()
    
    # saving the map as an HTML into the project directory
    gmap.draw("traceroute.html")
    
    # opening the HTML via default browser
    webbrowser.open("file:///" + cwd +"/traceroute.html")
