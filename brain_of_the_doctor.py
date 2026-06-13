import os
import base64
from groq import Groq
from dotenv import load_dotenv, find_dotenv

# Step 1: Load environment variables
load_dotenv(find_dotenv())
HF_TOKEN = os.environ.get("HF_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Pass the API key 
client = Groq(api_key=GROQ_API_KEY)

# Step 2: Convert image into binary encoding methods
with open("acne.jpg", "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

# Step 3: Setup Multimodal Payload
query = "Is there something wrong with my face?"
model = "meta-llama/Llama-4-Scout-17B-16E-Instruct"

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": query
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{encoded_image}"
                }
            }
        ]
    }
]

# Step 4: Send request to Groq Vision
print("Sending image and query to Groq...")
chat_completion = client.chat.completions.create(
    messages=messages,
    model=model
)

# Print 
print("\n" + "="*30 + " DOCTOR BOT RESPONSE " + "="*30)
print(chat_completion.choices[0].message.content)