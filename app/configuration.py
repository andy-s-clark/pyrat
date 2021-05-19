from os import environ


class Configuration:
    def __init__(self):
        self._config = {}
        env_config_items = {
            "github_access_token": None
        }
        for name, default in env_config_items.items():
            self._config[name] = environ.get(name.upper(), default)

    def read_item(self, name: str):
        return self._config[name] if name in self._config else None
