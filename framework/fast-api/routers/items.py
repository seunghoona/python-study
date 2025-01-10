from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()
items = {}


# 데이터 모델 정의
class Item(BaseModel):
    name: str = "myname"
    description: str = None
    price: float
    is_offer: bool = None


@router.post("/items/")
def create_item(item_id: int, item: Item):
    if item_id in items:
        raise HTTPException(status_code=400, detail="Item already exists")
    items[item_id] = item
    return {"message": "Item created successfully", "item": item}


@router.patch("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    update_data = item.dict(exclude_unset=True)
    items[item_id].dict().update(update_data)
    return {"message": "Item updated successfully", "item": items[item_id]}


@router.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id in items:
        del items[item_id]
        return {"message": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")
