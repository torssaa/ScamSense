import os
import google.generativeai as genai
from dotenv import load_dotenv

# Use absolute paths like in the main app
base_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(base_dir, ".env"))
load_dotenv(os.path.join(base_dir, ".env.local"))

def test_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found.")
        return

    print(f"Using API Key: {api_key[:10]}...")
    genai.configure(api_key=api_key)
    
    try:
        print("Testing Gemini 2.0 Flash...")
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content("Hello, respond with 'SUCCESS'")
        print(f"Response: {response.text}")
        print("✅ Gemini API is working correctly.")
    except Exception as e:
        print(f"❌ Gemini API Error: {str(e)}")
        
        print("\nAttempting fallback to Gemini 1.5 Flash...")
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content("Hello, respond with 'SUCCESS'")
            print(f"Response: {response.text}")
            print("✅ Gemini 1.5 Flash is working.")
        except Exception as e2:
            print(f"❌ Gemini 1.5 Flash Error: {str(e2)}")

if __name__ == "__main__":
    test_gemini()
