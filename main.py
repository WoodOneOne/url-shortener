import random
import string

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl

app = FastAPI(title="URL Shortener")

class LinkReq(BaseModel):
    url: HttpUrl

class Link(BaseModel):
    code: str
    url: str
    count: int = 0

storage: dict[str, Link] = {}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/storage")
def get_storage():
    return storage

@app.get("/{code}")
def get_code(code):
    if code in storage:
        storage[code].count += 1
        return storage[code].url
    else:
        raise HTTPException(status_code=404, detail="code not found")

@app.get("/{code}/stats")
def show_code_stats(code):
    return storage[code]

@app.post("/links", response_model=Link, status_code=201)
def create_link(req: LinkReq):
    newurl = str(req.url)

    # naive check for previous entries to prevent duplication. good enough for personal usage, but would not scale well.
    for entry in storage.values():
        if newurl == entry.url:
            return entry

    while True:
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        if code not in storage:
            break
    link = Link(code = code, url = newurl)
    storage[code] = link
    return link