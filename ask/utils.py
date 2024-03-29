from dotenv import dotenv_values
import os
from colorama import Fore, Style
import asyncio

def get_config():
    config_path = os.path.expanduser(f'~/.ask/.config')
    config = dotenv_values(config_path)
    return config

def get_api_key():
   config = get_config()
   api_key = config.get('API_KEY', None)
   if api_key == None:
        print('Unable to find API key.  Have you created run `ask init`?')
        return
   return api_key


async def print_waiting(fetched_data):
    print(Fore.YELLOW + '\nThinking', end='') 
    while not fetched_data.is_set():
        print('.', end='', flush=True)
        await asyncio.sleep(0.5) 
    print(Style.RESET_ALL)