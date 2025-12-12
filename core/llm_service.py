from openai import AsyncOpenAI
import os

class LLMService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.history = [
            {"role": "system", "content": "You are a concise, ultra-fast voice assistant. Speak naturally and briefly."}
        ]

    async def transcribe_audio(self, audio_file_path):
        """
        Audio file -> Text (STT)
        Uses OpenAI Whisper model.
        """
        with open(audio_file_path, "rb") as audio_file:
            transcription = await self.client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file
            )
        return transcription.text

    async def get_response_stream(self, user_text):
        """
        Text -> Text Stream (LLM)
        Yields tokens as they arrive.
        """
        self.history.append({"role": "user", "content": user_text})
        
        stream = await self.client.chat.completions.create(
            model="gpt-4o-mini", # Hız için mini
            messages=self.history,
            stream=True
        )

        full_response = ""
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                full_response += content
                yield content
        
        # Add assistant response to history for context
        self.history.append({"role": "assistant", "content": full_response})

    async def text_to_speech(self, text, output_file="output.mp3"):
        """
        Text -> Audio File (TTS)
        """
        response = await self.client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )
        response.stream_to_file(output_file)
        return output_file