import os
from pydantic import BaseModel, Field


class Env(BaseModel):
    API_URI: str = Field(default=os.environ.get("API_URI", "https://core-local.api.chronulus.com/v1"))
    CHRONULUS_API_KEY: str | None = Field(default=os.environ.get("CHRONULUS_API_KEY", None))

