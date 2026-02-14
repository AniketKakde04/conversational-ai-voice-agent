import logging
import os
from dotenv import load_dotenv
from livekit import agents
from livekit.agents import (
    AgentServer,
    AgentSession,
    Agent,
    llm,
    room_io,
)
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    cli,
    llm,
)

from livekit.plugins import (
    sarvam,
    openai,
    silero,
)
from livekit.agents.pipeline import VoicePipelineAgent, AgentCallContext
from livekit.plugins import sarvam

load_dotenv()
logger = logging.getLogger("sarvam-agent")

def prewarm(proc: JobContext):
    """
    Preloads the models so the first user doesn't wait.
    """
    # 1. LISTENING (Sarvam Saaras)
    proc.userdata["stt"] = sarvam.STT(
        model="saaras:v3",
        language="unknown",  # Auto-detects language
        mode="translate",    # Translates Indian languages to English for the LLM
        flush_signal=True    # CRITICAL: Allows the agent to be interrupted
    )
    
    # 2. SPEAKING (Sarvam Bulbul)
    proc.userdata["tts"] = sarvam.TTS(
        model="bulbul:v3",
        target_language_code="en-IN", # Indian English accent
        speaker="meera"               # Options: meera, aditya, etc.
    )

    # 3. THINKING (Sarvam LLM via OpenAI Compatibility)
    # We use the 'openai' plugin but point it to Sarvam's API URL
    proc.userdata["llm"] = openai.LLM(
        base_url="https://api.sarvam.ai/v1",
        api_key=os.getenv("SARVAM_API_KEY"), # Use Sarvam key, not OpenAI key
        model="sarvam-m",                    # Sarvam's LLM model
        temperature=0.5,
    )

async def entrypoint(ctx: JobContext):
    logger.info(f"Connecting to room {ctx.room.name}")
    
    # Connect to the LiveKit room
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # Use the pre-warmed models
    stt = ctx.userdata["stt"]
    tts = ctx.userdata["tts"]
    llm = ctx.userdata["llm"]

    # Initialize the Voice Pipeline
    # We create the initial chat context so the bot knows who it is
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=(
            "You are a helpful voice assistant created by Sarvam AI. "
            "You are concise, polite, and can speak about Indian topics intelligently. "
            "Keep your responses short (1-2 sentences) as this is a voice conversation."
        ),
    )

    agent = VoicePipelineAgent(
        vad=None,  # Sarvam STT handles VAD internally
        stt=stt,
        llm=llm,
        tts=tts,
        chat_ctx=initial_ctx,
        turn_detector=None, 
    )

    # Start the agent
    agent.start(ctx.room, participant=None)

    # Initial greeting
    await agent.say("Namaste! I am fully powered by Sarvam AI. How can I help you?", allow_interruptions=True)

if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            prewarm_fnc=prewarm,
        )
    )