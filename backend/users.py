from fastapi import APIRouter
from pydantic import BaseModel
import database
import secrets

app = APIRouter()


class User(BaseModel):
    username: str
    password: str

class Data_User(User):
    email: str

@app.post("/login/")
async def login(user: User):
    if (database.valid_user(user.username, user.password) == True):
        session_id = secrets.token_hex(32)
        database.active_session(session_id, database.get_user_id(user.username)) 
        return {"session_id": session_id}
    else:
        return {"session_id": None}

@app.get("/user/{username}/")
async def user(username: str):
    return database.search_user(username)


@app.post("/adduser/")
async def add_user(data_User: Data_User):
    if (database.add_user(data_User.username, data_User.email, data_User.password) == True):
        return {"Registro": "Valido"}
    else:
        return {"Registro": "error"}
