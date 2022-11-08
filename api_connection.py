from fastapi import FastAPI
from typing import List
from models import User, UserEncoder
import json
import io

app = FastAPI()

database : List[User] = []
    # User(
    #     user_id = 1,
    #     location = 1,
    #     gender = 1,
    #     attribute_1 = 1,
    #     attribute_2 = 1,
    #     attribute_3 = 1,
    #     attribute_4 = 1,
    #     preference_1 = 1,
    #     preference_2 = 1,
    #     preference_3 = 1,
    #     preference_4 = 1,
    # )

@app.get("/retrieve-user")
def retrieve_user():
    with open('data.json', 'w') as f:
        f.write(json.dumps(database, cls=UserEncoder))

    return database;

@app.post("/parse-data")
def parse_data(user : User):
    database.append(user)
    return {'User_ID Added' : user.user_id}
