from fastapi import FastAPI, HTTPException
import redis
import json
import os
from typing import List, Dict, Any

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

app = FastAPI(title="Event Read Service")

@app.get("/")
def read_root():
    return {"message": "Event Read Service"}

@app.get("/events/", response_model=List[Dict[str, Any]])
def get_all_events():
    """Get all events from Redis"""
    try:
        # Get all events from the Redis list
        events_data = redis_client.lrange("events", 0, -1)
        
        # Parse JSON strings to Python dictionaries
        events = [json.loads(event) for event in events_data]
        
        return events
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve events: {str(e)}")

@app.get("/events/count")
def get_events_count():
    """Get the count of events in Redis"""
    try:
        count = redis_client.llen("events")
        return {"count": count}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to count events: {str(e)}")

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