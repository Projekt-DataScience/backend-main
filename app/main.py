import os
from typing import Union

from fastapi import FastAPI, Depends
from pydantic import BaseModel

from config import DATABASE_URL
from auth_handler import sign_jwt, JWTBearer
from models import DatabaseManager, DBUser

dbm = DatabaseManager(DATABASE_URL)
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/admin/", dependencies=[Depends(JWTBearer())])
def logged_content():
    return {"Hello": "Admin"}


class LoginData(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "admin@example.de",
                "password": "admin"
            }
        }

class LoginDataResponse(BaseModel):
    result: int
    token: Union[str, None]


@app.post("/login/")
def login_user(login_data: LoginData):
    with dbm.create_session() as session:
        # todo: add password hashing
        valid_user = session.query(DBUser).filter(
                DBUser.email == login_data.email
                and DBUser.password == login_data.password
            )
    if valid_user.count() > 0:
        jwt = sign_jwt(valid_user.first().id)
        return LoginDataResponse(result=1, token=jwt)
    else:
        return LoginDataResponse(result=0, token=None)
