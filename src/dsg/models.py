from pydantic import BaseModel


class ConnectionInfo(BaseModel):
    type: str
    settings: dict[str, str]


class ProjectConfig(BaseModel):
    name: str
    display_name: str
    connection: ConnectionInfo


class Page(BaseModel):
    file_stem: str  # file name without extension
    title: str
    link: str
    content: str
