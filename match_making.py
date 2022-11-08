import pandas as pd
import numpy as np
import os
from collections import namedtuple
from collections import deque
import json

# json_file = 'sample.json'

def transform_json(json_file):
    # with open(json_file) as readfile:
    #     data = json.load(readfile)

    data = json.loads(json_file)

    male_self_eval_dict = {}
    male_preference_dict = {}
    female_self_eval_dict = {}
    female_preference_dict = {}

    # Split male and female
    for i in data:
        if i['gender'] == 1:
            female_self_eval_dict[i['user_id']] = [i['attribute_1'], i['attribute_2'], i['attribute_3'], i['attribute_4']]
            female_preference_dict[i['user_id']] = [i['preference_1'], i['preference_2'], i['preference_3'], i['preference_4']]
        elif i['gender'] == 2:
            male_self_eval_dict[i['user_id']] = [i['attribute_1'], i['attribute_2'], i['attribute_3'], i['attribute_4']]
            male_preference_dict[i['user_id']] = [i['preference_1'], i['preference_2'], i['preference_3'], i['preference_4']]

    return female_self_eval_dict, female_preference_dict, male_self_eval_dict, male_preference_dict

# female_self_eval_dict, female_preference_dict, male_self_eval_dict, male_preference_dict = transform_json(json_file)

# Determine Ranking Based On Preference
def calculate_euclidean_distance(preference_dict, self_eval_dict):
    output_dict = {}
    temp_dict = {}

    for key, value in preference_dict.items():
        for key_opposite, value_opposite in self_eval_dict.items():
            euclidean_distance = np.linalg.norm(np.array(value) - np.array(value_opposite))
            temp_dict[str(key_opposite)] = euclidean_distance

        output_dict[str(key)] = [k for k, _ in sorted(temp_dict.items(), key=lambda item: item[1])]

    return output_dict

# female_ranking = calculate_euclidean_distance(female_preference_dict, male_self_eval_dict)
# male_ranking = calculate_euclidean_distance(male_preference_dict, female_self_eval_dict)

def pref_to_rank(pref):
    return {a: {b: idx for idx, b in enumerate(a_pref)} for a, a_pref in pref.items()}

# male_set = set(male_self_eval_dict.keys())
# female_set = set(female_self_eval_dict.keys())

def GaleShapleyAlgo(male_set, female_set, male_ranking, female_ranking):
    B_rank = pref_to_rank(female_ranking)
    ask_list = {a: deque(bs) for a, bs in male_ranking.items()}
    pair = {}
    remaining_A = set(male_set)

    while len(remaining_A) > 0:
        a = remaining_A.pop()
        b = ask_list[str(a)].popleft()
        
        if b not in pair:
            pair[b] = a
        else:
            a0 = pair[b]
            b_prefer_a0 = B_rank[str(b)][str(a0)] < B_rank[str(b)][str(a)]
            if b_prefer_a0:
                remaining_A.add(a)
            else:
                remaining_A.add(a0)
                pair[b] = a

    return [(int(a), int(b)) for b, a in pair.items()]

# For cases where girls are more than boys
# if len(female_set) > len(male_set):
#     output = GaleShapleyAlgo(male_set, female_set, male_ranking, female_ranking)
# else:
#     output = GaleShapleyAlgo(female_set, male_set, female_ranking, male_ranking)
