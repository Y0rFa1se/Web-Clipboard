from modules.webhook import Webhook
from modules.webconfig import WebConfig
from modules.database import DB
from modules.storage import Storage
from modules.auth import Auth
from modules.logger import Logger

import json

with open("settings.json", "r") as f:
    SETTINGS = json.load(f)

Webhook.configure(SETTINGS)
WebConfig.configure(SETTINGS)
DB.configure(SETTINGS)
Storage.configure(SETTINGS)
Auth.configure(SETTINGS)
Logger.configure(SETTINGS)