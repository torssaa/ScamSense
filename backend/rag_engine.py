import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from typing import Dict, Any
from knowledge_base import KnowledgeBase

# Handle environment variables (local overrides standard)
base_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(base_dir, ".env"), override=True)
load_dotenv(os.path.join(base_dir, ".env.local"), override=True)

class RAGEngine:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print(f"CRITICAL ERROR: GEMINI_API_KEY not found in {base_dir}")
            raise ValueError("GEMINI_API_KEY missing")
        
        genai.configure(api_key=api_key)
        # Using Gemini 2.0 Flash (External search disabled due to library compatibility)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.kb = KnowledgeBase()

    async def analyze_message(self, sender: str, content: str) -> Dict[str, Any]:
        print(f"\n--- SCAMSENSE ANALYSIS START ---")
        print(f"Sender: {sender}")
        print(f"Content Length: {len(content)}")
        
        # Retrieve similar patterns from knowledge base
        context_patterns = self.kb.query(content)
        context_text = "\n".join([f"- {p['content']} (Category: {p['metadata']['category']})" for p in context_patterns])

        prompt = f"""
        You are an expert cybersecurity analyst.
        
        --- STEP 1: VERIFICATION (INTERNAL) ---
        Verify the sender domain and message content using your internal knowledge base:
        1. Check if the sender domain MATCHES the official company website (e.g. glassdoor.com sending for Glassdoor).
        2. Analyze if the message is a standard marketing/notification email (Unsubscribe link, no urgent threats).
        3. Recall if this specific sender/domain is a known legit source.

        --- STEP 2: ANALYZE ---
        Determine the risk based on the verification above.

        --- SENDER ---
        {sender}

        --- MESSAGE CONTENT ---
        {content}

        --- CONTEXT (Known Scam Patterns) ---
        {context_text}

        --- OUTPUT RULES ---
        - FIRST LINE: Must be the Scam Type OR "Legitimate Notification" / "Marketing Email" / "Conversational Message".
            - **CRITICAL**: If Risk is LOW, the Type MUST be "Legitimate", "Marketing", "Newsletter", or "Conversational Message".
        - MAX LENGTH: 7 lines, 60 words.
        - RECOMMENDED ACTION: 
            - If Risk is HIGH/MEDIUM: Choose "Report", "Block", "Ignore", or "Do not click on link".
            - If Risk is LOW: Use "No Action Needed".
        
        --- RISK TIERS ---
        - HIGH (85-100%): Verified scam, impersonation, credential phishing.
        - MEDIUM (25-84%): Suspicious but unverified, emotional manipulation, unsolicited offers.
        - LOW (0-24%): Verified Legitimate sender, Marketing emails from reputable companies, or Casual/Conversational messages (e.g., "Hello", "How are you?") with no malicious intent.

        Follow this JSON format exactly:
        {{
            "risk_score": int,
            "risk_level": "High" | "Medium" | "Low",
            "category": "string",
            "explanation": "string",
            "sentiment": "string",
            "recommended_action": "string"
        }}
        """

        try:
            print(f"ScamSense: Sending request to Gemini ({self.model.model_name})...")
            response = self.model.generate_content(prompt)
        except Exception as e:
            error_str = str(e)
            print(f"ScamSense: Gemini API Error: {error_str}")
            if "429" in error_str or "quota" in error_str.lower():
                return {
                    "risk_score": 0,
                    "risk_level": "Safe",
                    "category": "Quota Exceeded",
                    "explanation": "Gemini API daily free quota reached. Please wait a few minutes or check your API key limits.",
                    "sentiment": "N/A",
                    "recommended_action": "Check back later or use a different API key."
                }
            raise e

        try:
            # Extract JSON from potential markdown markers
            text = response.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            
            print(f"ScamSense: AI Response: {text[:100]}...")
            return json.loads(text)
        except Exception as e:
            # Fallback if AI output is not valid JSON
            print(f"ScamSense: JSON Parse Error: {str(e)}")
            return {
                "risk_score": 50,
                "risk_level": "Medium",
                "category": "Analysis Error",
                "explanation": f"Could not parse AI response. Error: {str(e)}",
                "sentiment": "Unknown",
                "recommended_action": "Do not click on link"
            }

if __name__ == "__main__":
    # Test
    # engine = RAGEngine()
    pass
