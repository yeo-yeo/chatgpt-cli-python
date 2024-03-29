#!/usr/bin/env python3

import argparse
import os
import asyncio

import datetime

from ask.openai import fetch_data
from ask.utils import print_waiting
        


async def main_impl():
    # argparse.ArgumentParser(description="🤖 ChatGPT CLI")
    # parser.add_argument('-x', '--xample', help='Just testing')
    # args = parser.parse_args()
    # print('You passed', args.xample)

    fetched_data = asyncio.Event()  
    user_input = input('> ')



    whole_response = await asyncio.gather(
          fetch_data(user_input, fetched_data),
          print_waiting(fetched_data)
      )

   # print(answer)

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