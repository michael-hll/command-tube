# this file is used for testing purpose
# samples code not used in command-tube

# pip install fastapi
# pip install uvicorn

from fastapi import FastAPI, Path
from typing import Optional
import os

app = FastAPI()

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

@app.post("/exec-tube")
def exec_tube():
    os.system("tube -y test -f")
    return {"Data": "Successfull"}
