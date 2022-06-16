from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: Union[str, None] = None

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "aaaaaaaaaaaaaaWorld"}

@app.post("/test")
async def create_item(item: Item):
    return item

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

