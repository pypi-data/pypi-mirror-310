import pickle
from pathlib import Path

class AgentCache:
    """Simple pickle-based cache implementation"""
    @staticmethod
    def load(cache_path: Path) -> dict:
        with open(cache_path, 'rb') as f:
            return pickle.load(f)
    
    @staticmethod
    def save(cache_path: Path, data: dict):
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        with open(cache_path, 'wb') as f:
            pickle.dump(data, f)