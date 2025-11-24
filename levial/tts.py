import subprocess
import time
from pathlib import Path

class PiperTTS:
    def __init__(self, model_path: Path, base_dir: Path):
        self.model_path = model_path
        self.base_dir = base_dir

    def synthesize(self, text: str, output_dir: Path) -> Path:
        output = output_dir / f"response_{int(time.time())}.wav"
        cmd = [
            "piper",
            "--model",
            str(self.model_path),
            "--output_file",
            str(output),
        ]
        print("[…] Running Piper TTS...")
        subprocess.run(cmd, input=text, text=True, check=True, cwd=str(self.base_dir))
        print(f"[Piper] Saved audio to {output}")
        return output
