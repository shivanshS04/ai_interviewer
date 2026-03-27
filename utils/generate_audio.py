import edge_tts
import asyncio
import threading

async def generate_audio_async(text):
    communicate = edge_tts.Communicate(text,voice="en-IN-PrabhatNeural")
    await communicate.save("speech.mp3")

def generate_audio(text):
    """Synchronous wrapper for generate_audio_async that runs in a separate thread to avoid event loop conflicts."""
    err = []
    def runner():
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(generate_audio_async(text))
            loop.close()
        except Exception as e:
            err.append(e)

    thread = threading.Thread(target=runner)
    thread.start()
    thread.join()
    
    if err:
        raise err[0]
