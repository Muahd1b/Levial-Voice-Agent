import subprocess
from typing import List, Tuple

class OllamaLLM:
    def __init__(self, model_name: str):
        self.model_name = model_name

    def build_prompt(self, history: List[Tuple[str, str]], user_text: str) -> str:
        lines = [
            "You are Local Voice Chat Agent, a concise helpful companion. "
            "Answer conversationally in 1-3 sentences.",
        ]
        for role, content in history:
            lines.append(f"{role.upper()}: {content}")
        lines.append(f"USER: {user_text}")
        lines.append("ASSISTANT:")
        return "\n".join(lines)

    def query(self, prompt: str) -> str:
        print(f"[…] Querying Ollama ({self.model_name})...")
        result = subprocess.run(
            ["ollama", "run", self.model_name],
            input=prompt,
            text=True,
            capture_output=True,
            check=True,
        )
        reply = result.stdout.strip()
        print(f"[Ollama] {reply}")
        return reply
