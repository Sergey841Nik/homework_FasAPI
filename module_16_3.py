from typing import Annotated

import uvicorn
from fastapi import FastAPI, HTTPException, Path, Depends


app = FastAPI()


users = {"1": "Имя: Example, возраст: 18"}


@app.get("/")
def home_page():
    return {"message": "Главная страница"}


@app.get("/user/")
def get_user() -> dict:
    return users


@app.post("/user/{username}/{age}")
def add_user(
    username: Annotated[
        str,
        Path(
            min_length=5,
            max_length=20,
            description="Enter username",
            example="UrbanUser",
        ),
    ],
    age: Annotated[int, Path(ge=18, description="Enter age", example=18)],
):
    user_id = int(max(users)) + 1
    users[str(user_id)] = f"'Имя: {username}, возраст: {age}'"
    return f"User {str(user_id)} is registered"


def valid_user_id(user_id: int):
    if not str(user_id) in users:
        raise HTTPException(status_code=404, detail="User not found")
    return str(user_id)


@app.put("/user/{user_id}/{username}/{age}")
def update_user(
    user_id: Annotated[
        str, Depends(valid_user_id)
    ],  # Выполняем проверку до запуска основной функции
    username: Annotated[
        str,
        Path(
            min_length=5,
            max_length=20,
            description="Enter username",
            example="UrbanUser",
        ),
    ],
    age: Annotated[int, Path(ge=18, description="Enter age", example=18)],
):
    users[user_id] = f"'Имя: {username}, возраст: {age}'"
    return f"The user {user_id} is updated"


@app.delete("/user/{user_id}")
def delete_user(user_id: Annotated[str, Depends(valid_user_id)]):
    user_id_del = users.pop(user_id)
    return f"User: {user_id_del} is deleted"


if __name__ == "__main__":
    uvicorn.run("module_16_3:app", reload=True)
