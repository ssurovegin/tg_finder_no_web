import os
from telethon import TelegramClient

from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv(), override=True)

SESSION_PATH = os.getenv('SESSION_PATH')
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')


client = TelegramClient(SESSION_PATH, API_ID, API_HASH,
                        device_model='iPhone 13', system_version='iOS 18',
                        app_version='11.11')

def get_telephone_client() -> TelegramClient:
    return client
