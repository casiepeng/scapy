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

