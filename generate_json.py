import json

dict_data = {
  "user_id": 0,
  "location": 0,
  "gender": 0,
  "attribute_1": 0,
  "attribute_2": 0,
  "attribute_3": 0,
  "attribute_4": 0,
  "preference_1": 0,
  "preference_2": 0,
  "preference_3": 0,
  "preference_4": 0
}

json_object = json.dumps(dict_data)

with open('sample.json', 'w') as outfiles:
    outfiles.write(json_object)