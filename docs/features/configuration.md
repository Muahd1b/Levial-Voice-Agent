# Configuration

## Overview

The Voice Agent is designed to be data-driven. Behavior, model selection, and timeouts are controlled via a JSON configuration file, allowing users to switch "profiles" without changing code.

## Configuration File

- **Location**: `config/default.json`
- **Override**: Set `LVCA_CONFIG` environment variable to a custom path.

## Key Settings

### Profiles

The `profiles` section allows defining multiple configurations (e.g., "fast", "accurate").

- `active_profile`: The key of the profile to use by default.
- `llm_model`: The Ollama model tag (e.g., `mistral:latest`).
- `whisper_model`: Path to the Whisper GGML model.
- `piper_model`: Path to the Piper ONNX voice model.

### Timeouts

- `recording_max_sec`: Maximum duration for a single utterance (auto-stop).

### Wake Word

- (Future) Settings for wake word sensitivity and model path.

## Environment Variables

- `LVCA_PROFILE`: Override the active profile (e.g., `LVCA_PROFILE=snappy`).
- `OLLAMA_MODEL`: Override the LLM model.
- `PIPER_MODEL`: Override the TTS model path.
