#!/usr/bin/env python3

import argparse
import requests
import os
import json
from dotenv import dotenv_values



def main():
    config_path = os.path.expanduser(f'~/.ask')
    config = dotenv_values(config_path)
    # parser = argparse.ArgumentParser(description="🤖 ChatGPT CLI")
    # parser.add_argument('-x', '--xample', help='Just testing')
    # args = parser.parse_args()
    # print('You passed', args.xample)

  
    response = input('What is your question? \n')

    url = f'https://api.openai.com/v1/chat/completions'

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": response}],
        "temperature": 0.7
      }

    api_key = config['API_KEY']
    headers = {"Authorization": f"Bearer {api_key}", 'content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    response_json = response.json()
    answer = response_json['choices'][0]['message']['content']
    print('\n')
    print(answer)

# not totally clear to me if i need this
if __name__ == '__main__':
    main()