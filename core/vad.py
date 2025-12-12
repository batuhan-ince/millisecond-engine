import torch
import numpy as np
import asyncio

class VoiceActivityDetector:
    def __init__(self, threshold=0.5):
        self.model, utils = torch.hub.load(
            repo_or_dir='snakers4/silero-vad',
            model='silero_vad',
            force_reload=False,
            onnx=False
        )
        self.get_speech_timestamps, _, self.read_audio, _, _ = utils
        self.threshold = threshold
        self.buffer = []
        print(">> VAD Model Loaded (Silero)")

    def is_speech(self, audio_chunk):
        # Audio chunk (bytes) -> Float32 Tensor
        audio_int16 = np.frombuffer(audio_chunk, dtype=np.int16)
        audio_float32 = audio_int16.astype(np.float32) / 32768.0
        tensor = torch.from_numpy(audio_float32)
        
        # Get probability
        speech_prob = self.model(tensor, 16000).item()
        return speech_prob > self.threshold