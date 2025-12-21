# The Millisecond Engine ⚡️

> "We are not building chatbots anymore; we are building systems that breathe."

This is the official reference implementation for the Medium series: [**"The Millisecond Matters: Engineering SOTA Voice Agents"**](https://medium.com/@inceb1997/the-millisecond-matters-engineering-sota-voice-agents-16f32e457745).

It demonstrates how to build a real-time, interruptible voice agent using Python `asyncio`, `Silero VAD` (Voice Activity Detection), and the OpenAI stack.

## 🏗 Architecture

This engine implements the core concepts discussed in the blog series:

* [**Part 1: Async Orchestration**](https://medium.com/@inceb1997/the-millisecond-matters-engineering-sota-voice-agents-16f32e457745) – No blocking `while` loops. The brain, ears, and mouth run in parallel.
* [**Part 2: The Kill Switch (VAD)**](https://medium.com/@inceb1997/the-millisecond-matters-engineering-sota-voice-agents-16f32e457745) – Uses **Silero VAD** (running locally on CPU) to detect human speech in milliseconds and manage turn-taking.
* [**Part 3: Latency Masking**](https://medium.com/@inceb1997/part-3-the-brain-in-the-loop-llm-orchestration-tool-use-f04ae00423d3) – Handles the "thinking time" of the LLM.

**The Stack:**
* **Ears:** OpenAI Whisper API (Server-side for speed)
* **Brain:** GPT-4o-mini (Low latency reasoning)
* **Mouth:** OpenAI TTS (Alloy voice)
* **Reflexes:** PyTorch & Silero VAD (Local)

## 📂 Project Structure

```text
millisecond-engine/
├── core/
│   ├── audio_interface.py   # PyAudio streaming wrapper
│   ├── vad.py               # Silero VAD implementation
│   └── llm_service.py       # OpenAI Wrapper (STT/LLM/TTS)
├── utils/
│   └── wav_helper.py        # PCM to WAV conversion
├── main.py                  # Entry point
├── orchestrator.py          # The "Brain" logic
└── requirements.txt         # Dependencies
```

## 🚀 Getting Started

### 1. Prerequisites (Important!)

Since we are dealing with raw audio streams (PyAudio), you must install the PortAudio library on your OS before installing the Python requirements.

**MacOS:**

```bash
brew install portaudio
```

**Linux (Ubuntu/Debian):**

```bash
sudo apt-get install portaudio19-dev python3-all-dev
```

**Windows:** Usually not required. If `pip install pyaudio` fails, you may need "Microsoft Visual C++ Build Tools".

### 2. Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/batuhan-ince/millisecond-engine.git
cd millisecond-engine

# Create Virtual Environment (Recommended)
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install Python Packages
pip install -r requirements.txt
```

### 3. API Key Setup

Create a `.env` file in the root directory and add your OpenAI Key:

```plaintext
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxx
```

### 4. Run It

```bash
python main.py
```

## 🎙 Usage

Wait for the `>> SYSTEM READY. Speak now!` message.

Speak naturally. The system uses a VAD (Voice Activity Detector), so it knows when you stop talking.

Watch the logs:

* **I:** Input detected (User speaking)
* **.:** Silence detected

The system will transcribe, think, and reply with audio.

## ⚠️ Known Limitations (Educational Use)

**Audio Playback:** To keep the code simple and cross-platform compatible without complex dependencies (like ffmpeg), this engine uses `os.system` to play the generated audio files (`afplay` on Mac, `start` on Windows). In a production environment, you should use audio streaming via WebSockets.

**STT:** We use OpenAI Whisper API for high accuracy. For ultra-low latency, you would swap this with Deepgram Nova-2 or a local Whisper Turbo model.

## 📚 The Blog Series

Read the full deep-dive on how this engine was designed:

* **Part 1:** [The Millisecond War – Architecture of a Real-Time Voice Agent](https://medium.com/@inceb1997/the-millisecond-matters-engineering-sota-voice-agents-16f32e457745)
* **Part 2:** [The Art of Interruption (VAD & Barge-in Logic)](https://medium.com/@inceb1997/part-2-the-art-of-interruption-vad-barge-in-logic-167e04b735a9)
* **Part 3:** [The Brain in the Loop (Latency Masking)](https://medium.com/@inceb1997/part-3-the-brain-in-the-loop-llm-orchestration-tool-use-f04ae00423d3)
* **Part 4:** [The Soul of the Voice (Prosody & Emotion)](https://medium.com/@inceb1997/part-4-the-soul-of-the-voice-prosody-cloning-emotions-fc0a4790bb00)
* **Part 5:** [The Future (Audio-to-Audio)](https://medium.com/@inceb1997/part-5-the-future-audio-to-audio-omni-models-78deab0ffe3b)

---

Built with ❤️ by [Batuhan İnce](https://www.linkedin.com/in/batuhan-ince-050441174/)
