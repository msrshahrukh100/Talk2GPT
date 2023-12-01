import whisper
from openai import OpenAI
import os
import sys


class ChatGPT:
    def __init__(self):
        self.client = OpenAI()
        self.whisper_model = whisper.load_model("base")

    def get_text_from_speech(self):    
        result = self.whisper_model.transcribe("input.wav", fp16=False)
        print(f"You: {result['text']}")
        return result["text"]

    def get_openai_response_as_text(self, content):
        sys.stdout.write("\rThinking...")
        sys.stdout.flush()
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": content
                }
            ]
        )
        return response.choices[0].message.content

    def get_openai_response_as_audio(self):
        try:
            os.remove("output.mp3")
        except OSError:
            pass
        
        text_from_speech = self.get_text_from_speech()
        openai_response = self.get_openai_response_as_text(text_from_speech)
        response = self.client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=openai_response
        )
        response.stream_to_file(f"output.mp3")
        sys.stdout.write(f"\rAI: {openai_response}")
        sys.stdout.flush()
        
    

    