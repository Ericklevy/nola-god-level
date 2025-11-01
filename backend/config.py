from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    ELASTIC_URL: str

    class Config:
        env_file = ".env" 
        env_file_encoding = "utf-8"

# Cria uma instância única que será usada em toda a aplicação
settings = Settings()