import os
import tempfile
from faster_whisper import WhisperModel

# Initialize model (downloading if necessary, can be optimized to load once)
# Using 'tiny' or 'base' for speed, or 'small' for better accuracy.
# Since it's running locally, let's start with 'base.en'.
model_size = "base.en"
model = WhisperModel(model_size, device="cpu", compute_type="int8")

def transcribe_audio(audio_bytes):
    """
    Transcribes audio bytes to text using Faster Whisper.
    """
    if not audio_bytes:
        return ""
    
    try:
        # Create a temporary file to save the audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(audio_bytes)
            temp_audio_path = temp_audio.name

        segments, info = model.transcribe(temp_audio_path, beam_size=5)
        
        transcription = ""
        for segment in segments:
            transcription += segment.text

        # Clean up
        os.remove(temp_audio_path)
        
        return transcription.strip()
    except Exception as e:
        print(f"Error during transcription: {e}")
        return ""
