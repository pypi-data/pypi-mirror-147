from enum import Enum

class ConfigType(Enum):
    ENV = "env"
    DOTENV = "dotenv"
    TOML = "toml"
    JSON = "json"
    PYTHON = "python"

config_key_map = {
    "client_id": "id"
}