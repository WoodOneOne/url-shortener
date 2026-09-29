import random
import string

from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI(title="URL Shortener")

class LinkReq(BaseModel):
    url: HttpUrl

class Link(BaseModel):
    code: str
    url: str

storage: dict[str, Link] = {}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/links")
def show_links():
    return storage

@app.post("/links", response_model=Link, status_code=201)
def create_link(req: LinkReq):
    while True:
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        if code not in storage:
            break
    link = {"code": code, "url": str(req.url)}
    storage[code] = link
    return link