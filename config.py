from pydantic import BaseSettings
from functools import lru_cache # read .env only once for each request

class Settings(BaseSettings):
    DB_FOLDER_NAME: str = ""
    MODEL_FOLDER_NAME: str = ""
    class Config:
        env_file = '.env'

@lru_cache()
def get_settings():
    return Settings()