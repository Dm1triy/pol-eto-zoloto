from pydantic import BaseSettings


class Settings(BaseSettings):
    kafka_bootstrap_servers: str
    kafka_video_topic: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
