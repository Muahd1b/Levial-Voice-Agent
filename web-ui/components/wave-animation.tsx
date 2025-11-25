"use client";

import { motion } from "framer-motion";
import { Mic } from "lucide-react";

interface WaveAnimationProps {
  status: "idle" | "listening" | "processing" | "speaking" | "error";
  onClick?: () => void;
}

export function WaveAnimation({ status, onClick }: WaveAnimationProps) {
  const waveVariants = {
    idle: {
      scale: [1, 1.05, 1],
      opacity: [0.3, 0.5, 0.3],
    },
    listening: {
      scale: [1, 1.2, 1],
      opacity: [0.5, 0.8, 0.5],
    },
    processing: {
      scale: [1, 0.9, 1],
      opacity: [0.5, 0.8, 0.5],
      rotate: [0, 180, 360],
    },
    speaking: {
      scale: [1, 1.3, 1, 1.1, 1],
      opacity: [0.6, 1, 0.6, 0.8, 0.6],
    },
    error: {
      scale: 1,
      opacity: 0.5,
      backgroundColor: "#ef4444",
    },
  };

  const getAnimationState = () => {
    return status;
  };

  return (
    <div className="relative flex items-center justify-center h-64 w-64 cursor-pointer" onClick={onClick}>
      {/* Outer waves */}
      {[0, 1, 2].map((index) => (
        <motion.div
          key={index}
          className={`absolute rounded-full ${status === "error" ? "bg-red-500" : "bg-primary"}`}
          initial={{ scale: 0.8, opacity: 0 }}
          animate={waveVariants[getAnimationState()]}
          transition={{
            duration: status === "processing" ? 1 : 2,
            repeat: Infinity,
            delay: index * 0.3,
            ease: "easeInOut",
          }}
          style={{
            width: `${200 - index * 30}px`,
            height: `${200 - index * 30}px`,
          }}
        />
      ))}

      {/* Center icon */}
      <motion.div
        className={`absolute z-10 rounded-full p-8 shadow-lg ${status === "error" ? "bg-red-500" : "bg-primary"}`}
        animate={{
          scale: status === "speaking" ? [1, 1.1, 1] : status === "listening" ? 1.05 : 1,
        }}
        transition={{
          duration: 0.5,
          repeat: status === "speaking" ? Infinity : 0,
        }}
      >
        <Mic className="h-12 w-12 text-primary-foreground" />
      </motion.div>

      {/* Status text */}
      <div className="absolute -bottom-8 text-center w-full">
        <motion.p
          className="text-sm font-medium text-muted-foreground capitalize"
          animate={{ opacity: [0.7, 1, 0.7] }}
          transition={{ duration: 2, repeat: Infinity }}
        >
          {status === "idle" ? "Click to Speak" : status}
        </motion.p>
      </div>
    </div>
  );
}
