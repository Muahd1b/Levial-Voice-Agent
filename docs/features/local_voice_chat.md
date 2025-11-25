# Local Voice Chat

## Overview

The core of the Local Voice Chat Agent is a privacy-preserving, low-latency voice loop that runs entirely on the local machine. It orchestrates speech-to-text, LLM processing, and text-to-speech without sending audio data to the cloud.

## Architecture

The voice loop follows this pipeline:

1.  **Microphone Capture**: Records audio using `sounddevice`.
2.  **ASR (Automatic Speech Recognition)**: Transcribes audio using `whisper.cpp` (local C++ implementation of OpenAI's Whisper).
3.  **LLM (Large Language Model)**: Generates a response using `Ollama` (running `mistral:latest` or other configured models).
4.  **TTS (Text-to-Speech)**: Synthesizes speech using `Piper` (fast, local neural TTS).
5.  **Audio Playback**: Plays the generated audio through system speakers.

## Implementation Details

- **File**: `voice_loop.py`
- **Class**: `VoiceAgent`
- **Threading**: The listening loop runs in a separate thread to allow non-blocking control.

### Key Functions

- `start_listening()`: Begins capturing audio from the microphone.
- `stop_listening()`: Stops capture and triggers processing.
- `_process_utterance(audio_path)`: Orchestrates the transcription, query, and synthesis pipeline.

## Dependencies

- `whisper.cpp`: Must be built locally.
- `ollama`: Must be running locally (`ollama serve`).
- `piper`: Binary and voice model (`en_US-lessac-medium.onnx`) must be present.
