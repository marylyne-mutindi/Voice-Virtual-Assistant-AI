import os
import re
from dotenv import load_dotenv  # type: ignore
from elevenlabs.client import ElevenLabs  # type: ignore
from elevenlabs.conversational_ai.conversation import Conversation  # type: ignore
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface  # type: ignore
from elevenlabs.types import ConversationConfig  # type: ignore

print("Current working directory:", os.getcwd())
print("Files in directory:", os.listdir())

# Load environment variables
load_dotenv("credentials.env")  # specify your env file if not '.env'

API_KEY = os.getenv("API_KEY")
AGENT_ID = os.getenv("AGENT_ID")

print("AGENT_ID:", AGENT_ID)
print("API_KEY:", API_KEY)

if not API_KEY or not AGENT_ID:
    raise ValueError("Missing API_KEY or AGENT_ID from .env file")

user_name = "Marylyne"

# Initial schedule as a dictionary for easier updates
schedule_data = {
    "Monday": [
        {"time": "9:00 AM - 10:00 AM", "event": "Team meeting"},
        {"time": "10:30 AM - 11:30 AM", "event": "Project discussion"},
        {"time": "1:00 PM - 2:00 PM", "event": "Client call"},
    ],
    "Tuesday": [
        {"time": "9:00 AM - 10:00 AM", "event": "Team meeting"},
        {"time": "10:30 AM - 11:30 AM", "event": "Project discussion"},
        {"time": "1:00 PM - 2:00 PM", "event": "Client call"},
    ],
    "Wednesday": [
        {"time": "9:00 AM - 10:00 AM", "event": "Team meeting"},
        {"time": "10:30 AM - 11:30 AM", "event": "Project discussion"},
        {"time": "1:00 PM - 2:00 PM", "event": "Client call"},
    ],
    "Thursday": [
        {"time": "9:00 AM - 10:00 AM", "event": "Team meeting"},
        {"time": "10:30 AM - 11:30 AM", "event": "Project discussion"},
        {"time": "1:00 PM - 2:00 PM", "event": "Client call"},
    ],
}

def schedule_to_string():
    """Convert schedule_data dict to a string representation for prompt."""
    output = []
    for day, events in schedule_data.items():
        event_strings = [f"{e['time']}: {e['event']}" for e in events]
        output.append(f"{day}: " + ", ".join(event_strings))
    return "\n".join(output)

schedule_str = schedule_to_string()

prompt = f"You are a helpful assistant. Your interlocutor {user_name} has the following schedule:\n{schedule_str}"
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
    # Detect if user wants to schedule a meeting
    detected = detect_schedule_intent(transcript)
    if detected:
        day, time_range, description = detected
        add_meeting(day, time_range, description)
        # Have the assistant respond verbally
        conversation.say_text(f"Got it! I've scheduled {description} on {day} at {time_range}.")

def detect_schedule_intent(transcript):
    """
    Very basic regex to detect:
    "Schedule a meeting on Friday at 4 PM for performance review"
    """
    pattern = r"schedule .* on (\w+) at ([\d:APMapm ]+) for (.+)"
    match = re.search(pattern, transcript, re.IGNORECASE)
    if match:
        day = match.group(1).capitalize()
        time_range = match.group(2).strip()
        description = match.group(3).strip()
        return day, time_range, description
    return None

def add_meeting(day, time_range, description):
    if day not in schedule_data:
        schedule_data[day] = []
    schedule_data[day].append({"time": time_range, "event": description})
    print(f"📅 Added meeting: '{description}' on {day} at {time_range}")

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
