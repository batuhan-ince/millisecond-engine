import pyaudio
import asyncio
import queue

class AudioInterface:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.input_queue = asyncio.Queue()
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self.chunk = 512  # 32ms window for VAD

    def input_callback(self, in_data, frame_count, time_info, status):
        self.input_loop.call_soon_threadsafe(self.input_queue.put_nowait, in_data)
        return (None, pyaudio.paContinue)

    async def start_stream(self):
        self.input_loop = asyncio.get_running_loop()
        self.stream = self.p.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk,
            stream_callback=self.input_callback
        )
        print(">> Microphone Stream Started")

    def play_audio(self, audio_data):
        stream = self.p.open(
            format=self.format,
            channels=self.channels,
            rate=24000, # OpenAI TTS default
            output=True
        )
        stream.write(audio_data)
        stream.stop_stream()
        stream.close()