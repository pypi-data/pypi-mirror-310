from pydantic import BaseModel


class OpenApiConfig(BaseModel):
    spec: str
    api_key: str
