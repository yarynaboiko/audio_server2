from fastapi import FastAPI, HTTPException

app = FastAPI()

users = []

@app.post("/user/add")
def add_user(login: str, name: str, surname: str, age: int):
    for user in users:
        if user['login'] == login:
            return HTTPException(status_code=400, detail="Такий користувач вже існує")
    new_user = {"login":login, "name":name, "surname":surname, "age":age}
    users.append(new_user)
    return new_user