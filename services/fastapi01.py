# this file is used for testing purpose
# samples code not used in command-tube

# pip install fastapi
# pip install uvicorn

from fastapi import FastAPI, Path, Query, HTTPException
from typing import Optional
import os
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None

class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None

inventory = {}    

# Add it to the uvicorn server
# >>> uvicorn fastapi01:app --reload

@app.get('/')
def home():
    return {"Data": "Hello World"}

@app.get('/get-item/{item_id}')
def get_itm(item_id: int = Path(None, description="The ID of the item.")):
    result = item_id + item_id
    return {"Data": result}

@app.get('/get-item-by-name')
def get_itm(name: Optional[str] = None):
    if name:
        return {"Data": name}
    return {"Data": "None"}

# http://127.0.0.1:8000/get-item-by-name/1?name=mac&test=2
@app.get('/get-item-by-name/{item_id}')
def get_itm(*, item_id: int, name: Optional[str] = None, test: int):
    if item_id:
        # raise HTTPException(status_code=404, detail="Item name not found.")
        return {"Data": str(item_id) + name + str(test)}
    return {"Data": "None"}

@app.post("/exec-tube")
def exec_tube():
    os.system("tube -y test -f")
    return {"Data": "Successfull"}

@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        
        return {"Error": "Item ID already exists."}
    
    inventory[item_id] = {"name": item.name, "brand": item.brand, "price": item.price}
    return inventory[item_id]

@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        return {"Error": "Item ID does not exists."}
    
    print(inventory[item_id])
    
    if item.name != None:
        inventory[item_id]["name"] = item.name
    
    if item.price != None:
        inventory[item_id]["price"] = item.price
        
    if item.brand != None:
        inventory[item_id]["brand"] = item.brand
        
    return inventory[item_id]

@app.delete("/delete-item")
def delete_item(item_id: int = Query(..., describe="The ID of the item to delete.")):
    if item_id not in inventory:
        return {"Error": "The ID does not exists."}
    
    del inventory[item_id]
    return {"Success": "Item delted!"}