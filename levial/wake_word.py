import threading
import time
import logging
import numpy as np
import openwakeword
from openwakeword.model import Model
from typing import Callable, Optional

logger = logging.getLogger(__name__)

class WakeWordListener:
    def __init__(self, 
                 callback: Callable[[str], None], 
                 model_paths: list[str] = ["hey_jarvis"], # Using hey_jarvis as proxy for Levial for now
                 chunk_size: int = 1280,
                 inference_framework: str = "onnx"):
        
        self.callback = callback
        self.chunk_size = chunk_size
        self.running = False
        self.thread: Optional[threading.Thread] = None
        
        # Load openWakeWord model
        logger.info(f"Loading wake word models: {model_paths}")
        self.model = Model(
            wakeword_models=model_paths,
            inference_framework=inference_framework
        )
        logger.info("Wake word models loaded.")

    def start(self, audio_stream_callback: Callable[[int], np.ndarray]):
        """
        Start listening for the wake word in a background thread.
        audio_stream_callback: A function that returns the next chunk of audio (numpy array).
        """
        self.running = True
        self.thread = threading.Thread(target=self._listen_loop, args=(audio_stream_callback,), daemon=True)
        self.thread.start()
        logger.info("WakeWordListener started.")

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
        logger.info("WakeWordListener stopped.")

    def _listen_loop(self, audio_stream_callback):
        while self.running:
            # Get audio chunk
            # Note: This assumes the audio stream provider is blocking or we sleep
            # For now, we assume the callback gives us data or None
            audio_chunk = audio_stream_callback(self.chunk_size)
            
            if audio_chunk is None:
                time.sleep(0.01)
                continue
                
            # Run prediction
            prediction = self.model.predict(audio_chunk)
            
            # Check for wake word
            for mdl_name, score in prediction.items():
                if score > 0.5: # Threshold
                    logger.info(f"Wake word detected: {mdl_name} (score: {score:.2f})")
                    self.callback(mdl_name)
                    # Reset buffer/state if needed? openWakeWord handles internal buffer.
                    # We might want to pause listening briefly to avoid double triggers
                    self.model.reset()
                    time.sleep(0.5) 

from collections import deque

class SpeechDetector:
    def __init__(self, chunk_size: int = 1280, buffer_duration_sec: float = 3.0):
        from openwakeword.vad import VAD
        self.vad = VAD()
        self.chunk_size = chunk_size
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.speech_detected_event = threading.Event()
        
        # Buffer to store recent audio
        # 16000 Hz / 1280 samples = 12.5 chunks per second
        maxlen = int(12.5 * buffer_duration_sec)
        self.buffer = deque(maxlen=maxlen)

    def start(self, audio_stream_callback: Callable[[int], np.ndarray]):
        self.running = True
        self.speech_detected_event.clear()
        self.buffer.clear()
        self.thread = threading.Thread(target=self._listen_loop, args=(audio_stream_callback,), daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)

    def wait_for_speech(self, timeout: float = None) -> bool:
        return self.speech_detected_event.wait(timeout)
    
    def get_buffer(self) -> list[np.ndarray]:
        """Return the current buffer contents."""
        return list(self.buffer)

    def _listen_loop(self, audio_stream_callback):
        while self.running:
            audio_chunk = audio_stream_callback(self.chunk_size)
            if audio_chunk is None:
                time.sleep(0.01)
                continue
            
            # Add to buffer
            self.buffer.append(audio_chunk)
            
            # VAD prediction
            score = self.vad(audio_chunk)
            
            if score is not None and score > 0.5: # Threshold
                self.speech_detected_event.set()
                # We don't stop automatically, caller should stop us
                # But we can pause to avoid spamming
                time.sleep(0.1)
