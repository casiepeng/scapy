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
    # making sure the wesbsite gave us lat and long
    if 'latitude' in data and 'longitude' in data:
        print(data['latitude'],data['longitude'])
                         
    # pausing for 2 seconds to make sure we don't get banned by 'dazzlepod.com'
    time.sleep(SLEEP_SECONDS)
            
    #calls function to plot the lats and longs
    plot_lat_long()
