import requests
from pyutra.ColorText import ColorText
from pyutra.CoolDebugging import CoolDebugging

color_system = ColorText()
debug_system = CoolDebugging()

class Pastelib:
  def __init__(self, api_key:str):
    self.api_key = api_key

  def create_paste(self, text:str, name:str=None, privacy:str="public", format:str="text", expire="never"):
    if privacy == "public":
      privacy = 0
    if privacy == "unlisted":
      privacy = 1
    if privacy == "private":
      privacy = 2

    expire = expire.lower()

    if expire == "never":
      expire = "N"
    elif expire == "10 minutes":
      expire = "10M"
    elif expire == "1 hour":
      expire = "1H"
    elif expire == "1 day":
      expire = "1D"
    elif expire == "1 week":
      expire = "1W"
    elif expire == "2 weeks":
      expire = "2W"
    elif expire == "1 month":
      expire = "1M"
    elif expire == "6 months":
      expire = "6M"
    elif expire == "1 year":
      expire = "1Y"

    data = {
      "api_dev_key": self.api_key,
      "api_option": "paste",
      "api_paste_code": text,
      "api_paste_name": name,
      "api_paste_private": privacy,
      "api_paste_format": format,
      "api_paste_expire_date": expire
    }

    try:
      res = requests.post("https://pastebin.com/api/api_post.php", data=data)

      if res.status_code == 200:
        return res.text
      else:
        return False
    except Exception as e:
      return False

  def get_paste(self, url:str, json:bool=False):
    if url.startswith("https://") or url.startswith("http://"):
      paste_id = self.get_paste_id(url)
    else:
      paste_id = url

    res = requests.get(f"https://pastebin.com/raw/{paste_id}")

    if res.status_code == 200:
      if json == False:
        return res.text
      else:
        return res.json()
    else:
      return False

  def get_paste_id(self, url:str):
    return url.split("/")[-1]
