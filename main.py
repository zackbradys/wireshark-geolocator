# Wireshark Geolocator (Python)
# Simple Python program using Wireshark and MaxMind's GeoLite2 to locate users via their internet protocol addresses.
# Visit the GitHub Repository at https://github.com/zackbradys/wireshark-geolocator.
# Last motified on 01/02/2021 by zackbradys

from geolite2 import geolite2
import socket, subprocess

# For wireless adapter/interface use, uncomment the line below
# cmd = r"C:\Program Files\Wireshark\tshark.exe -i Wi-Fi"

# For wired adapter/interface use, comment the line below
cmd = r"C:\Program Files\Wireshark\tshark.exe -i Ethernet"

# Start Wireshark Geolocator Script
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
local_ip = socket.gethostbyname(socket.gethostname())

reader = geolite2.reader()

def determine_location(ip):
    location = reader.get(ip)
    
    try:
        country = location["country"]["names"]["en"]
    except:
        country = "Indeterminable"

    try:
        subdivision = location["subdivisions"][0]["names"]["en"]
    except:
        subdivision = "Indeterminable"    

    try:
        city = location["city"]["names"]["en"]
    except:
        city = "Indeterminable"
    
    return country, subdivision, city


for line in iter(process.stdout.readline, b""):
    columns = str(line).split(" ")

    if "UDP" in columns or "SKYPE" in columns:
        
        if "->" in columns:
            src_ip = columns[columns.index("->") - 1]
        elif "\\xe2\\x86\\x92" in columns:
            src_ip = columns[columns.index("\\xe2\\x86\\x92") - 1]
        else:
            continue
            
        if src_ip == local_ip:
            continue

        try:
            country, sub, city = determine_location(src_ip)
            print(src_ip + " = " + "Location Info: " + country + " | " + sub + " | " + city)
        except:
            try:
                true_ip = socket.gethostbyname(src_ip)
                country, sub, city = determine_location(true_ip)
                print(src_ip + " = " + "Location Info: " + country + " | " + sub + " | " + city)
            except:
                print("Indeterminable")

                
# End Wireshark Geolocator Script
