import requests
import xml.etree.ElementTree as ET
from pyutra.ColorText import ColorText
from pyutra.pastelib.Pastelib import Pastelib
from pyutra.CoolDebugging import CoolDebugging

color_system = ColorText()
debug_system = CoolDebugging()

class User:
    def __init__(self, api_key: str, user_key: str = None, username: str = None, password: str = None):
        self.api_key = api_key

        if user_key == None:
            if username == None or password == None:
                debug_system.error("Can't get user key without the username or password")
            else:
                data = {
                    "api_dev_key": api_key,
                    "api_user_name": username,
                    "api_user_password": password
                }

                res = requests.post("https://pastebin.com/api/api_login.php", data=data)

                if res.status_code == 200:
                    self.user_key = res.text
                elif res.text == "Bad API request, invalid login":
                    debug_system.error("Incorrect username or password")
                    self.user_key = None
                else:
                    debug_system.error(f"Failed to set user key\n{res.text}")
                    self.user_key = None
        else:
            self.user_key = user_key

    def list_pastes(self, limit: int = 50):
        if limit > 1000:
            limit = 1000
        if limit < 1:
            limit = 1

        data = {
            "api_dev_key": self.api_key,
            "api_user_key": self.user_key,
            "api_results_limit": limit,
            "api_option": "list"
        }

        res = requests.post("https://pastebin.com/api/api_post.php", data=data)

        if res.status_code == 200:
            root = ET.fromstring(res.text)

            pastes = []

            for paste in root.findall('paste'):
                paste_data = {
                    'paste_key': paste.find('paste_key').text,
                    'paste_date': paste.find('paste_date').text,
                    'paste_title': paste.find('paste_title').text or '',
                    'paste_size': paste.find('paste_size').text,
                    'paste_expire_date': paste.find('paste_expire_date').text,
                    'paste_private': paste.find('paste_private').text,
                    'paste_format_long': paste.find('paste_format_long').text or '',
                    'paste_format_short': paste.find('paste_format_short').text,
                    'paste_url': paste.find('paste_url').text,
                    'paste_hits': paste.find('paste_hits').text
                }
                pastes.append(paste_data)

            return pastes
        else:
            return False

    def delete_paste(self, url: str):
        if url.startswith("https://") or url.startswith("http://"):
            paste_id = Pastelib(self.api_key).get_paste_id(url)
        else:
            paste_id = url
        data = {
            "api_dev_key": self.api_key,
            "api_user_key": self.user_key,
            "api_option": "delete",
            "api_paste_key": paste_id
        }
        res = requests.post("https://pastebin.com/api/api_post.php", data=data)
        try:
            if res.status_code == 200:
                return True
            else:
                return False
        except Exception:
            return False

    def get_user_info(self):
        data = {
            "api_dev_key": self.api_key,
            "api_user_key": self.user_key,
            "api_option": "userdetails"
        }

        res = requests.post("https://pastebin.com/api/api_post.php", data=data)
        if res.status_code == 200:
            root = ET.fromstring(res.text)

            user_data = {
                'user_name': root.find('user_name').text,
                'user_format_short': root.find('user_format_short').text,
                'user_expiration': root.find('user_expiration').text,
                'user_avatar_url': root.find('user_avatar_url').text,
                'user_private': root.find('user_private').text,
                'user_website': root.find('user_website').text or '',
                'user_email': root.find('user_email').text,
                'user_location': root.find('user_location').text or '',
                'user_account_type': root.find('user_account_type').text
            }

            return user_data
        else:
            return False

    def get_private_paste(self, url: str, json: bool = False):
        if url.startswith("https://") or url.startswith("http://"):
            paste_id = Pastelib(self.api_key).get_paste_id(url)
        else:
            paste_id = url

        data = {
            "api_dev_key": self.api_key,
            "api_user_key": self.user_key,
            "api_paste_key": paste_id,
            "api_option": "show_paste"
        }

        res = requests.post(f"https://pastebin.com/api/api_raw.php", data=data)

        if res.status_code == 200:
            if json == False:
                return res.text
            else:
                return res.json()
        else:
            return False