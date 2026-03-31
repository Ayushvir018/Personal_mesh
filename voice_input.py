import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np
import tempfile
import os
from faster_whisper import WhisperModel

# Load model - using small for better accuracy
model = WhisperModel("small", device="cpu", compute_type="int8")

def record_audio(duration=10, sample_rate=16000):
    print("Recording... speak now")
    audio = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype='int16',
        device=2
    )
    sd.wait()
    print("Recording done.")
    return audio, sample_rate

def transcribe_audio(audio, sample_rate):
    temp_file = tempfile.mktemp(suffix=".wav")
    wav.write(temp_file, sample_rate, audio)
    
    segments, info = model.transcribe(temp_file, language="en")
    text = " ".join([seg.text for seg in segments]).strip()
    
    os.remove(temp_file)
    return text

def voice_to_text(duration=10):
    audio, sample_rate = record_audio(duration, sample_rate=16000)
    text = transcribe_audio(audio, sample_rate)
    return text