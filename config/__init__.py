from os import environ


class Config:
    def __init__(self, env_config_items):
        self._config = {}
        for name, default in env_config_items.items():
            self._config[name] = environ.get(name.upper(), default)

    def __getattr__(self, name: str):
        return self._config[name] if name in self._config else None
