from typing import Union

from fastapi import FastAPI
from fastapi.logger import logger
from pydantic import BaseModel

from .routers import account, divert, transfer


class Item(BaseModel):
    name: str
    description: Union[str, None] = None

app = FastAPI()

app.include_router(account.router)
app.include_router(divert.router)
app.include_router(transfer.router)



@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

