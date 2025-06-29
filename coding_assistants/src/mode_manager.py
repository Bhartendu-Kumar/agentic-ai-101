import json
from pathlib import Path

class ModeManager:
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.modes = self._load_modes()

    def _load_modes(self):
        """Loads modes from the JSON configuration file."""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                return {mode['slug']: mode for mode in config['modes']}
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading modes configuration: {e}")
            return {}

    def get_modes(self):
        """Returns a list of available mode names."""
        return [mode['name'] for mode in self.modes.values()]

    def get_system_prompt(self, mode_slug: str):
        """Returns the system prompt for a given mode slug."""
        return self.modes.get(mode_slug, {}).get('system_prompt')

    def get_mode_slug(self, mode_name: str):
        """Returns the slug for a given mode name."""
        for slug, mode in self.modes.items():
            if mode['name'] == mode_name:
                return slug
        return None