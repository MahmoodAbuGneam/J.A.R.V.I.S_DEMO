from openai import OpenAI
import time
from pygame import mixer
import os
#https://platform.openai.com/playground/assistants
# Initialize the client and mixer
client = OpenAI(api_key="OPENAI_API_KEY", default_headers={"OpenAI-Beta": "assistants=v2"})
mixer.init()

assistant_id = "assistant_ID"
thread_id = "thread_ID"

# Retrieve the assistant and thread
assistant = client.beta.assistants.retrieve(assistant_id)
thread = client.beta.threads.retrieve(thread_id)

def ask_question_memory(question):
    global thread
    client.beta.threads.messages.create(thread.id, role="user", content=question)
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)
    
    while (run_status := client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)).status != 'completed':
        if run_status.status == 'failed':
            return "The run failed."
        time.sleep(1)
    
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    
    full_response = ""
    for content in messages.data[0].content:
        if content.type == 'text':
            full_response += content.text.value + "\n"
    
    return full_response.strip()

def generate_tts(sentence, speech_file_path):
    response = client.audio.speech.create(model="tts-1", voice="echo", input=sentence)
    response.stream_to_file(speech_file_path)
    return str(speech_file_path)

def play_sound(file_path):
    mixer.music.load(file_path)
    mixer.music.play()

def TTS(text):
    if not text.strip():  # Checks if the text is empty or only contains whitespace
        text = "Hold on a minute Sir ."
    speech_file_path = generate_tts(text, "speech.mp3")
    play_sound(speech_file_path)
    while mixer.music.get_busy():
        time.sleep(1)
    mixer.music.unload()
    os.remove(speech_file_path)
    return "done"

