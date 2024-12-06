import requests

class Webhooks:
    def real_webhook(self, url:str):
        if url.startswith("https://discord.com/api/") or url.startswith("http://discord.com/api/"):
            res = requests.get(url)

            if res.status_code == 200:
                return True
            else:
                return False
        else:
            return False

    def send_message(self, url:str, message:str=None, embeds:list=None, file:str=None):
        extra_embeds = []
        embed = []
        if self.real_webhook(url) == False:
            return False

        data = {}

        files = {}

        if message:
            data["content"] = message

        if embeds:
            if len(embeds) > 20:
                for i in range(19):
                    embed.append(embeds[i])
                for i in embed:
                    embeds.remove(i)

                extra_embeds = embeds
            data["embeds"] = embed

        if file:
            with open(file, "rb") as f:
                files["file"] = f

        res = requests.post(url, json=data, files=files)

        if res.status_code == 200:
            if extra_embeds != []:
                self.send_message(url, message, extra_embeds, file)
            return True
        else:
            return False

    def embed_builder(self, title:str, description:str, color:int=None, image:str=None, last_embeds:list=None):
        if last_embeds == None:
            last_embeds = []

        embed = {
            "title": title,
            "description": description,
            "color": color,
            "image": {
                "url": image
            }
        }

        last_embeds.append(embed)

        return last_embeds

    def delete_webhook(self, url:str):
        res = requests.delete(url)

        if res.status_code == 200 or res.status_code == 204:
            return True
        else:
            return False

    def edit_webhook(self, url:str, name:str=None, avatar:str=None, channel:int=None):
        data = {
            "name": name,
            "channel_id": channel,
            "avatar": {
                "url": avatar
            }
        }

        res = requests.patch(url, json=data)

        if res.status_code == 200 or res.status_code == 204:
            return True
        else:
            return False

    def webhook_info(self, url):
        res = requests.get(url)

        if res.status_code == 200:
            return res.json()
        else:
            return False

    def edit_message(self, url:str, message_id:int, message:str=None, embeds:list=None, file:str=None):
        if self.real_webhook(url) == False:
            return False

        data = {}

        files = {}

        if message:
            data["content"] = message

        if embeds:
            data["embeds"] = embeds

        if file:
            with open(file, "rb") as f:
                files["file"] = f

        res = requests.post(url+"message/"+str(message_id), json=data, files=files)

        if res.status_code == 200 or res.status_code == 201:
            return True
        else:
            return False

    def delete_message(self, url:str, message_id:int):
        res = requests.delete(url+"message/"+str(message_id))

        if res.status_code == 200 or res.status_code == 201 or res.status_code == 204:
            return True
        else:
            return False