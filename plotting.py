"""
@date: 12/9/24
@author: Madison Davidson, Casie Peng
@PID: mzddie, casiepeng
@assignment: Class Project
"""

import requests, time, json, os
import webbrowser, sys

# scapy is an extensive networking library for python. We are going to be using its 'traceroute()'
from scapy.layers.inet import socket
from scapy.layers.inet import traceroute
# this is to plot our lat/long data onto Google Maps  https://pypi.org/project/gmplot/
from gmplot import gmplot   

# Hostname input stuff
if (len(sys.argv) != 2):
    hostname = "mn.gov"
else:
    hostname = sys.argv[1]

# converts host to ip
ip = socket.gethostbyname(hostname)

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
    gmap = gmplot.GoogleMapPlotter(lat, long, 3)
    gmap.marker(lat, long, color='red', label='1')



# plots 3 coordinates onto Google Maps - hardcoded for in-class example
def plot_lat_long(lats, longs):
   
    # the initial lat long and the zoom levels for the map (3 is zoomed out)


    #colors: red, orange, yellow, green, blue
    for i in range(len(lats)):

        the_color = 'red'

        if i % 5 == 0:
            the_color = 'red'
        elif i % 5 == 1:
            the_color = 'orange'
        elif i % 5 == 2:
            the_color = 'yellow'
        elif i % 5 == 3:
            the_color = 'green'
        else:
            the_color = 'blue'

        gmap = gmplot.GoogleMapPlotter(lats[i], longs[i], 3)
        gmap.marker(lats[i], longs[i], color=the_color, label=str(i))

    
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

#will need to slow down the request frequency from 'dazzlepod.com' to find latitude and longitude
SLEEP_SECONDS = 2;

# a good explanation of how traceroute works: https://www.youtube.com/watch?v=G05y9UKT69s
# add maxttl=100 or more if you want to traceroute even deeper.
#'res' -- results from traceroute 
res, _ = traceroute(ip,maxttl=64,verbose = 0)
# will store retrieved IPs here.
ips = []

# going through the traceroute results and extracting IP addresses into the array
for item in res.get_trace()[ip]:
    try:
        hopping_ip = res.get_trace()[ip][item][0]
        if hopping_ip not in ips:
            ips.append(hopping_ip)
    except IndexError:
        pass
    
#find coordinates and plot them   
find_and_plot_coordinates(ips)