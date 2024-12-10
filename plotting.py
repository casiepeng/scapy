"""
@date: 12/9/24
@author: Madison Davidson, Casie Peng
@PID: mzddie, casiepeng
@assignment: Class Project
@hostname: bundesregierung.de
"""
# Importing important stuff.... we stole from Round1, 2, and 3!
import requests, time, json, os
import webbrowser, sys
from scapy.layers.inet import socket
from scapy.layers.inet import traceroute
from gmplot import gmplot   

# Hostname input stuff, basically use default host if commandline is not input
if (len(sys.argv) != 2):
    hostname = "aubg.bg"
else:
    hostname = sys.argv[1]

# Converts host into its corresponding IP address
ip = socket.gethostbyname(hostname)
# Uses scapy traceroute function to map out the network hops
res, _ = traceroute(ip, maxttl=64, verbose=0)
# Empty list of IP addresses
ips = []

# Extracts the IP adresses from traceroute results, avoids duplicates, and adds the hop's IP to the list- and then ignores cases where no IP is recorded.
for item in res.get_trace()[ip]:
    try:
        hopping_ip = res.get_trace()[ip][item][0]
        if hopping_ip not in ips:
            ips.append(hopping_ip)
    except IndexError:
        pass

# Function to plot coordinates using Google Maps
def plot_lat_long(lats, longs):
    url = f"http://dazzlepod.com/ip/me.json" # Gets user's current ip to use for initial
    response = requests.get(url) # uses a get request for the ip lookup
    data = response.json() # parses the json response
    ilat = data.get('latitude', None) # extracts lat and long data from the json
    ilong = data.get('longitude', None)

    # Adds users initial location as the starting point for the maps markers
    lats.insert(0, ilat)
    longs.insert(0,ilong)

    # Initializes the map with starting location
    gmap = gmplot.GoogleMapPlotter(lats[0], longs[0], 3)
    gmap.marker(lats[0], longs[0], color='red', label='1') # Marks starting point

    # Loops through list of coords and adds markers for each destination
    for i in range(len(lats)):
        the_color = 'red'
        # Cycling colors for unique markers
        if i % 5 == 0:
            the_color = 'm'
        elif i % 5 == 1:
            the_color = 'c'
        elif i % 5 == 2:
            the_color = 'r'
        elif i % 5 == 3:
            the_color = 'g'
        else:
            the_color = 'b'
        
        gmap.marker(lats[i], longs[i], color=the_color, label=str(i + 1))

    if ":\\" in gmap.coloricon:
        gmap.coloricon = gmap.coloricon.replace('/', '\\')
        gmap.coloricon = gmap.coloricon.replace('\\', '\\\\')
    # Connects all markers with a line/trail
    gmap.plot(lats, longs, color='b', edge_width=2.5)

    # Saves the map created as an HTML file which is then opened in the user's default browser
    cwd = os.getcwd()
    gmap.draw("traceroute.html")
    webbrowser.open("file:///" + cwd + "/traceroute.html")

# Function to find lat and long of IP addresses and plots them
def find_and_plot_coordinates(ips):
    # Initializing empty set and arrays
    unique_coords = set() 
    lat = [] 
    long = []  

    # Loops through each collected IP address
    for ip in ips:
        # API usage for each IP
        url = f"http://dazzlepod.com/ip/{ip}.json"
        print(f"Retrieving data for IP: {ip}") # Confirmation on which IP is being used
        response = requests.get(url) #

        # If request is successful, parse and collect the json data
        if response.status_code == 200:
            data = response.json()
            # Check if latitude and longtitute exist in the given json data
            if 'latitude' in data and 'longitude' in data:
                latitude = data['latitude']
                longitude = data['longitude']

                # Checks to make sure lat and long are real values to avoid NoneType errors
                if isinstance(latitude, (float, int)) and isinstance(longitude, (float, int)):
                    coords = (latitude, longitude)

                    # Adds the coords to the list if they are not duplicates
                    if coords not in unique_coords:
                        unique_coords.add(coords)
                        lat.append(latitude)
                        long.append(longitude)
        # Pauses to prevent API rate-limits
        time.sleep(SLEEP_SECONDS)
    # Plots the coords
    plot_lat_long(lat, long)
# Defines sleeper seconds
SLEEP_SECONDS = 2

# Finally calls the function to plot all traceroute hops and create and open a map
find_and_plot_coordinates(ips)
