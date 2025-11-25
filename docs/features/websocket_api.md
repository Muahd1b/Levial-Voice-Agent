# WebSocket API

## Overview

The Voice Agent exposes a WebSocket API to allow external clients (like the Web UI) to control the agent and receive real-time updates. This API is served by a FastAPI application.

## Server Details

- **File**: `server.py`
- **Port**: 8000 (default)
- **Endpoint**: `/ws`

## Protocol

### Client -> Server Commands

Clients send JSON messages to control the agent.

| Command                          | Description                                             |
| :------------------------------- | :------------------------------------------------------ |
| `{"command": "start_recording"}` | Triggers the agent to start listening.                  |
| `{"command": "stop_recording"}`  | Triggers the agent to stop listening and process audio. |

### Server -> Client Events

The server broadcasts JSON messages to update clients on the agent's status.

| Type                     | Data                 | Description                                    |
| :----------------------- | :------------------- | :--------------------------------------------- |
| `{"type": "listening"}`  | `None`               | Agent has started recording.                   |
| `{"type": "processing"}` | `None`               | Agent is processing audio (transcription/LLM). |
| `{"type": "transcript"}` | `{"text": "..."}`    | Intermediate or final user transcript.         |
| `{"type": "response"}`   | `{"text": "..."}`    | The text response from the LLM.                |
| `{"type": "speaking"}`   | `None`               | Agent has started audio playback.              |
| `{"type": "idle"}`       | `None`               | Agent is back to idle state.                   |
| `{"type": "error"}`      | `{"message": "..."}` | An error occurred.                             |

## Usage

To start the server:

```bash
python server.py
```
