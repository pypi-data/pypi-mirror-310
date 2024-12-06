import requests

class Nukify:
    def __init__(self, token:str):
        self.token = token

    def base_url(self, version:int):
        return f"https://discord.com/api/v{version}/"

    def verify_token(self):
        base_url = self.base_url(10)

        headers = {
            "Authorization": "Bot " + self.token
        }

        res = requests.get(base_url+"applications/@me", headers=headers)

        if res.status_code == 200:
            return True
        else:
            return False

    def get_bot_info(self):
        base_url = self.base_url(10)

        headers = {
            "Authorization": "Bot " + self.token
        }

        res = requests.get(base_url + "applications/@me", headers=headers)

        if res.status_code == 200:
            return res.json()
        else:
            return False

    def grab_webhooks(self, guild_id:int):
        base_url = self.base_url(10)

        headers = {
            "Authorization": "Bot "+self.token
        }

        res = requests.get(base_url+f"guilds/{guild_id}/webhooks", headers=headers)

        if res.status_code == 200:
            return res.json()
        else:
            return False

    def create_webhook(self, name:str, channel_id:int, avatar:str=None):
        base_url = self.base_url(10)

        headers = {
            "Authorization": "Bot " + self.token
        }

        data = {
            "name": name,
            "avatar": {
                "url": avatar
            }
        }

        res = requests.get(base_url + f"channels/{channel_id}/webhooks", headers=headers)

        if res.status_code == 200:
            return res.json()
        else:
            return False