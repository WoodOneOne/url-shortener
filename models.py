from pydantic import HttpUrl
from sqlmodel import Field, SQLModel
from datetime import date

class LinkReq(SQLModel):
    url: HttpUrl

class LinkRecord(SQLModel, table=True):
    code: str = Field(primary_key=True)
    url: str = Field(index=True)
    count: int = Field(default=0)
    creation_date: date = Field(default=date.today())

class LinkResp(SQLModel):
    code: str
    url: str
    count: int
    creation_date: date