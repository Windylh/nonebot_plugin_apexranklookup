from pydantic import BaseSettings


class Config(BaseSettings):
    apex_api_token = "api_token"

    class Config:
        extra = "ignore"