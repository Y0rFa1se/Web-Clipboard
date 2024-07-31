import requests

class Webhook:
    is_enabled = False
    url = ""

    @classmethod
    def configure(cls, SETTINGS):
        cls.is_enabled = SETTINGS["WEBHOOK"]["ENABLED"]
        cls.url = SETTINGS["WEBHOOK"]["URL"]

    @staticmethod
    def send(txt):
        if Webhook.is_enabled:
            message = {"text": txt}
            requests.post(Webhook.url, json=message)

            return True
        
        return False