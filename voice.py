import speech_recognition as sr
import pyttsx3
from chatgpt_bot import ChatgptBot

engine = pyttsx3.init()
#chatgpt = ChatgptBot()



def speak(text):
    engine.say(text)
    engine.runAndWait()






def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Calibrating...")
        r.adjust_for_ambient_noise(source, duration=5)
        # optional parameters to adjust microphone sensitivity
        # r.energy_threshold = 200
        # r.pause_threshold=0.5

        print("Okay, go!")
        while True:
            text = ""
            print("listening now...")
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=30)
                print("Recognizing...")
                # whisper model options are found here: https://github.com/openai/whisper#available-models-and-languages
                # other speech recognition models are also available.
                text = r.recognize_whisper(
                    audio,
                    model="medium.en",
                    show_dict=True,
                )["text"]
                print('Transcribed: ', text)
            except Exception as e:
                unrecognized_speech_text = (
                    f"Sorry, I didn't catch that. Exception was: {e}s"
                )
                print(unrecognized_speech_text)
            except KeyboardInterrupt:
                print("KeyboardInterrupt")
                break
            

            #response_text = chatgpt.enter_prompt(prompt=text)
            #print(response_text)
            

