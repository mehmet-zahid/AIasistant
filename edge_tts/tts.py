#!/usr/bin/env python3

"""
Example of dynamic voice selection using VoicesManager.
"""

import asyncio
import random

import edge_tts
from edge_tts import VoicesManager

TEXT = "Hi, my name is Edge. I am a text to speech engine. I can speak in many languages."
OUTPUT_FILE = "en.mp3"

class SpeakerManager:
    def __init__(self) -> None:
        self.voice_file = "voices.txt"
        self.speakers = []
        self.read_file()
    
    def read_file(self) -> list:
        with open(self.voice_file, "r") as f:
            speaker_infos = f.read().split("\n\n")
            for speaker in speaker_infos:
                speaker_info = speaker.split("\n")
                name = speaker_info[0].split(':')[1].strip()
                language = name.split('-')[0].strip()
                gender = speaker_info[1].split(':')[1].strip()
                self.speakers.append({
                    'Name': name,
                    'Gender': gender,
                    'Language': language
                })
              
    def get_voices(self, language: str=None) -> list:
        if language:
            
            found =[speaker for speaker in self.speakers if speaker['Language'] == language]
            print(f'Found {len(found)} speakers for {language}')
            return found
        return self.speakers
    
async def test_speakers():
    sm = SpeakerManager()
    voices = sm.get_voices(language='en')
    for voice in voices:
        communicate = edge_tts.Communicate(TEXT, voice["Name"])

async def amain() -> None:
    """Main function"""
    voices = await VoicesManager.create()
    chosed_voices = []
    chosed_voices.append(voices.find(Gender="Male", Language="en"))
    chosed_voices.append(voices.find(Gender="Female", Language="en"))
    for voice in chosed_voices:
        communicate = edge_tts.Communicate(TEXT, random.choice(voice)["Name"])
        await communicate.save(OUTPUT_FILE)


if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    try:
        loop.run_until_complete(amain())
    finally:
        loop.close()