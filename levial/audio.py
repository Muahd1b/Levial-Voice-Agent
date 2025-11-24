import queue
import sys
import threading
import time
import wave
import shutil
import subprocess
from pathlib import Path
from typing import Optional

import numpy as np
import sounddevice as sd

class AudioCapture:
    def __init__(self, sample_rate: int, channels: int, max_duration_sec: Optional[float] = None):
        self.sample_rate = sample_rate
        self.channels = channels
        self.max_duration_sec = max_duration_sec

    def record_until_enter(self, output_path: Path) -> Optional[Path]:
        """Record audio until the user presses Enter. Returns path to the wav file."""
        print("Recording... Press Enter to stop.")
        stop_event = threading.Event()

        def wait_for_stop() -> None:
            input()
            stop_event.set()

        threading.Thread(target=wait_for_stop, daemon=True).start()

        audio_queue: queue.Queue[np.ndarray] = queue.Queue()
        frames: list[np.ndarray] = []

        def callback(indata, frames_count, time_info, status):
            if status:
                print(f"[audio] {status}", file=sys.stderr)
            audio_queue.put(indata.copy())

        start_time = time.time()

        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="float32",
            callback=callback,
        ):
            while not stop_event.is_set():
                try:
                    chunk = audio_queue.get(timeout=0.1)
                    frames.append(chunk)
                except queue.Empty:
                    continue
                if self.max_duration_sec and (time.time() - start_time) >= self.max_duration_sec:
                    print(f"[i] Recording limit reached ({self.max_duration_sec}s).")
                    stop_event.set()

        if not frames:
            print("[!] No audio captured.")
            return None

        audio = np.concatenate(frames, axis=0)
        audio = np.clip(audio, -1.0, 1.0)
        audio_int16 = (audio * 32767).astype(np.int16)

        with wave.open(str(output_path), "wb") as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(2)
            wf.setframerate(self.sample_rate)
            wf.writeframes(audio_int16.tobytes())

        print(f"[✓] Saved recording to {output_path}")
        return output_path

class AudioPlayer:
    @staticmethod
    def play(audio_path: Path) -> None:
        """Play audio using afplay (macOS) or fallback to stdout path."""
        if shutil.which("afplay"):
            subprocess.run(["afplay", str(audio_path)], check=True)
        elif shutil.which("ffplay"):
            subprocess.run(["ffplay", "-nodisp", "-autoexit", str(audio_path)], check=True)
        else:
            print(f"[i] Audio ready at {audio_path}; open it manually.")
