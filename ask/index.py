#!/usr/bin/env python3

import argparse
import os
import json
from dotenv import dotenv_values
import aiohttp
import asyncio
from colorama import Fore, Style
import datetime

async def fetch_data(url,headers,payload, fetched_data):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=json.dumps(payload), headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    # Set the event to notify that data fetch is completed
                    fetched_data.set()
                    return data
                else:
                    print(f"Error calling OpenAI.  API response: {response.status}")
    except aiohttp.ClientError as e:
        print(f"An error occured: {e}")
        
async def print_waiting(fetched_data):
    print(Fore.YELLOW + '\nThinking', end='') 
    while not fetched_data.is_set():
        print('.', end='', flush=True)
        await asyncio.sleep(0.5) 
    print(Style.RESET_ALL)

async def main_impl():
    config_path = os.path.expanduser(f'~/.ask/.config')
    config = dotenv_values(config_path)
    # argparse.ArgumentParser(description="🤖 ChatGPT CLI")
    # parser.add_argument('-x', '--xample', help='Just testing')
    # args = parser.parse_args()
    # print('You passed', args.xample)

    # used to manage breaking the loop when the request finishes (is this a good approach?)
    fetched_data = asyncio.Event()  
    response = input('> ')

    url = f'https://api.openai.com/v1/chat/completions'

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": response}],
        "temperature": 0.7
      }

    api_key = config.get('API_KEY', None)
    
    if api_key == None:
        print('Unable to find API key.  Have you created run `ask init`?')
        return
    
    headers = {"Authorization": f"Bearer {api_key}", 'content-type': 'application/json'}

    response, _ = await asyncio.gather(
          fetch_data(url, headers, payload, fetched_data),
          print_waiting(fetched_data)
      )

    answer = response['choices'][0]['message']['content']
    print('\n🤖:')
    print(answer)

    current_datetime = datetime.datetime.now()

    date = current_datetime.strftime("%Y-%m-%d")
    time = current_datetime.strftime("%H:%M:%S")
    output_directory = '~/.ask/{date}' 
    # if not os.path.exists(output_directory):
    #     os.makedirs(output_directory)
    # with (open('{output_directory}/{time}.txt'),'w') as file:
    #     file.write(answer)

def main():
    asyncio.run(main_impl())

if __name__ == '__main__':
    main()