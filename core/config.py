from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Definir las variables de entorno del .env
    PROJECT_NAME: str
    DATABASE_URL: str
    SECRET_KEY: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()