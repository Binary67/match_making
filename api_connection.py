from fastapi import FastAPI
from typing import List
from models import User, UserEncoder
import json
import io
from match_making import transform_json, calculate_euclidean_distance, cleaning_dict

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

    json_data = json.dumps(database, cls=UserEncoder)
    female_self_eval_dict, female_preference_dict, male_self_eval_dict, male_preference_dict, female_info_dict, male_info_dict = transform_json(json_data)
    female_ranking = calculate_euclidean_distance(female_preference_dict, male_self_eval_dict, female_info_dict, male_info_dict)
    male_ranking = calculate_euclidean_distance(male_preference_dict, female_self_eval_dict, male_info_dict, female_info_dict)
    final_dict = cleaning_dict(female_ranking, male_ranking)

    # with open('data.json', 'w') as f:
    #     f.write(json.dumps(database, cls=UserEncoder))

    return final_dict

@app.post("/parse-data")
def parse_data(user : User):
    database.append(user)
    return {'User_ID Added' : user.user_id}

@app.get("/")
def parse_data():

    return {'Hello' : 'World'}

