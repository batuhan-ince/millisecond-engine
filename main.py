import asyncio
from dotenv import load_dotenv
from orchestrator import MillisecondEngine

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    print("---------------------------------------")
    print(" The Millisecond Engine v1.0")
    print(" Architecture from 'The Millisecond Matters'")
    print("---------------------------------------")
    
    try:
        engine = MillisecondEngine()
        asyncio.run(engine.run())
    except KeyboardInterrupt:
        print("\n>> Shutting down.")