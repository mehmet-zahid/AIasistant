import sounddevice as sd
import numpy as np

# Set up the audio recording parameters
sample_rate = 16000  # Sample rate (in Hz)
duration = 10  # Duration of the recording (in seconds)

# Create an empty list to store the recorded audio frames
audio_frames = []

# Define the audio callback function
def audio_callback(indata, frames, time, status):
    if status:
        print("Error: {}".format(status))
    
    # Append the audio frames to the list
    audio_frames.append(indata.copy())

def transcribe(audio_data):
    

# Start the audio recording
with sd.InputStream(callback=audio_callback, channels=1, samplerate=sample_rate):
    print("Recording started. Speak now...")
    sd.sleep(int(duration * 1000))
    print("Recording stopped.")

# Concatenate the audio frames into a single ndarray
audio_data = np.concatenate(audio_frames)

# Convert the audio data to the required format for Whisper (int16, mono)
audio_data = np.squeeze(audio_data)
audio_data = audio_data.astype(np.int16)

# Transcribe the speech using Whisper
transcription = transcribe(audio_data)

# Print the transcription
print("Transcription:", transcription)
