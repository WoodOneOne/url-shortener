from datetime import datetime, timezone

from pydantic import HttpUrl
from sqlmodel import Field, SQLModel


class LinkReq(SQLModel):
    url: HttpUrl


class LinkRecord(SQLModel, table=True):
    code: str = Field(primary_key=True)
    url: str = Field(index=True)
    count: int = Field(default=0)
    creation_date: datetime = Field(default=datetime.now(timezone.utc))


class LinkResp(SQLModel):
    code: str
    url: str
    count: int
    creation_date: datetime