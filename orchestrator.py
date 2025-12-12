import asyncio
import os
import time
from colorama import Fore, Style
# Kendi modüllerimiz
from core.vad import VoiceActivityDetector
from core.audio_interface import AudioInterface
from core.llm_service import LLMService
from utils.wav_helper import save_pcm_as_wav

class MillisecondEngine:
    def __init__(self):
        print(">> Initializing Engine components...")
        self.vad = VoiceActivityDetector(threshold=0.5)
        self.audio = AudioInterface()
        self.llm = LLMService()
        
        self.is_listening = True
        self.TEMP_INPUT = "temp_input.wav"
        self.TEMP_OUTPUT = "temp_output.mp3"

    async def run(self):
        await self.audio.start_stream()
        print(Fore.GREEN + "\n>> SYSTEM READY. Speak now!" + Style.RESET_ALL)

        buffer = bytearray()
        silence_frames = 0
        
        while True:
            chunk = await self.audio.input_queue.get()
            
            if self.is_listening:
                if self.vad.is_speech(chunk):
                    print(Fore.YELLOW + "I", end="", flush=True) # I = Input/Speech
                    buffer.extend(chunk)
                    silence_frames = 0
                else:
                    if len(buffer) > 0:
                        print(Fore.BLACK + ".", end="", flush=True) # . = Silence
                        silence_frames += 1
                        
                        if silence_frames > 20: 
                            print(Fore.CYAN + "\n>> End of turn detected. Processing..." + Style.RESET_ALL)
                            await self.process_turn(buffer)
                            
                            # Reset buffer
                            buffer = bytearray()
                            silence_frames = 0

    async def process_turn(self, audio_buffer):
        self.is_listening = False
        start_time = time.time()

        save_pcm_as_wav(audio_buffer, self.TEMP_INPUT)
        
        # 2. STT (Whisper API)
        print(">> Transcribing...")
        try:
            user_text = await self.llm.transcribe_audio(self.TEMP_INPUT)
        except Exception as e:
            print(Fore.RED + f"STT Error: {e}" + Style.RESET_ALL)
            self.is_listening = True
            return

        if not user_text.strip():
            print(">> No speech detected (Empty transcription).")
            self.is_listening = True
            return

        print(Fore.WHITE + f"User: {user_text}" + Style.RESET_ALL)

        # 3. LLM Stream (GPT-4o)
        print(Fore.MAGENTA + "AI: ", end="")
        full_response = ""
        
        async for token in self.llm.get_response_stream(user_text):
            print(token, end="", flush=True)
            full_response += token
        print(Style.RESET_ALL)

        # 4. TTS (OpenAI)
        print("\n>> Synthesizing Audio...")
        audio_file = await self.llm.text_to_speech(full_response, self.TEMP_OUTPUT)
        
        # 5. Play Audio
        print(f">> Playing ({time.time() - start_time:.2f}s latency)")
        
        if os.name == 'posix': # Mac/Linux
            os.system(f"afplay {audio_file}") 
        else: # Windows
            os.system(f"start {audio_file}")

        self.is_listening = True
        print(Fore.GREEN + "\n>> Listening..." + Style.RESET_ALL)

if __name__ == "__main__":
    try:
        engine = MillisecondEngine()
        asyncio.run(engine.run())
    except KeyboardInterrupt:
        print("\n>> Stopping...")