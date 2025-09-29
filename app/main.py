from threading import Lock
from typing import Dict, List
import os

from fastapi import FastAPI, HTTPException, Query, Header, Depends
from pydantic import BaseModel, Field


app = FastAPI(title="Spreadsheet Broker")


class AddPayload(BaseModel):
    spreadsheet: str = Field(..., min_length=1)
    data: List[List[str]]


_store_lock = Lock()
_store: Dict[str, List[List[str]]] = {}

AUTH_KEY = os.getenv("AUTH_KEY")


def require_auth(authorization: str | None = Header(default=None)) -> None:
    if not AUTH_KEY:
        raise HTTPException(status_code=500, detail="Server not configured: AUTH_KEY missing")
    if authorization is None:
        raise HTTPException(
            status_code=401,
            detail="Missing Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = authorization.strip()
    if token.lower().startswith("bearer "):
        token = token[7:].strip()
    if token != AUTH_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.post("/add")
def add(payload: AddPayload, _: None = Depends(require_auth)) -> dict:
    """Store or replace data for a given spreadsheet key in memory."""
    with _store_lock:
        _store[payload.spreadsheet] = payload.data
    return {"status": "ok"}


@app.get("/get")
def get(
    spreadsheet: str = Query(..., min_length=1),
    pop: bool = False,
    _: None = Depends(require_auth),
) -> dict:
    """Return the data for a spreadsheet key; optionally remove it from memory."""
    with _store_lock:
        if spreadsheet not in _store:
            raise HTTPException(status_code=404, detail="Spreadsheet not found")
        if pop:
            data = _store.pop(spreadsheet)
        else:
            data = _store[spreadsheet]
    return {"data": data}


