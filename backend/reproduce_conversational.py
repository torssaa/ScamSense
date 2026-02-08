import asyncio
import os
from rag_engine import RAGEngine

async def test_conversational():
    print("Initializing RAG Engine...")
    try:
        engine = RAGEngine()
    except Exception as e:
        print(f"Failed to initialize engine: {e}")
        return

    sender = "Friend <+65 9123 4567>"
    content = """
    Hey man, how are you doing? Long time no see.
    Are you free for lunch next week? Let me know.
    """

    print(f"\nAnalyzing conversational message from: {sender}")
    result = await engine.analyze_message(sender, content)
    
    print("\n--- ANALYSIS RESULT ---")
    print(f"Risk Score: {result.get('risk_score')}")
    print(f"Risk Level: {result.get('risk_level')}")
    print(f"Category: {result.get('category')}")
    print(f"Recommended Action: {result.get('recommended_action')}")
    print(f"Explanation: {result.get('explanation')}")

if __name__ == "__main__":
    asyncio.run(test_conversational())
