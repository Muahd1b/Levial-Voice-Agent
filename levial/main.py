import sys
from pathlib import Path
from .config import ConfigManager
from .orchestrator import ConversationOrchestrator

def main():
    base_dir = Path(__file__).resolve().parent.parent
    try:
        config_manager = ConfigManager(base_dir)
        orchestrator = ConversationOrchestrator(config_manager)
        orchestrator.run_loop()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"[FATAL] {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
