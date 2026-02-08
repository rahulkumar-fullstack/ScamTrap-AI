from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_key: str
    minilm_model: str

    class Config:
        env_file = ".env"

settings = Settings()
