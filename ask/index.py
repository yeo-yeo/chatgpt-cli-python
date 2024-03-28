#!/usr/bin/env python3

import argparse
import os
import json
from dotenv import dotenv_values
import aiohttp
import asyncio

async def fetch_data(url,headers,payload, fetched_data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=json.dumps(payload), headers=headers) as response:
            data = await response.json()
            # Set the event to notify that data fetch is completed
            fetched_data.set()
            return data
        
async def print_waiting(fetched_data):
    print('\nThinking', end='') 
    while not fetched_data.is_set():
        print('.', end='', flush=True)
        await asyncio.sleep(0.5) 

async def main_impl():
    config_path = os.path.expanduser(f'~/.ask')
    config = dotenv_values(config_path)
    # parser = argparse.ArgumentParser(description="🤖 ChatGPT CLI")
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

    api_key = config['API_KEY']
    headers = {"Authorization": f"Bearer {api_key}", 'content-type': 'application/json'}


    waiting, response = await asyncio.gather(
          print_waiting(fetched_data),
          fetch_data(url, headers, payload, fetched_data)
      )

    answer = response['choices'][0]['message']['content']
    print('\n')
    print(answer)

def main():
    asyncio.run(main_impl())

if __name__ == '__main__':
    main()