from typing import Union

from fastapi import FastAPI
from fastapi.logger import logger
from pydantic import BaseModel
from app.database import create_connection_pool


class Item(BaseModel):
    name: str
    description: Union[str, None] = None

app = FastAPI()

pool = create_connection_pool()


@app.get("/")
def read_root():
    logger.warn("hello")
    return {"Hello": "aaaaaaaaaaaaaaWorld"}

@app.get("/dbtest")
async def create_item():
    return {"test": 12}

@app.post("/test")
async def create_item(item: Item):
    return item

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

