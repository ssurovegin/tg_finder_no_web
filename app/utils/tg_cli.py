import os
from telethon import TelegramClient

from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())



client = TelegramClient('finder', os.getenv('API_ID'), os.getenv('API_HASH'))

async def start_client():
    await client.start()

def get_telephone_client() -> TelegramClient:
    return client