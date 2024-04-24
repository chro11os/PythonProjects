import time
import speedtest
import socket
import requests
import platform

def get_internet_speed():
    st = speedtest.Speedtest()
    download_speed = st.download() / 1024 / 1024  # Convert to Mbps
    upload_speed = st.upload() / 1024 / 1024  # Convert to Mbps
    return download_speed, upload_speed

def get_ip_address():
    ip = socket.gethostbyname(socket.gethostname())
    return ip

def get_os_info():
    os_name = platform.system()
    os_model = platform.machine()
    os_release = platform.release()
    return f"Operating System: {os_name}\nModel: {os_model}\nRelease: {os_release}"

def search(query):
    api_key = "AIzaSyAqkKSyBEIwP_puokeU8_WA2TO600ajcAs"
    search_engine_id = "f657634a782ef4aaa"
    url = f'https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={query}'
    response = requests.get(url)
    data = response.json()
    for item in data['items']:
        print(item['title'])
        print(item['link'])
        print(item['snippet'])
        print()

if __name__ == "__main__":
    print("Welcome to Pysearch, a Terminal-based search engine")
    print("Waiting for connection...")
    time.sleep(3)
    print("Connected.\n")

    print("Connection details:")
    download_speed, upload_speed = get_internet_speed()
    print(f"Download speed: {download_speed:.2f} Mbps")
    print(f"Upload speed: {upload_speed:.2f} Mbps")
    print(f"IP address: {get_ip_address()}")
    print(get_os_info())

    while True:
        query = input("\nEnter your search query (type 'exit' to quit): ")
        if query.lower() == 'exit':
            break
        search(query)

