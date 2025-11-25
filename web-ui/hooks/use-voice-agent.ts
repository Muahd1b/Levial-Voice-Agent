"use client";

import { useEffect, useRef, useState, useCallback } from "react";

interface VoiceAgentState {
  status: "idle" | "listening" | "processing" | "speaking" | "error";
  transcript: string;
  lastResponse: string;
  isConnected: boolean;
}

export function useVoiceAgent() {
  const [state, setState] = useState<VoiceAgentState>({
    status: "idle",
    transcript: "",
    lastResponse: "",
    isConnected: false,
  });

  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const connect = () => {
      const ws = new WebSocket("ws://localhost:8000/ws");

      ws.onopen = () => {
        setState((prev) => ({ ...prev, isConnected: true }));
        console.log("Connected to Voice Agent");
      };

      ws.onclose = () => {
        setState((prev) => ({ ...prev, isConnected: false }));
        console.log("Disconnected from Voice Agent");
        // Reconnect after 3 seconds
        setTimeout(connect, 3000);
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          handleMessage(data);
        } catch (e) {
          console.error("Error parsing message:", e);
        }
      };

      wsRef.current = ws;
    };

    connect();

    return () => {
      wsRef.current?.close();
    };
  }, []);

  const handleMessage = (data: any) => {
    switch (data.type) {
      case "listening":
        setState((prev) => ({ ...prev, status: "listening" }));
        break;
      case "processing":
        setState((prev) => ({ ...prev, status: "processing" }));
        break;
      case "speaking":
        setState((prev) => ({ ...prev, status: "speaking" }));
        break;
      case "idle":
        setState((prev) => ({ ...prev, status: "idle" }));
        break;
      case "transcript":
        setState((prev) => ({ ...prev, transcript: data.text }));
        break;
      case "response":
        setState((prev) => ({ ...prev, lastResponse: data.text }));
        break;
      case "error":
        setState((prev) => ({ ...prev, status: "error" }));
        console.error("Voice Agent Error:", data.message);
        break;
    }
  };

  const startRecording = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ command: "start_recording" }));
    }
  }, []);

  const stopRecording = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ command: "stop_recording" }));
    }
  }, []);

  return {
    ...state,
    startRecording,
    stopRecording,
  };
}
