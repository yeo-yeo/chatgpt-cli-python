import json
import aiohttp
from ask.utils import get_api_key
from colorama import Style

async def fetch_data(user_input, fetched_data):
    api_key = get_api_key()
    
    headers = {"Authorization": f"Bearer {api_key}", 'content-type': 'application/json'}

    url = f'https://api.openai.com/v1/chat/completions'

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": user_input}],
        "temperature": 0.7,
        "stream": True
      }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=json.dumps(payload), headers=headers) as response:
                if response.status == 200:
                    # Response received - can stop printing the 'Thinking...' message
                    fetched_data.set()
                    whole_response = []

                    print(Style.RESET_ALL, '\n\n🤖:')
                    # Iterate through the response content in chunks
                    async for chunk in response.content:
                        try:
                            # Remove the 'data: ' prefix from SSE response
                            parsed = json.loads(chunk[6:].decode('utf-8')) 
                            chunk_message = parsed['choices'][0]['delta']['content'] 
                            whole_response.append(chunk_message)
                            print(chunk_message, end='', flush=True)
                        except:
                            pass
                    return whole_response
                else:
                    print(f"Error calling OpenAI.  API response: {response.status}")
    except aiohttp.ClientError as e:
        print(f"An error occured: {e}")