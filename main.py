import whisper
from openai import OpenAI
import os
import sys
import time

client = OpenAI()

model = whisper.load_model("base")

def speech_to_text():    
    result = model.transcribe("input.wav", fp16=False)
    print(f"You: {result['text']}")
    return result["text"]

def get_openai_response():
    content = speech_to_text()
    sys.stdout.write("\rThinking...")
    sys.stdout.flush()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": content
            }
        ]
    )
    return response.choices[0].message.content

def get_audio_response():
    try:
        os.remove("output.mp3")
    except OSError:
        pass
    text = get_openai_response()
    response = client.audio.speech.create(
      model="tts-1",
      voice="alloy",
      input=text
    )
    response.stream_to_file(f"output.mp3")
    sys.stdout.write(f"\rAI: {text}")
    sys.stdout.flush()
    
    