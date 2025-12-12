import wave

def save_pcm_as_wav(pcm_data, filename, rate=16000, channels=1, sampwidth=2):
    """
    Saves raw PCM bytes to a valid WAV file with headers.
    """
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sampwidth) # 2 bytes for int16
        wf.setframerate(rate)
        wf.writeframes(pcm_data)