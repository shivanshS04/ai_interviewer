import edge_tts

async def generate_audio(text):
    communicate = edge_tts.Communicate(text,voice="en-IN-PrabhatNeural")
    await communicate.save("speech.mp3")
