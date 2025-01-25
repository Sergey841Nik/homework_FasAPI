from typing import Annotated

import uvicorn
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


app = FastAPI()

templates = Jinja2Templates(directory='templates')

class User(BaseModel):
    id: int
    username: str
    age: int


users: list[User] = []


@app.get("/")
def home_page(request: Request):
    return templates.TemplateResponse(
            "users.html",
            {"request": request, "users": users}
        )

@app.get("/user/{user_id}", response_model=list[User])
def get_user(request: Request, user_id: int):
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse(
            "users.html",
            {"request": request, "user": user}
        )


@app.post("/user/{username}/{age}/", response_model=User)
def add_user(username: str, age: int) -> User:
    new_user_id = max((u.id for u in users), default=0) + 1
    nuw_user = User(id=new_user_id, username=username, age=age)
    users.append(nuw_user)
    return nuw_user


def valid_user_id(user_id: int) -> User:
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")


@app.put("/user/{user_id}/{username}/{age}/", response_model=User)
def update_user(
    user: Annotated[User, Depends(valid_user_id)],  # Выполняем проверку до запуска основной функции
    username: str,
    age: int,
) -> User:
    user.username = username
    user.age = age
    return user


@app.delete("/user/{user_id}/")
def delete_user(user_del: Annotated[User, Depends(valid_user_id)]) -> User:
    for i, user in enumerate(users):
        if user.id == user_del.id:
            del users[i]
            break
    return user_del


if __name__ == "__main__":
    uvicorn.run("module_16_5:app", reload=True)
