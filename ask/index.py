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
from ask.consts import app_directory, api_key_key

async def main_impl():
    conversation = {}
    
    # Handler for ?? (ctrl + c)
    def quit_handler(sig, frame):
        print("\nExiting script...")
        id = save_to_file(conversation)
        print("Conversation ID: ", id)
        sys.exit(0)

    signal.signal(signal.SIGINT, quit_handler)

    parser = argparse.ArgumentParser(description="🤖 ChatGPT CLI")
    parser.add_argument(
        "command", choices=["init"], help="Set up your OpenAI credentials", nargs="?"
    )
    parser.add_argument(
        "-c", "--conversation", help="Use with the ID printed at the end of a previous conversation to resume that same conversation.  Will not work if the conversation has been deleted.", nargs=1
    )
    args = parser.parse_args()

    # Handle init setup
    if args.command == "init":
        print(
            Fore.YELLOW + "Welcome to ask! To get started you will need to generate an OpenAI API key and paste it here to save it to your ask config.\n\nVisit " + Fore.WHITE + "https://platform.openai.com/api-keys." + Fore.YELLOW + "\n\nThe key should be like sk-{20chars}\n" + Style.RESET_ALL
        )
        key = input("Please paste your key: ")
        os.makedirs(app_directory, exist_ok=True)
        with open(os.path.expanduser(app_directory), "w+") as file:
            file.write(f"{api_key_key}={key.strip()}")
        print("Success!  You are ready to ask your first question.")

    # Make sure an API key is set
    try:
        check_for_config()
    except Exception as e:
        print(Fore.RED, e, Style.RESET_ALL)
        sys.exit(1)

    # TODO: clean out old conversations
        
    if args.conversation:
        # TODO - validate, load into conversation object if present
        pass

    while True:
        fetched_data_flag = asyncio.Event()

        # Prompt user for their question
        user_input = input("> ")

        # Store their question in the conversation dictionary
        conversation[time.time()] = {'content': user_input, 'role': 'user'}

        # Simultaneous kick off the API request and printing the waiting message
        # The fetch_data function also writes the response to the conversation dictionary
        await asyncio.gather(
            fetch_data(conversation, fetched_data_flag), print_waiting(fetched_data_flag)
        )

        print("\n")


def main():
    # Asyncio lib needed so the data request and wait message can happen simultaneously (requests lib is blocking)
    asyncio.run(main_impl())


if __name__ == "__main__":
    main()
