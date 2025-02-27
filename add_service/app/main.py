from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis
import json
import os
from typing import Dict, Any
import uuid
from datetime import datetime

# Get Redis connection details from environment variables or use defaults
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

# Create Redis client
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True
)

app = FastAPI(title="Event Add Service")

class Event(BaseModel):
    """Model for event data"""
    name: str
    data: Dict[str, Any]

@app.get("/")
def read_root():
    return {"message": "Event Add Service"}

@app.post("/events/", status_code=201)
def add_event(event: Event):
    """Add a new event to Redis"""
    try:
        # Generate a unique ID for the event
        event_id = str(uuid.uuid4())
        
        # Add timestamp
        timestamp = datetime.utcnow().isoformat()
        
        # Create event object
        event_data = {
            "id": event_id,
            "name": event.name,
            "data": event.data,
            "timestamp": timestamp
        }
        
        # Store in Redis
        # We'll use a Redis list called 'events' to store all events
        redis_client.rpush("events", json.dumps(event_data))
        
        return {"id": event_id, "message": "Event added successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add event: {str(e)}")

@app.get("/health")
def health_check():
    """Health check endpoint"""
    try:
        # Check if Redis is available
        redis_client.ping()
        return {"status": "healthy"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 