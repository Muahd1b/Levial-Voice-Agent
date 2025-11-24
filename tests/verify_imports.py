import sys
from pathlib import Path

# Add current directory to path so we can import levial
sys.path.append(str(Path(__file__).resolve().parent.parent))

try:
    from levial.config import ConfigManager
    from levial.orchestrator import ConversationOrchestrator
    print("[PASS] Imports successful")
except ImportError as e:
    print(f"[FAIL] Import error: {e}")
    sys.exit(1)

try:
    base_dir = Path(__file__).resolve().parent.parent
    config = ConfigManager(base_dir)
    print(f"[PASS] Config loaded. Profile: {config.profile_name}")
    print(f"       Whisper: {config.whisper_model_path}")
    print(f"       LLM: {config.llm_model_name}")
except Exception as e:
    print(f"[FAIL] Config load error: {e}")
    sys.exit(1)
