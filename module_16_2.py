from typing import Annotated

import uvicorn
from fastapi import FastAPI, Path


app = FastAPI()

@app.get("/")
def home_page():
    return {"message": "Главная страница"}

@app.get("/user/admin")
def admin_page():
    return {"message": "Вы вошли как админ"}

@app.get("/user/{user_id}")
def user_page(
    user_id: Annotated[int, Path(ge=1, le=100, description="Enter User ID", example=1)]
):
    return {"message": f"Вы вошли как пользователь № {user_id}"}

@app.get("/user/{username}/{age}")
def user_info(
    username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username", example="UrbanUser")],
    age: Annotated[int, Path(ge=18, le=120, description="Enter age", example='24')],
):
    return {"message": f"Информация о пользователе. Имя: {username}, Возраст: {age}"}


if __name__ == "__main__":
    uvicorn.run(
        "module_16_2:app", reload=True
    )