import whisper

model = whisper.load_model("base")

def transcribe(recording):
    audio = whisper.load_audio(recording)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    options = whisper.DecodingOptions(language='tr', fp16=False)

    result = whisper.decode(model, mel, options=options)

    if result.no_speech_prob < 0.5:
        print(result.text)
        