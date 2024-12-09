"""
@date: 12/9/24
@author: Madison Davidson, Casie Peng
@PID: mzddie, casiepeng
@assignment: Class Project
"""
import sys, requests
from scapy.all import traceroute
from gmplot import gmplot
from scapy.layers.inet import socket

if (len(sys.argv) != 2):
    hostname = "mn.gov"
else:
    hostname = sys.argv[1]

ip = socket.gethostbyname(hostname)

def find_and_plot_coordinates(ip):
    
    # tool for finding latitutde and longitude of ip address
    url = f"http://dazzlepod.com/ip/{ip}.json"
    
    # debugging the URLs
    print(url)
    response = requests.get(url)
    data = response.json()
    lat = []
    long = []
    # making sure the wesbsite gave us lat and long
    if 'latitude' in data and 'longitude' in data:
        print(data['latitude'],data['longitude'])
        lat.append(data['latitude'])
        long.append(data['longitude'])
        
        
                         
    # pausing for 2 seconds to make sure we don't get banned by 'dazzlepod.com'
    time.sleep(SLEEP_SECONDS)
            
    #calls function to plot the lats and longs
    plot_lat_long(lat, long)

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
