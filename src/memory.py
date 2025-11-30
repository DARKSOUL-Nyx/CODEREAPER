import json
import os
import time

class MemoryBank:
    def __init__(self, db_path="codereaper_memory.json"):
        self.db_path = db_path
        self.memory = self._load_memory()

    def _load_memory(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as f:
                return json.load(f)
        return {"preferences": [], "session_history": []}

    def save_memory(self):
        with open(self.db_path, 'w') as f:
            json.dump(self.memory, indent=2)

    def add_preference(self, rule):
        """Learns a new coding preference (e.g., 'Use Snake Case')."""
        if rule not in self.memory["preferences"]:
            self.memory["preferences"].append(rule)
            self.save_memory()

    def get_context_block(self):
        """Returns a string of learned rules to inject into the Agent's prompt."""
        if not self.memory["preferences"]:
            return ""
        rules = "\n- ".join(self.memory["preferences"])
        return f"\nCRITICAL MEMORY (Follow these learned rules):\n- {rules}\n"

    # --- Session Management (Pause/Resume) ---
    def save_checkpoint(self, stage, data):
        with open("checkpoint.json", "w") as f:
            json.dump({"timestamp": time.time(), "stage": stage, "data": data}, f)
    
    def load_checkpoint(self):
        if os.path.exists("checkpoint.json"):
            with open("checkpoint.json", "r") as f:
                return json.load(f)
        return None