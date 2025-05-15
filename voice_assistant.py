import os
from dotenv import load_dotenv  # type: ignore
from elevenlabs.client import ElevenLabs  # type: ignore
from elevenlabs.conversational_ai.conversation import Conversation  # type: ignore
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface  # type: ignore
from elevenlabs.types import ConversationConfig  # type: ignore

print("Current working directory:", os.getcwd())  # Prints current folder your script runs from
print("Files in directory:", os.listdir())

# Load environment variables
load_dotenv("credentials.env")  # specify your env file if not '.env'

# Get variables by their names in the env file
API_KEY = os.getenv("API_KEY")
AGENT_ID = os.getenv("AGENT_ID")

print("AGENT_ID:", AGENT_ID)
print("API_KEY:", API_KEY)

if not API_KEY or not AGENT_ID:
    raise ValueError("Missing API_KEY or AGENT_ID from .env file")

# Rest of your code remains unchanged...

user_name = "Marylyne"
schedule = "your boyfriend's birthday is on the 10th of this july, and you have a meeting with your boss on the 20th at 10 AM. You also have a dentist appointment on the 25th at 3 PM."
prompt = f"You are a helpful assistant. Your interlocutor has the following schedule: {schedule}."
first_message = f"Hello {user_name}, how can I help you today?"

conversation_override = {
    "agent": {
        "prompt": {"prompt": prompt},
        "first_message": first_message,
    },
}

config = ConversationConfig(
    conversation_config_override=conversation_override,
    extra_body={},
    dynamic_variables={},
)

client = ElevenLabs(api_key=API_KEY)

def print_agent_response(response):
    print(f"Agent: {response}")

def print_interrupted_response(original, corrected):
    print(f"Agent interrupted, truncated response: {corrected}")

def print_user_transcript(transcript):
    print(f"User: {transcript}")

conversation = Conversation(
    client,
    AGENT_ID,
    config=config,
    requires_auth=True,
    audio_interface=DefaultAudioInterface(),
    callback_agent_response=print_agent_response,
    callback_agent_response_correction=print_interrupted_response,
    callback_user_transcript=print_user_transcript,
)

conversation.start_session()
