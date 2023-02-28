"""SETTINGS
Settings loaders using Pydantic BaseSettings classes (load from environment variables / dotenv file)
"""

# # Installed # #
import pydantic


class BaseSettings(pydantic.BaseSettings):
    class Config:
        env_file = ".env"


class APISettings(BaseSettings):
    title: str = "Compiler API"
    host: str = "localhost"
    port: int = 5000

    class Config(BaseSettings.Config):
        env_prefix = "API_"


class BlockchainSettings(BaseSettings):
    host: str = "localhost"
    port: int = 5005
    name: str = 'Khwopa Blockchain'

    class Config(BaseSettings.Config):
        env_prefix = "BLOCKCHAIN_"


class Settings():
    api_settings = APISettings()
    blockchain_settings = BlockchainSettings()


def get_configs():
    return Settings()


configs = get_configs()
