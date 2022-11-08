from pydantic import BaseModel
import json
from json import JSONEncoder

class User(BaseModel):
    user_id : int
    location : int
    gender : int
    attribute_1 : int
    attribute_2 : int
    attribute_3 : int
    attribute_4 : int
    preference_1 : int
    preference_2 : int
    preference_3 : int
    preference_4 : int

class UserEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__