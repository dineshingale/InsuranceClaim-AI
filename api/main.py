import os
import sys
import uvicorn
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.router import router

app = FastAPI(
    title="Insurance Claims Fraud Detection API",
    description="ML-powered API for detecting insurance claim fraud, authenticity, and priority assessment",
    version="1.0.0"
)

# Configure CORS for external app integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include prediction router
app.include_router(router, prefix="/api", tags=["predictions"])

@app.get("/")
def read_root():
    return {
        "message": "Insurance Claims Fraud Detection API",
        "docs": "/docs",
        "health": "/api/health"
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=os.getenv("ENV", "development") == "development"
    )
