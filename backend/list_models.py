import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
load_dotenv(os.path.join(os.path.dirname(__file__), ".env.local"), override=True)
api_key = os.getenv("GEMINI_API_KEY")

print("Listing available models...")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"Name: {m.name}")
        print(f"Supported methods: {m.supported_generation_methods}")
        print("-" * 20)
