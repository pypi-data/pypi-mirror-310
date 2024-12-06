import requests
import socket

def domain_to_ip(domain:str):
    try:
        ip = socket.gethostbyname(domain)

        return ip
    except Exception:
        return False

def get_webpage(url:str, hide:str):
    headers = {}

    if hide == True:
        headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0"

    res = requests.get(url, headers=headers)

    if res.status_code == 200:
        return res.text
    else:
        return False

def grab_robots(domain:str):
    res = requests.get(f"{domain}/robots.txt")

    if res.status_code == 200:
        return res.text
    else:
        return False