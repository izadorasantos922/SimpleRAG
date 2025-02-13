# Conect to Gemini's API 

import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

if API_KEY is None:
    raise ValueError("GEMINI_API_KEY environment variable not set")

user_question = input("What do you want to ask Nilza today? ")

url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
headers = {"Content-Type": "application/json"}
data = {"contents": [{"parts": [{"text": user_question}]}]}

response = requests.post(url, headers=headers, json=data, params={"key": API_KEY})

if response.status_code == 200:
    answer = response.json()
    print("Nilza's answer: ", answer['candidates'][0]['content']['parts'][0]['text'])
else:
    print(f"Failed to generate content. Status code: {response.status_code}")
    print(response.text)
