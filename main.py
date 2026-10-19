import random
import string
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select

from database import *
from models import *


@asynccontextmanager
async def lifespan(_app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="URL Shortener", lifespan=lifespan)

SessionDep = Annotated[Session, Depends(get_session)]


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/storage")
def get_storage():
    return storage


@app.get("/{code}/stats")
def show_code_stats(code: str, session: SessionDep):
    link = session.get(LinkRecord, code)
    if link is None:
        raise HTTPException(status_code=404, detail="code not found")
    return link


@app.get("/{code}")
def get_code(code: str, session: SessionDep):
    link = session.get(LinkRecord, code)
    if link is None:
        raise HTTPException(status_code=404, detail="code not found")

    link.count += 1
    session.add(link)
    session.commit()
    return RedirectResponse(url=link.url, status_code=307)


@app.post("/links", response_model=LinkResp, status_code=201)
def create_link(req: LinkReq, session: SessionDep):
    newurl = str(req.url)

    existing = session.exec(select(LinkRecord).where(LinkRecord.url == newurl)).first()

    if existing is not None:
        return existing

    while True:
        code = "".join(random.choices(string.ascii_letters + string.digits, k=6))
        if session.get(LinkRecord, code) is None:
            break

    link = LinkRecord(code=code, url=newurl)

    session.add(link)
    session.commit()
    session.refresh(link)

    return link
