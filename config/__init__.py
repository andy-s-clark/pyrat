from os import environ
from typing import Dict


class Config:
    def __init__(self, env_config_items: Dict[str, str]):
        self._config: Dict[str, str] = {}
        for name, default in env_config_items.items():
            self._config[name] = environ.get(name.upper(), default)

    def __getattr__(self, name: str) -> str:
        return self._config[name] if name in self._config else None
