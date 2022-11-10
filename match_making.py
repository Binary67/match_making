import pandas as pd
import numpy as np
import os
from collections import namedtuple
from collections import deque
import json
import random

def transform_json(json_file):
    # # To comment out during deployment
    # with open(json_file) as readfile:
    #     data = json.load(readfile)

    # To uncomment during deployment
    data = json.loads(json_file)

    male_self_eval_dict = {}
    male_preference_dict = {}
    female_self_eval_dict = {}
    female_preference_dict = {}
    male_info_dict = {}
    female_info_dict = {}

    # Split male and female
    for i in data:
        if i['gender'] == 1:
            female_info_dict[i['user_id']] = [i['location'], i['age']]
            female_self_eval_dict[i['user_id']] = [i['attribute_1'], i['attribute_2'], i['attribute_3'], i['attribute_4']]
            female_preference_dict[i['user_id']] = [i['preference_1'], i['preference_2'], i['preference_3'], i['preference_4']]
        elif i['gender'] == 2:
            male_info_dict[i['user_id']] = [i['location'], i['age']]
            male_self_eval_dict[i['user_id']] = [i['attribute_1'], i['attribute_2'], i['attribute_3'], i['attribute_4']]
            male_preference_dict[i['user_id']] = [i['preference_1'], i['preference_2'], i['preference_3'], i['preference_4']]

    return female_self_eval_dict, female_preference_dict, male_self_eval_dict, male_preference_dict, female_info_dict, male_info_dict

# Determine Ranking Based On Preference
def calculate_euclidean_distance(preference_dict, self_eval_dict, target_info_dict, opposite_info_dict):
    output_dict = {}

    for key, value in preference_dict.items():
        temp_dict = {}
        dict_keys =  list(self_eval_dict.keys())
        random.shuffle(dict_keys)
        shuffled_dict = dict((x, y) for x, y in ((key, self_eval_dict[key]) for key in dict_keys))
        for key_opposite, value_opposite in shuffled_dict.items():
            if target_info_dict[key][0] == opposite_info_dict[key_opposite][0] and abs(target_info_dict[key][1] - opposite_info_dict[key_opposite][1]) <= 5:
                euclidean_distance = np.linalg.norm(np.array(value) - np.array(value_opposite))
                temp_dict[str(key_opposite)] = euclidean_distance

        output_dict[str(key)] = [k for k, _ in sorted(temp_dict.items(), key=lambda item: item[1])]

        if len(output_dict[str(key)]) < 3:
            for key_opposite, value_opposite in shuffled_dict.items():
                if abs(target_info_dict[key][1] - opposite_info_dict[key_opposite][1]) <= 5:
                    euclidean_distance = np.linalg.norm(np.array(value) - np.array(value_opposite))
                    temp_dict[str(key_opposite)] = euclidean_distance

        output_dict[str(key)] = [k for k, _ in sorted(temp_dict.items(), key=lambda item: item[1])]


    return output_dict

def cleaning_dict(female_ranking, male_ranking):
    temp_dict = female_ranking.copy()
    temp_dict.update(male_ranking)

    final_dict = {}

    for key, value in temp_dict.items():
        final_dict[key] = value[:3]

    return final_dict
