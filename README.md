# Sarwan Voice Agent

A voice-enabled AI agent powered by LiveKit and Sarvam AI, specialized for Indian contexts.

## Features

- **Brain (LLM)**: Sarvam AI (`sarvam-m`) via OpenAI compatibility layer.
- **Ears (STT)**: Sarvam Saaras v3 (`saaras:v3`) for accurate speech-to-text.
- **Voice (TTS)**: Sarvam Bulbul v2 (`bulbul:v2`) with natural-sounding Indian voices (e.g., `meera`).
- **Real-time Interaction**: Built on LiveKit Agents framework.

## Setup

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd sarwan-voice-agent
    ```

2.  **Install Dependencies**:
    Navigate to the backend directory and install the required packages.
    ```bash
    cd backend
    python -m venv .venv
    .venv\Scripts\activate  # Windows
    # source .venv/bin/activate  # macOS/Linux
    pip install -r requirements.txt
    ```

3.  **Environment Variables**:
    Create a `.env` file in the `backend` directory with the following keys:
    ```env
    LIVEKIT_URL=<your-livekit-url>
    LIVEKIT_API_KEY=<your-livekit-api-key>
    LIVEKIT_API_SECRET=<your-livekit-api-secret>
    SARVAM_API_KEY=<your-sarvam-api-key>
    ```

## Running the Agent

Start the agent in development mode:

```bash
cd backend
python main.py dev
```

This will connect the agent to your LiveKit project. You can check the logs to verify the connection.

## Configuration

The agent is configured in `backend/main.py`. You can adjust the following settings:
- **Instructions**: Modify the system prompt to change the agent's personality.
- **Language**: STT language is set to auto-detect (`unknown`), but can be fixed to specific Indian languages (e.g., `hi-IN`).
- **Voice**: Change the TTS `speaker` to other available voices (e.g., `anushka`, `dhruv`).
