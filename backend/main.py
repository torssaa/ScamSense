from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_engine import RAGEngine
import uvicorn
import asyncio

app = FastAPI(title="ScamSense Backend")

# Rate limiting settings
MAX_REQUESTS = 300
request_count = 0

# Enable CORS for the Chrome extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict to extension ID or specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalysisRequest(BaseModel):
    sender: str
    content: str

engine = None
init_error = "Engine not yet initialized"

@app.on_event("startup")
async def startup_event():
    global engine, init_error
    try:
        engine = RAGEngine()
        init_error = None
        print("ScamSense RAG Engine initialized successfully.")
    except Exception as e:
        init_error = str(e)
        print(f"Error initializing RAG Engine: {e}")

@app.get("/health")
async def health():
    return {
        "status": "healthy" if engine else "error",
        "service": "ScamSense Backend",
        "model_loaded": engine is not None,
        "error": init_error
    }

@app.post("/analyze")
async def analyze(request: AnalysisRequest):
    global request_count
    
    if engine is None:
        raise HTTPException(
            status_code=503, 
            detail=f"AI Engine Error: {init_error}. Please ensure GEMINI_API_KEY is set in backend/.env"
        )
    
    # Check hard limit
    if request_count >= MAX_REQUESTS:
        print(f"RATE LIMIT: Hard stop reached ({MAX_REQUESTS} requests).")
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded: Hard stop at {MAX_REQUESTS} requests reached."
        )

    # Increment and check batch limit (Every 3 requests, wait 1 minute)
    request_count += 1
    
    if request_count % 3 == 0:
        print(f"BATCH LIMIT: {request_count} requests reached. Waiting 60 seconds as requested...")
        await asyncio.sleep(60)
    else:
        # Standard 1s delay for non-batch requests
        print(f"Request {request_count}/{MAX_REQUESTS}: Applying 1s safety delay...")
        await asyncio.sleep(1)
    
    try:
        result = await engine.analyze_message(request.sender, request.content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
