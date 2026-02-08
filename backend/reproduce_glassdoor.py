import asyncio
import os
from rag_engine import RAGEngine

async def test_glassdoor():
    print("Initializing RAG Engine...")
    try:
        engine = RAGEngine()
    except Exception as e:
        print(f"Failed to initialize engine: {e}")
        return

    sender = "Glassdoor Jobs <noreply@glassdoor.com>"
    content = """
    'GLASSDOOR'
    Jobs for Torsa
    See the latest roles at Zest Life Singapore, Opportunity Presented by Recruitment and more. To help refine this list, search for more jobs.
    Life, Business & Personal Solutions Strategist (Mid-Career Friendly) role at Zest Life Singapore: you would be a great fit!
    Unsolicited job offers from Glassdoor. Some roles listed include 'Life, Business & Personal Solutions Strategist' at Zest Life Singapore. Salary ranges appear broad. Email from noreply@glassdoor.com.
    """

    print(f"\nAnalyzing message from: {sender}")
    result = await engine.analyze_message(sender, content)
    
    print("\n--- ANALYSIS RESULT ---")
    print(f"Risk Score: {result.get('risk_score')}")
    print(f"Risk Level: {result.get('risk_level')}")
    print(f"Category: {result.get('category')}")
    print(f"Recommended Action: {result.get('recommended_action')}")
    print(f"Explanation: {result.get('explanation')}")

if __name__ == "__main__":
    asyncio.run(test_glassdoor())
