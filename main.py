# Wireshark Geolocator
# Simple python program using wireshark's command line interface to intercept users internet protocol addresses and determine their approximate location (IP Address are inherently imprecise). 
# Once the IP Address has been determined via wireshark, this script will use MaxMind's GeoIP2 databases, to find their location information such as their country, state, and city. 
# Once their IP Address and Location has been determined, it will print the result.

from geolite2 import geolite2
import socket, subprocess

# For wireless interface use, uncomment the line below
# cmd = r"C:\Program Files\Wireshark\tshark.exe"

# For wired interface use, comment the line below
cmd = r"C:\Program Files\Wireshark\tshark.exe -i ethernet"

# Start Wireshark Geolocator Script
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
local_ip = socket.gethostbyname(socket.gethostname())
reader = geolite2.reader()

def determine_location(ip_address):
    location = reader.get(ip_address)
    
    try:
      country = location["country"]["names"]["en"]
    except:
      country = "Not found."

    try:
      subdivision = location["subdivisions"][0]["names"]["en"]
    except:
      subdivision = "Not found."    

    try:
      city = location["city"]["names"]["en"]
    except:
      city = "Not found."
    
    return country, subdivision, city


for line in iter(process.stdout.readline, b""):
    columns = str(line).split(" ")

    if "UDP" in columns or "SKYPE" in columns:
        
        if "->" in columns:
            source_ip = columns[columns.index("->") - 1]
        elif "\\xe2\\x86\\x92" in columns:
            source_ip = columns[columns.index("\\xe2\\x86\\x92") - 1]
        else:
            continue
            
        if source_ip == local_ip:
            continue

        try:
            country, subdivision, city = determine_location(source_ip)
            print("Location Information:" + country + " | " + subdivision + " | " + city)
        except:
            try:
                true_ip = socket.gethostbyname(source_ip)
                country, subdivision, city = determine_location(true_ip)
                print("Location Information:" + country + " | " + subdivision + " | " + city)
            except:
                print("Not found.")
                
# End Wireshark Geolocator Script
