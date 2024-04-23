import os
import time 
import speedtest
import socket

# make a speed stats for the search engine
print ("Waiting for connection")
time.sleep(1)

print("Connecting.", end="\r")
while True:
    time.sleep(1)
    print("Connecting..", end="\r")
    time.sleep(1)
    print("Connecting...", end="\r")
    time.sleep(1)
print("Connecting.", end="\r")


""" Code that returns ip address"""
def get_internet_speed():
    st = speedtest.Speedtest()
    download_speed = st.download() / 1024 / 1024  # Convert to Mbps
    upload_speed = st.upload() / 1024 / 1024  # Convert to Mbps
    return download_speed, upload_speed

download_speed, upload_speed = get_internet_speed()
if (get_internet_speed() == true):
    print("Connection successful")
print(f"Download speed: {download_speed:.2f} Mbps")
print(f"Upload speed: {upload_speed:.2f} Mbps")


""" code that returns the ip address of the computer """

def get_ip_address():
    ip = socket.gethostbyname(socket.gethostname())
    return ip

print(f"IP address: {get_ip_address()}")




# initializations 

get_internet_speed()














