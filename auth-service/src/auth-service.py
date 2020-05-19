from fastapi import FastAPI, Response, Request, HTTPException, status
from pydantic import BaseModel
import time


class MqttClient(BaseModel):
    clientid: str
    username: str
    password: str


app = FastAPI()


@app.post("/auth", status_code=200)
async def authenticate(request: Request):
    body: bytes = await request.body()  # hangs forever
    body_text: str = bytes.decode(body)
    body_parts = body_text.split('&')

    username = body_parts[1].split('=')[1]
    password = body_parts[2].split('=')[1]

    # print("AUTH-CALL")
    # print("params: " + username +" "+ password)
    time.sleep(5)
    if (username == "user_01" and password == "passwd01") or (username == "user_02" and password == "passwd02"):
        return
    else:
        raise HTTPException(status_code=400, detail="Invalid username or password")
