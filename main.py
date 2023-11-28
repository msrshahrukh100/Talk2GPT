import whisper
from openai import OpenAI

client = OpenAI()

model = whisper.load_model("base")

def speech_to_text():    
    result = model.transcribe("input.wav", fp16=False)
    print(f"You: {result['text']}")
    return result["text"]

def get_openai_response():
    content = speech_to_text()
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
    text = get_openai_response()
    response = client.audio.speech.create(
      model="tts-1",
      voice="alloy",
      input=text
    )
    response.stream_to_file(f"output.mp3")
    