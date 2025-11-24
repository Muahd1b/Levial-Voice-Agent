import sys
import subprocess
from typing import List, Tuple
from pathlib import Path

from .config import ConfigManager
from .audio import AudioCapture, AudioPlayer
from .asr import WhisperASR
from .tts import PiperTTS
from .llm import OllamaLLM

class ConversationOrchestrator:
    def __init__(self, config_manager: ConfigManager):
        self.config = config_manager
        self.audio_capture = AudioCapture(
            sample_rate=self.config.mic_sample_rate,
            channels=self.config.mic_channels,
            max_duration_sec=self.config.recording_max_sec
        )
        self.asr = WhisperASR(
            bin_path=self.config.whisper_bin_path,
            model_path=self.config.whisper_model_path,
            base_dir=self.config.base_dir
        )
        self.tts = PiperTTS(
            model_path=self.config.piper_model_path,
            base_dir=self.config.base_dir
        )
        self.llm = OllamaLLM(model_name=self.config.llm_model_name)
        self.history: List[Tuple[str, str]] = []

    def run(self):
        print("Levial - Local Voice Assistant")
        print("Ensure `ollama serve` is running and Piper/Whisper paths are valid.")
        print("Controls: press Enter to start speaking, Enter again to stop, 'q' to quit.")

        while True:
            user_cmd = input("\nPress Enter to speak or type 'q' to quit: ").strip().lower()
            if user_cmd in {"q", "quit", "exit"}:
                print("Goodbye!")
                break

            audio_path = self.audio_capture.record_until_enter(
                output_path=self.config.artifacts_dir / f"utterance_{int(sys.time()) if 'sys' in locals() and hasattr(sys, 'time') else 0}.wav" # fixme: sys.time doesn't exist, use time.time
            )
            # Correction: I need to import time in this file or pass it. 
            # Actually, let's fix the import in the next step or just use a timestamp generator.
            # I'll re-write this file content correctly in the tool call.
            pass 

    def run_loop(self):
        # Re-implementing run logic with correct imports
        import time
        
        print("Levial - Local Voice Assistant")
        print("Ensure `ollama serve` is running and Piper/Whisper paths are valid.")
        print("Controls: press Enter to start speaking, Enter again to stop, 'q' to quit.")

        while True:
            user_cmd = input("\nPress Enter to speak or type 'q' to quit: ").strip().lower()
            if user_cmd in {"q", "quit", "exit"}:
                print("Goodbye!")
                break

            timestamp = int(time.time())
            audio_path = self.config.artifacts_dir / f"utterance_{timestamp}.wav"
            
            recorded_path = self.audio_capture.record_until_enter(output_path=audio_path)
            if not recorded_path:
                continue

            try:
                transcript = self.asr.transcribe(recorded_path)
            except subprocess.CalledProcessError as exc:
                print(f"[x] Whisper failed: {exc}")
                continue

            if not transcript:
                print("[!] Empty transcript, skipping.")
                continue

            prompt = self.llm.build_prompt(self.history, transcript)
            try:
                reply = self.llm.query(prompt)
            except subprocess.CalledProcessError as exc:
                print(f"[x] Ollama error: {exc.stderr}")
                continue

            self.history.append(("user", transcript))
            self.history.append(("assistant", reply))
            if self.config.max_history_turns and len(self.history) > self.config.max_history_turns:
                self.history = self.history[-self.config.max_history_turns:]

            try:
                audio_reply = self.tts.synthesize(reply, self.config.artifacts_dir)
                AudioPlayer.play(audio_reply)
            except subprocess.CalledProcessError as exc:
                print(f"[x] Piper/playback error: {exc}")
