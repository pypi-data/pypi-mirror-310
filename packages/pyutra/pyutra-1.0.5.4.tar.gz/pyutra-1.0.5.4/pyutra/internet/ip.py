import socket

import requests

def grab_ip():
    res = requests.get("https://api.ipify.io")

    if res.status_code == 200:
        return res.text
    else:
        return False

def grab_ip_info(ip:str):
    res = requests.get(f"https://ipinfo.io/widget/demo/{ip}")

    if res.status_code == 200:
        return res.json()["data"]

def google_maps(latitude, longitude, zoom=10):
    return f"https://www.google.com/maps?q={latitude},{longitude}&zoom={zoom}"