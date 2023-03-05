import openai
import requests

openai.api_key = "your key here"

messages = [
    {"role": "system", "content": "You are a kind helpful assistant."}
]



URL = "https://api.openai.com/v1/chat/completions"

payload = {
"model": "gpt-3.5-turbo",
"messages": [{"role": "user", "content": f"where is indore?"}],
"temperature" : 1.0,
"top_p":1.0,
"n" : 1,
"stream": False,
"presence_penalty":0,
"frequency_penalty":0,
}

headers = {
"Content-Type": "application/json",
"Authorization": f"Bearer {openai.api_key}"
}

response = requests.post(URL, headers=headers, json=payload, stream=False)

print("response", response.content)