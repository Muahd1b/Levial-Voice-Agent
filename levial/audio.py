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
        return self._record_loop(output_path, stop_event)

    def record_until_silence(self, output_path: Path, silence_threshold: float = 0.01, silence_duration: float = 2.0) -> Optional[Path]:
        """Record audio until silence is detected for a duration."""
        print("Recording... Speak now.")
        stop_event = threading.Event()
        
        # We need a custom loop or callback to detect silence
        # For simplicity, we'll use the _record_loop but with a silence check callback?
        # No, let's implement a blocking record loop here or refactor.
        # Refactoring _record_loop to take a 'should_stop' predicate is better.
        
        return self._record_loop(output_path, stop_event, silence_threshold, silence_duration)

    def _record_loop(self, output_path: Path, stop_event: threading.Event, silence_threshold: float = 0, silence_duration: float = 0) -> Optional[Path]:
        audio_queue: queue.Queue[np.ndarray] = queue.Queue()
        frames: list[np.ndarray] = []

        def callback(indata, frames_count, time_info, status):
            if status:
                print(f"[audio] {status}", file=sys.stderr)
            audio_queue.put(indata.copy())

        start_time = time.time()
        last_sound_time = time.time()
        is_speaking = False

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
                    
                    # Silence Detection Logic
                    if silence_duration > 0:
                        rms = np.sqrt(np.mean(chunk**2))
                        if rms > silence_threshold:
                            last_sound_time = time.time()
                            is_speaking = True
                        
                        if is_speaking and (time.time() - last_sound_time > silence_duration):
                            print("[i] Silence detected.")
                            stop_event.set()
                            
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
    def save_audio(self, frames: list[np.ndarray], output_path: Path) -> Optional[Path]:
        """Save raw audio frames to a WAV file."""
        if not frames:
            print("[!] No audio to save.")
            return None

        audio = np.concatenate(frames, axis=0)
        
        # Handle different data types
        if audio.dtype == np.int16:
            audio_int16 = audio
        else:
            # Assume float32/float64 (-1.0 to 1.0)
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
    def __init__(self):
        self.current_process: Optional[subprocess.Popen] = None

    def play(self, audio_path: Path) -> None:
        """Play audio using afplay (macOS) or fallback to stdout path. Non-blocking."""
        self.stop() # Stop any previous playback
        
        cmd = []
        if shutil.which("afplay"):
            cmd = ["afplay", str(audio_path)]
        elif shutil.which("ffplay"):
            cmd = ["ffplay", "-nodisp", "-autoexit", str(audio_path)]
        else:
            print(f"[i] Audio ready at {audio_path}; open it manually.")
            return

        try:
            # Use Popen to allow interruption
            self.current_process = subprocess.Popen(
                cmd, 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL
            )
            # We don't wait here, so we can interrupt. 
            # But we might want to know when it finishes? 
            # For now, the orchestrator will handle flow.
        except Exception as e:
            print(f"[x] Audio playback failed: {e}")

    def stop(self):
        """Stop current playback immediately."""
        if self.current_process:
            if self.current_process.poll() is None:
                self.current_process.terminate()
                try:
                    self.current_process.wait(timeout=0.1)
                except subprocess.TimeoutExpired:
                    self.current_process.kill()
            self.current_process = None

    def wait(self):
        """Wait for playback to finish."""
        if self.current_process:
            self.current_process.wait()
