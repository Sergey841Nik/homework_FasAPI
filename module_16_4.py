from typing import Annotated

import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field


app = FastAPI()

class User(BaseModel):
    id: int
    username: str
    age: int

class UserAdd(BaseModel):
    username: str = Field(min_length=3, max_length=20, description="Имя пользователя")
    age: int = Field(ge=18, description="Возраст пользователя")
    

users: list[User] = []


@app.get("/")
def home_page():
    return {"message": "Главная страница"}


@app.get("/user/", response_model=list[User])
def get_user() -> list:
    return users


@app.post("/user/", response_model=User)
def add_user(user: UserAdd) -> User:
    new_user_id = max((u.id for u in users), default=0) + 1
    nuw_user = User(id=new_user_id, username=user.username, age=user.age)
    users.append(nuw_user)
    return nuw_user


def valid_user_id(user_id: int):
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")


@app.put("/user/{user_id}/")
def update_user(
    user: Annotated[User, Depends(valid_user_id)],  # Выполняем проверку до запуска основной функции
    user_update: UserAdd,
):
    user.username = user_update.username
    user.age = user_update.age
    return user


@app.delete("/user/{user_id}")
def delete_user(user_del: Annotated[User, Depends(valid_user_id)]):
    for i, user in enumerate(users):
        if user.id == user_del.id:
            del users[i]
            break
    return f"User: {user_del} is deleted"


if __name__ == "__main__":
    uvicorn.run("module_16_4:app", reload=True)
