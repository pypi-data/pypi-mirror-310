import json
import sys
import os
from pyutra.ColorText import ColorText

cool_text = ColorText()

class Extras:
    def clear(self):
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    def pause(self, message:str="Enter to continue...\n", color:str="cyan"):
        input(cool_text.colorize(message, color))

    def status_builder(self, status:bool, response):
        return {
            "status": status,
            "response": response
        }

    def json_formater(self, data:dict, indent:int=4):
        return json.dumps(data, indent=indent)