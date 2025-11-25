from fastapi import FastAPI
from datetime import datetime
import os

app = FastAPI(title="DataPress POC API")

@app.get("/")
def root():
    return {
        "service": "api",
        "environment": os.getenv("DP_ENV", "dev"),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "message": os.getenv("WELCOME_MESSAGE", "Bienvenue sur l'API DataPress POC")
    }

@app.get("/health")
def health():
    # Peut être utilisé par les probes Kubernetes
    return {"status": "ok", "ts": datetime.utcnow().isoformat() + "Z"}
