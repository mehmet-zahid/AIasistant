import pyaudio
import wave
from scipy.io import wavfile
import noisereduce as nr



class AudioREcorder:
    def __init__(self) -> None:
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 512
        self.RECORD_SECONDS = 5
        self.WAVE_OUTPUT_FILENAME = "temp.wav"
        self.device_index = 2

        self.audio = pyaudio.PyAudio()
        self.index = 6
        self.audio_init()
        
    def audio_init(self):

        print("----------------------record device list---------------------")
        info = self.audio.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        for i in range(0, numdevices):
            if (self.audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print("Input Device id ", i, " - ", self.audio.get_device_info_by_host_api_device_index(0, i).get('name'))

        print("-------------------------------------------------------------")

        self.index = int(input())
        print("recording via index (selected device) " + str(self.index))

    def close(self):
        self.audio.terminate()


    def record(self, noise_reduction=False):
        stop = False

        while not stop:
            print("Press 's' to start recording and 'q' to stop recording [don't forget to press 'Enter']")
            if 's' in input():
                stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS,
                                    rate=self.RATE, input=True, input_device_index=self.index,
                                    frames_per_buffer=self.CHUNK)
                print("Recording started")
                Recordframes = []

                while True:
                    for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
                        data = stream.read(self.CHUNK)
                        Recordframes.append(data)
                    if stop:
                        break

                    if 'q' in input():
                        print("Recording stopped")
                        stop = True

                stream.stop_stream()
                stream.close()

                # save audio file
                self.waveFile = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')

                self.waveFile.setnchannels(self.CHANNELS)
                self.waveFile.setsampwidth(self.audio.get_sample_size(self.FORMAT))
                self.waveFile.setframerate(self.RATE)
                self.waveFile.writeframes(b''.join(Recordframes))
                self.waveFile.close()

        if noise_reduction:
            # load data
            rate, data = wavfile.read(self.WAVE_OUTPUT_FILENAME)

            # perform noise reduction
            reduced_noise = nr.reduce_noise(y=data, sr=rate, n_jobs=3)

            # write audio to file
            wavfile.write("temp.wave", rate, reduced_noise)

if __name__ == "__main__":
    try:
        audio = AudioREcorder()
        audio.record()
        audio.close()
    except KeyboardInterrupt:
        audio.close()
        audio.waveFile.close()
        print("Keyboard Interrupt")