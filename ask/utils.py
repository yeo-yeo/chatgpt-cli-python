from dotenv import dotenv_values, find_dotenv
import os
from colorama import Fore, Style
import asyncio
import datetime
import json

config_path = os.path.expanduser(f"~/.ask/.config")


def check_for_config():
    # specifically check for existence of file rather than keys?
    config = get_config()
    if not config.get("API_KEY", None):
        raise Exception("Config not set up properly.  Have you run `ask init`?")


def get_config():
    return dotenv_values(config_path)


def get_api_key():
    config = get_config()
    api_key = config.get("API_KEY", None)
    if api_key == None:
        print("Unable to find API key.  Have you created run `ask init`?")
        return
    return api_key


async def print_waiting(fetched_data):
    print(Fore.YELLOW + "\nThinking", end="")
    while not fetched_data.is_set():
        print(".", end="", flush=True)
        await asyncio.sleep(0.5)
    print(Style.RESET_ALL)


def save_to_file(output):
    current_datetime = datetime.datetime.now()
    date, time = current_datetime.strftime("%Y%m%d"), current_datetime.strftime(
        "%H%M%S"
    )
    output_directory = f"~/.ask/{date}"
    expanded_path = os.path.expanduser(output_directory)
    os.makedirs(expanded_path, exist_ok=True)
    file_path = os.path.join(expanded_path, f"{time}")
    with open(file_path, "w+") as file:
        file.write(json.dumps(output))
    return f"{date}/{time}"
