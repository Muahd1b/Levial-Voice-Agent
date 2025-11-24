import os
import subprocess
from pathlib import Path

class WhisperASR:
    def __init__(self, bin_path: Path, model_path: Path, base_dir: Path):
        self.bin_path = bin_path
        self.model_path = model_path
        self.base_dir = base_dir
        self.dyld_parts = [
            base_dir / "whisper.cpp" / "build" / "src",
            base_dir / "whisper.cpp" / "build" / "ggml" / "src",
            base_dir / "whisper.cpp" / "build" / "ggml" / "src" / "ggml-blas",
            base_dir / "whisper.cpp" / "build" / "ggml" / "src" / "ggml-metal",
        ]

    def transcribe(self, audio_path: Path) -> str:
        """Invoke Whisper CLI and return the transcript string."""
        env = os.environ.copy()
        dyld_paths = [str(p) for p in self.dyld_parts if p.exists()]
        existing = env.get("DYLD_LIBRARY_PATH")
        if existing:
            dyld_paths.append(existing)
        env["DYLD_LIBRARY_PATH"] = ":".join(dyld_paths)

        cmd = [
            str(self.bin_path),
            "-m",
            str(self.model_path),
            "-f",
            str(audio_path),
            "-otxt",
        ]

        print("[…] Running Whisper transcription...")
        subprocess.run(cmd, check=True, cwd=str(self.base_dir), env=env)
        txt_path = Path(f"{audio_path}.txt")  # whisper-cli appends ".txt" to original filename
        transcript = txt_path.read_text(encoding="utf-8").strip()
        print(f"[Whisper] {transcript}")
        return transcript
