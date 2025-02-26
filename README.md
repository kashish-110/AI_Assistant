# AI Voice Assistant Backend

## 📌 Overview
This project is an AI-powered voice assistant backend built using **FastAPI**, **LLaMA-2**, **Google TTS**, and **MongoDB**. It can:
- Process and respond to user queries using **LLaMA-2**.
- Store interaction history in **MongoDB**.
- Convert AI-generated text responses into speech using **Google TTS**.
- Be deployed in a **Dockerized environment**.

## 🚀 Features
- **FastAPI Backend** for handling user requests.
- **LLaMA-2 Model** for AI-generated responses.
- **Google TTS** for speech synthesis.
- **MongoDB Storage** for conversation history.
- **Docker Support** for containerized deployment.

## 📂 Project Structure
```
📦 AI-Assistant
 ┣ 📂 app
 ┃ ┣ 📜 main.py              # FastAPI server
 ┃ ┣ 📜 requirements.txt     # Python dependencies
 ┣ 📜 Dockerfile             # Docker configuration
 ┣ 📜 README.md              # Project documentation
 ┣ 📜 .env                   # Environment variables
```

## 🔧 Installation & Setup
### 1️⃣ **Clone the Repository**
```sh
git clone https://github.com/yourusername/ai-assistant.git
cd ai-assistant
```

### 2️⃣ **Create Virtual Environment & Install Dependencies**
```sh
python -m venv venv
source venv/bin/activate  # For Mac/Linux
venv\Scripts\activate     # For Windows
pip install -r requirements.txt
```

### 3️⃣ **Set Up Environment Variables**
Create a `.env` file in the root directory:
```
MONGO_URI=mongodb://localhost:27017
MODEL_PATH=/path/to/llama/model.bin
```

### 4️⃣ **Run the FastAPI Server**
```sh
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 📌 API Endpoints
| Method | Endpoint | Description |
|--------|----------------|--------------------------------------|
| `POST` | `/book-appointment/` | AI-generated response for user input |
| `POST` | `/text-to-speech/` | Convert text response to speech |
| `GET`  | `/get-interactions/{user_id}` | Retrieve user conversation history |
| `GET`  | `/` | Health check |

## 🐳 Docker Deployment
### 1️⃣ **Build the Docker Image**
```sh
docker build -t ai-assistant .
```

### 2️⃣ **Run the Container**
```sh
docker run -p 8000:8000 --env-file .env ai-assistant
```

## 🚀 Deploy on DockerHub
### 1️⃣ **Login to DockerHub**
```sh
docker login
```

### 2️⃣ **Tag the Image**
```sh
docker tag ai-assistant yourusername/ai-assistant:latest
```

### 3️⃣ **Push the Image**
```sh
docker push yourusername/ai-assistant:latest
```

## 🛠 Troubleshooting
- **Docker Daemon Not Running?** Restart Docker Desktop and ensure WSL 2 backend is enabled.
- **MongoDB Connection Issues?** Ensure MongoDB is running and accessible via `MONGO_URI`.
- **AI Model Loading Error?** Verify the correct path to LLaMA model in `MODEL_PATH`.

## 📜 License
This project is licensed under the **MIT License**.

---
🔗 **Author:** Your Name  
📧 **Contact:** your.email@example.com

