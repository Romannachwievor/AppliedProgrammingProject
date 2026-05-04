# ============================================================================
# DAY 4: Advanced API Features
# ============================================================================
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import json
from pathlib import Path

app = FastAPI(
    title="Applied Programming Course API",
    description="Reference implementation for Day 4",
    version="1.0.0"
)

class GreetingResponse(BaseModel):
    message: str

@app.get("/", response_model=GreetingResponse)
def read_root():
    """Welcome endpoint - returns greeting message"""
    return {"message": "Hello World!"}

@app.get("/greetings/{name}", response_model=GreetingResponse)
def read_greeting(name: str):
    """Personalized greeting endpoint - returns greeting message with name"""
    return {"message": f"Hello {name}!"}

@app.get("/is-adult/{age}")
def check_adult(age: int):
    """Check if person is an adult (18 or older)"""
    is_adult = age > 18
    return {
        "age": age,
        "is_adult": is_adult,
        "can_vote": is_adult,
        "can_drive": is_adult
    }
