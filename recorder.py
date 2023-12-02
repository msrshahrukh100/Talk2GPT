import pyaudio
import math
import struct
import wave
import time
from chatgpt import ChatGPT
import vlc

Threshold = 10

SHORT_NORMALIZE = (1.0/32768.0)
number_of_frames = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
swidth = 2
TIMEOUT_LENGTH = 2


class Recorder:

    @staticmethod
    def rms(frames):
        count = len(frames) / swidth
        # count = 4096 the number of frames
        format = "%dh" % (count)
        shorts = struct.unpack(format, frames)
        sum_squares = 0.0
        # len(shorts) = 4096
        for sample in shorts:
            n = sample * SHORT_NORMALIZE
            sum_squares += n * n
        rms = math.pow(sum_squares / count, 0.5)

        return rms * 1000

    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.player = vlc.MediaPlayer("output.mp3")
        self.stream = self.p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  output=True,
                                  frames_per_buffer=number_of_frames)

    def record(self):
        self.player.stop()
        print('Listening...')
        rec = []
        current = time.time()
        end = time.time() + TIMEOUT_LENGTH

        while current <= end:

            data = self.stream.read(number_of_frames)
            if self.rms(data) >= Threshold: 
                end = time.time() + TIMEOUT_LENGTH
            current = time.time()
            rec.append(data)
        self.write(b''.join(rec))

    def write(self, recording):
        wf = wave.open("input.wav", 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(recording)
        wf.close()

    def listen(self):
        print('Listening beginning')
        chatgpt = ChatGPT()
        while True:
            input = self.stream.read(number_of_frames, exception_on_overflow=False)
            rms_val = self.rms(input)
            if rms_val > Threshold and not self.player.get_state().__str__() == 'State.Playing':
                self.record()
                chatgpt.get_openai_response_as_audio()
                self.player.play()