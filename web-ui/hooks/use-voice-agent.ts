"use client";

import { useEffect, useRef, useState } from "react";

interface VoiceAgentState {
  status: "idle" | "wake_word_detected" | "listening" | "thinking" | "speaking" | "error";
  transcript: string;
  lastResponse: string;
  isConnected: boolean;
  wakeWord?: string;
  userProfile?: any;
  audioLevel?: number;
}

export function useVoiceAgent() {
  const [state, setState] = useState<VoiceAgentState>({
    status: "idle",
    transcript: "",
    lastResponse: "",
    isConnected: false,
    wakeWord: undefined,
    userProfile: undefined,
    audioLevel: 0,
  });

  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const connect = () => {
      const ws = new WebSocket("ws://localhost:8000/ws");

      ws.onopen = () => {
        setState((prev) => ({ ...prev, isConnected: true }));
        console.log("Connected to Levial Voice Agent");
      };

      ws.onclose = () => {
        setState((prev) => ({ ...prev, isConnected: false, status: "idle" }));
        console.log("Disconnected from Voice Agent, reconnecting in 3s...");
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
    console.log("Received message:", data);
    
    switch (data.type) {
      case "connected":
        console.log(data.message);
        break;
      case "idle":
        setState((prev) => ({ ...prev, status: "idle" }));
        break;
      case "wake_word_detected":
        setState((prev) => ({ ...prev, status: "wake_word_detected", wakeWord: data.wake_word }));
        playDing();
        break;
      case "listening":
        setState((prev) => ({ ...prev, status: "listening" }));
        break;
      case "thinking":
        setState((prev) => ({ ...prev, status: "thinking" }));
        break;
      case "speaking":
        setState((prev) => ({ ...prev, status: "speaking" }));
        break;
      case "transcript":
        setState((prev) => ({ ...prev, transcript: data.text }));
        break;
      case "response":
        setState((prev) => ({ ...prev, lastResponse: data.text }));
        break;
      case "knowledge_update":
        setState((prev) => ({ ...prev, userProfile: data.profile }));
        console.log("Knowledge updated:", data.profile);
        break;
      case "audio_level":
        setState((prev) => ({ ...prev, audioLevel: data.level }));
        break;
      case "error":
        setState((prev) => ({ ...prev, status: "error" }));
        console.error("Voice Agent Error:", data.message);
        break;
    }
  };

  const playDing = () => {
    const audio = new Audio("data:audio/wav;base64,UklGRl9vT19XQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YU"); // Short placeholder
    // Using a better base64 for a pleasant ding
    // Actually, let's use a real generated beep for now to ensure it works
    const ctx = new (window.AudioContext || (window as any).webkitAudioContext)();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    
    osc.connect(gain);
    gain.connect(ctx.destination);
    
    osc.type = "sine";
    osc.frequency.setValueAtTime(880, ctx.currentTime); // A5
    osc.frequency.exponentialRampToValueAtTime(440, ctx.currentTime + 0.1);
    
    gain.gain.setValueAtTime(0.3, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.1);
    
    osc.start();
    osc.stop(ctx.currentTime + 0.1);
  };

  const updateKnowledge = (updates: any) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({
        type: "update_knowledge",
        updates: updates
      }));
      console.log("Sent knowledge update:", updates);
    } else {
      console.error("WebSocket not connected, cannot update knowledge");
    }
  };

  return {
    ...state,
    updateKnowledge,
  };
}
