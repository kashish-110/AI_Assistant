import requests
import speech_recognition as sr
import os
import gtts
from playsound import playsound

API_URL = "http://127.0.0.1:8000"
USER_ID = "user_123"  # Unique user ID

def listen_to_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening... Speak now!")
        recognizer.adjust_for_ambient_noise(source)
        
        try:
            audio = recognizer.listen(source, timeout=10)
            text = recognizer.recognize_google(audio)
            print(f"🗣 You said: {text}")
            return text

        except sr.WaitTimeoutError:
            print("⏳ No speech detected, try again.")
            return None
        except sr.UnknownValueError:
            print("❌ Could not understand audio.")
            return None
        except sr.RequestError as e:
            print(f"❌ API Error: {e}")
            return None

def ask_ai(user_input):
    """Send user input to AI API and handle errors."""
    try:
        payload = {
            "user_id": USER_ID,
            "user_input": user_input
        }

        response = requests.post(f"{API_URL}/book-appointment/", json=payload)
        print("📤 Sent Request:", payload)

        if response.status_code != 200:
            print(f"❌ API Error: {response.status_code}, Response: {response.text}")
            return None
        
        response_json = response.json()
        print("📥 AI Response:", response_json)

        return response_json.get("response", "")

    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to the server.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
        return None

def text_to_speech(text):
    """Convert AI text response to speech and play it."""
    try:
        response = requests.post(f"{API_URL}/text-to-speech/", json={"text": text})

        if response.status_code == 200:
            with open("response.mp3", "wb") as f:
                f.write(response.content)
            print("🔊 Playing response audio...")
            playsound("response.mp3")
        else:
            print(f"❌ TTS API Error: {response.status_code}, Response: {response.text}")

    except Exception as e:
        print(f"❌ Error calling TTS API: {e}")

# 🎙 Main Interaction Loop
while True:
    user_input = listen_to_speech()

    if user_input and user_input.lower() in ["exit", "quit"]:
        print("👋 Exiting...")
        break
    
    if user_input:
        response = ask_ai(user_input)
        if response:
            print("🤖 AI:", response)
            text_to_speech(response)  # Speak AI response

            while True:
                follow_up = listen_to_speech()
                if follow_up:
                    response = ask_ai(follow_up)
                    if response:
                        print("🤖 AI:", response)
                        text_to_speech(response)
                else:
                    break  # Stop if no more input
