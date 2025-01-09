from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()
items = {}


# 데이터 모델 정의
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    is_offer: bool = None


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


@app.post("/items/")
def create_item(item_id: int, item: Item):
    if item_id in items:
        return {"error": "Item already exists"}
    items[item_id] = item
    return {"message": "Item created successfully", "item": item}


@app.patch("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in items:
        return {"error": "Item not found"}
    update_data = item.dict(exclude_unset=True)  # unset된 값은 제외
    items[item_id].dict().update(update_data)
    return {"message": "Item updated successfully", "item": items[item_id]}


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id in items:
        del items[item_id]
        return {"message": "Item deleted successfully"}
    return {"error": "Item not found"}
