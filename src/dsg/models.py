from pydantic import BaseModel


class ConnectionInfo(BaseModel):
    type: str
    settings: dict[str, str]


class ProjectConfig(BaseModel):
    name: str
    connection: ConnectionInfo
