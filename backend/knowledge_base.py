import chromadb
import os
from typing import List, Dict

class KnowledgeBase:
    def __init__(self, db_path: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection("scam_patterns")
        self._initialize_data()

    def _initialize_data(self):
        # Advanced scam patterns derived from user feedback and curated datasets
        patterns = [
            # --- Inheritance & Compensation Scams (User Screenshot 1) ---
            {
                "id": "inheritance_un_imf",
                "text": "Beneficiary, We have concluded to release your outstanding compensation, Inheritance payment of $2,700,000.00 after meeting with United Nations and IMF. Contact Director Jerry Campbell.",
                "metadata": {"category": "Inheritance Scam", "risk_level": "High"}
            },
            # --- Sextortion & Blackmail (User Screenshot 2) ---
            {
                "id": "blackmail_sextortion",
                "text": "If you dont send me $1000 in 24 hours, i will send your pictures to your family and friends.",
                "metadata": {"category": "Blackmail / Sextortion", "risk_level": "High"}
            },
            # --- Job & Tasks Scams ---
            {
                "id": "job_scam_social_media",
                "text": "Earn $300-500 daily by liking YouTube videos or completing simple tasks. Urgent contact via Telegram or WhatsApp.",
                "metadata": {"category": "Job Scams", "risk_level": "High"}
            },
            # --- Technical Support & Account Suspension ---
            {
                "id": "account_suspension_urgent",
                "text": "Your Amazon/Netflix/Apple account will be permanently closed in 2 hours due to unauthorized activity. Verify now to prevent data loss.",
                "metadata": {"category": "Account Security Phishing", "risk_level": "High"}
            }
        ]
        
        # Add patterns
        if self.collection.count() < 10: # Allow re-initialization if small
            self.collection.add(
                documents=[p["text"] for p in patterns],
                metadatas=[p["metadata"] for p in patterns],
                ids=[p["id"] for p in patterns]
            )

    def query(self, text: str, n_results: int = 3) -> List[Dict]:
        results = self.collection.query(
            query_texts=[text],
            n_results=n_results
        )
        
        extracted = []
        if results["documents"]:
            for i in range(len(results["documents"][0])):
                extracted.append({
                    "content": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i]
                })
        return extracted

if __name__ == "__main__":
    kb = KnowledgeBase()
    print(f"Collection count: {kb.collection.count()}")
