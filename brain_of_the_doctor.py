import os
import base64
from groq import Groq
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
HF_TOKEN = os.environ.get("HF_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

import base64

def encode_image(image_path):
    """Encodes an image dynamically without letting python cache the results."""
    if not image_path:
        return None
    
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
query = "Is there something wrong with my face?"
model = "meta-llama/Llama-4-Scout-17B-16E-Instruct"

def analyze_image_with_query(query,model,encoded_image):
    client = Groq(api_key=GROQ_API_KEY)
    
    
    

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

  
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model
    )
    return chat_completion.choices[0].message.content

