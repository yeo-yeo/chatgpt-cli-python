#!/usr/bin/env python3

import argparse
import os
import asyncio
import signal
import sys
from colorama import Fore, Style
import time

from ask.openai import fetch_data
from ask.utils import print_waiting, save_to_file, check_for_config


async def main_impl():
    conversation = {}

    def signal_handler(sig, frame):
        print("\nExiting script...")
        id = save_to_file(conversation)
        print("Conversation ID: ", id)
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser(description="🤖 ChatGPT CLI")
    parser.add_argument(
        "command", choices=["init"], help="Set up your OpenAI credentials", nargs="?"
    )
    args = parser.parse_args()

    if args.command == "init":
        print(
            "Welcome to ask! To get started you will need to generate an OpenAI API key and paste it here to save it to your ask config."
        )
        key = input("Please paste your key: ")
        if not os.path.exists(os.path.expanduser(f"~/.ask")):
            os.makedirs(os.path.expanduser(f"~/.ask"))
        with open(os.path.expanduser(f"~/.ask/.config"), "w+") as file:
            file.write(f"API_KEY={key}")
        print("Success!  You are ready to ask your first question.")

    try:
        check_for_config()
    except Exception as e:
        print(Fore.RED, e, Style.RESET_ALL)
        sys.exit(1)

    while True:
        fetched_data = asyncio.Event()
        user_input = input("> ")
        conversation[f"{time.time()}-user"] = user_input

        [[key, whole_response], _] = await asyncio.gather(
            fetch_data(user_input, fetched_data), print_waiting(fetched_data)
        )
        conversation[key] = whole_response
        print("\n")


def main():
    asyncio.run(main_impl())


if __name__ == "__main__":
    main()
