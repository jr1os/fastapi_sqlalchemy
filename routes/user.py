from fastapi import APIRouter, Response, status
from config.db import conn
from models.user import users
from typing import List
from schemas.user import User
from cryptography.fernet import Fernet
from starlette.status import HTTP_204_NO_CONTENT

key = Fernet.generate_key()
k = Fernet(key)
user = APIRouter()


@user.get(
    "/users",
    tags=["users"],
    response_model=List[User],
    description="Get a list of all users",
)
def get_users():
    return conn.execute(users.select()).fetchall()


@user.post("/users", tags=["users"], response_model=User)
def create_user(user: User):
    new_user = {"name": user.name, "email": user.email}
    new_user["password"] = k.encrypt(user.password.encode("utf-8"))
    result = conn.execute(users.insert().values(new_user))
    return conn.execute(users.select().where(users.c.id == result.lastrowid)).first()


@user.get("/users/{id}", tags=["users"], response_model=User)
def get_user(id: str):
    return conn.execute(users.select().where(users.c.id == id)).first()


@user.delete("/users/{id}", tags=["users"], status_code=HTTP_204_NO_CONTENT)
def delete_user(id: str):
    conn.execute(users.delete().where(users.c.id == id))
    return Response(status_code=HTTP_204_NO_CONTENT)


@user.put("/users/{id}", tags=["users"], response_model=User)
def update_user(id: str, user: User):
    conn.execute(
        users.update()
        .values(
            name=user.name,
            email=user.email,
            password=k.encrypt(user.password.encode("utf-8")),
        )
        .where(users.c.id == id)
    )
    return conn.execute(users.select().where(users.c.id == id)).first()
