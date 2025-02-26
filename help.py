from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import FileResponse
from pydantic import BaseModel
from ctransformers import AutoModelForCausalLM
from pymongo import MongoClient
import os
from gtts import gTTS
from datetime import datetime
import traceback
import asyncio
from concurrent.futures import ThreadPoolExecutor

app = FastAPI()

# ✅ Load LLaMA Model
try:
    model_path = r"C:\Users\Kashish Gupta\python\AI assisstant\venv\llama-2-7b-chat.ggmlv3.q4_0.bin"
    llama_model = AutoModelForCausalLM.from_pretrained(
        model_path, model_file="llama-2-7b-chat.ggmlv3.q4_0.bin", model_type="llama"
    )
    print("✅ LLaMA model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading LLaMA model: {str(e)}")
    traceback.print_exc()
    llama_model = None

# ✅ MongoDB Setup
try:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    client = MongoClient(MONGO_URI)
    db = client["ai_assistant"]
    collection = db["interactions"]
    print("✅ MongoDB connected successfully!")
except Exception as e:
    print(f"❌ Error connecting to MongoDB: {str(e)}")
    traceback.print_exc()
    collection = None

# ✅ Request Model
class AppointmentRequest(BaseModel):
    user_id: str
    user_input: str

executor = ThreadPoolExecutor()

def count_tokens(text):
    """Estimate token count (each word ~1 token)"""
    return len(text.split())

@app.post("/book-appointment/")
async def book_appointment(request: AppointmentRequest):
    """Process appointment request, store interactions, and enable follow-ups."""
    user_id = request.user_id
    user_input = request.user_input

    print(f"📩 Received input from {user_id}: {user_input}")

    if llama_model is None:
        raise HTTPException(status_code=500, detail="AI Model not loaded.")

    # Retrieve conversation history from MongoDB (latest 10 interactions)
    if collection is not None:
        conversation_history = list(collection.find({"user_id": user_id}).sort("timestamp", -1).limit(10))
        conversation_texts = [f"User: {doc['user_input']}\nAI: {doc['ai_response']}" for doc in conversation_history]
    else:
        conversation_texts = []

    # ✅ Trim conversation to fit within 300 tokens (keeping buffer)
    MAX_TOKENS = 300
    trimmed_conversation = []
    total_tokens = 0

    for entry in reversed(conversation_texts):  # Start from oldest
        entry_tokens = count_tokens(entry)
        if total_tokens + entry_tokens > MAX_TOKENS:
            break
        trimmed_conversation.append(entry)
        total_tokens += entry_tokens

    # ✅ Form prompt with strict token control
    prompt = "\n".join(trimmed_conversation) + f"\nUser: {user_input}\nAI:"

    try:
        loop = asyncio.get_running_loop()
        response_text = await loop.run_in_executor(executor, lambda: llama_model(prompt, max_new_tokens=50))
        ai_response = response_text.strip()

        if not ai_response:
            raise HTTPException(status_code=500, detail="AI response was empty.")

        # ✅ Store interaction in MongoDB
        if collection is not None:
            collection.insert_one({
                "user_id": user_id,
                "user_input": user_input,
                "ai_response": ai_response,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        return {"response": ai_response}

    except Exception as e:
        print(f"❌ AI Error: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"AI error: {str(e)}")

@app.post("/text-to-speech/")
async def text_to_speech(text: str = Body(..., embed=True)):
    """Convert AI response to speech."""
    try:
        if not text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty.")

        tts = gTTS(text=text, lang="en")
        audio_file = "response.mp3"
        tts.save(audio_file)

        return FileResponse(audio_file, media_type="audio/mpeg", filename="response.mp3")

    except Exception as e:
        print(f"❌ TTS Error: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error generating speech: {str(e)}")

@app.get("/get-interactions/{user_id}")
async def get_interactions(user_id: str):
    """Retrieve all interactions for a user"""
    try:
        if collection is not None:
            interactions = list(collection.find({"user_id": user_id}, {"_id": 0}))  # Exclude MongoDB _id field
            return {"user_id": user_id, "interactions": interactions}
        else:
            raise HTTPException(status_code=500, detail="Database not connected.")
    except Exception as e:
        print(f"❌ Error retrieving interactions: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/")
async def root():
    """Health Check"""
    return {"message": "🚀 AI Assistant API is running!"}
