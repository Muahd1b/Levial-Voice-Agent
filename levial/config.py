import json
import os
import sys
from pathlib import Path
from typing import Any, Dict

class ConfigManager:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.config = self._load_config()
        self.profile_name = os.environ.get("LVCA_PROFILE", self.config.get("active_profile"))
        self.profile = self._load_profile()
        self.artifacts_dir = (self.base_dir / self.config.get("artifacts_dir", "artifacts")).resolve()
        self.artifacts_dir.mkdir(exist_ok=True)

    def _load_config(self) -> Dict[str, Any]:
        config_path = Path(os.environ.get("LVCA_CONFIG", self.base_dir / "config" / "default.json"))
        if not config_path.exists():
            print(f"[x] Config file not found: {config_path}. Create one or set LVCA_CONFIG.", file=sys.stderr)
            sys.exit(1)
        with config_path.open() as fh:
            return json.load(fh)

    def _load_profile(self) -> Dict[str, Any]:
        profiles = self.config.get("profiles", {})
        if self.profile_name not in profiles:
            print(f"[x] Profile '{self.profile_name}' missing in config.", file=sys.stderr)
            sys.exit(1)
        profile = profiles[self.profile_name]
        print(f"[config] Loaded profile '{self.profile_name}': {profile.get('description', '')}")
        return profile

    @property
    def whisper_model_path(self) -> Path:
        return self.base_dir / self.profile.get("whisper_model", "whisper.cpp/models/ggml-small.bin")

    @property
    def whisper_bin_path(self) -> Path:
        return self.base_dir / "whisper.cpp" / "build" / "bin" / "whisper-cli"

    @property
    def piper_model_path(self) -> Path:
        return Path(os.environ.get("PIPER_MODEL", self.base_dir / self.profile.get("piper_model", "en_US-lessac-medium.onnx")))

    @property
    def llm_model_name(self) -> str:
        return os.environ.get("OLLAMA_MODEL", self.profile.get("llm_model", "mistral:latest"))

    @property
    def mic_sample_rate(self) -> int:
        return self.profile.get("mic_sample_rate", 16_000)

    @property
    def mic_channels(self) -> int:
        return self.profile.get("mic_channels", 1)

    @property
    def max_history_turns(self) -> int:
        return self.profile.get("max_history_turns", 6)
    
    @property
    def recording_max_sec(self) -> float | None:
        return self.config.get("timeouts", {}).get("recording_max_sec")
