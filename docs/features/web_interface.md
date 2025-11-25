# Web Interface

## Overview

The Web Interface provides a modern, visual frontend for the Voice Agent. It allows users to interact with the agent, view conversation history, and monitor the system's internal state in real-time.

## Tech Stack

- **Framework**: Next.js (React)
- **Styling**: Tailwind CSS
- **State Management**: React Hooks
- **Communication**: WebSocket (connecting to the Python backend)

## Features

### 1. Real-time Status

The UI displays the current state of the agent:

- **Idle**: Ready to listen.
- **Listening**: Currently recording audio.
- **Thinking**: Processing the input (transcribing or querying LLM).
- **Speaking**: Playing back the response.

### 2. Conversation History

A scrollable chat interface shows the conversation log, including:

- **User Transcripts**: What the agent heard.
- **Agent Responses**: What the agent replied.

### 3. Controls

- **Push-to-Talk Button**: A central button to toggle recording.
- **Visualizer**: (Planned) Audio wave visualization during speech.

## Development

The web UI is located in the `web-ui` directory.
Run locally with:

```bash
cd web-ui
npm run dev
```
