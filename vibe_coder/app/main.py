from dotenv import load_dotenv # api picker
from openai import AsyncOpenAI # api caller
from openai.helpers import LocalAudioPlayer # audio player
import asyncio # asyncio library
load_dotenv() # load env variables

import speech_recognition as sr # speech to text
from .graph import graph # graph

messages = [] # messages

openai = AsyncOpenAI() # openai api caller

async def tts(text: str):
    async with openai.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="coral",
        input=text,
        instructions="Speak in a funny tone",
        response_format="pcm"
    ) as response:
        await LocalAudioPlayer().play(response)

def main():
    r = sr.Recognizer()  # Speech to Text

    with sr.Microphone() as source:  # Mic Access
        r.adjust_for_ambient_noise(source) # adjust for ambient noise
        r.pause_threshold = 2 # pause threshold

        while True:
            print("Speak something...")
            audio = r.listen(source)

            print("Processing Audio... (STT)")
            stt = r.recognize_google(audio)

            print("You said:", stt)
            messages.append({ "role": "user", "content": stt })

            for event in graph.stream({ "messages": messages }, stream_mode="values"):
                if "messages" in event:
                    messages.append({ "role": "assistant", "content": event["messages"][-1].content })
                    event["messages"][-1].pretty_print()


# main()

asyncio.run(tts(text="Hey! (laugh) Nice to meet you. How can I help you with coding"))