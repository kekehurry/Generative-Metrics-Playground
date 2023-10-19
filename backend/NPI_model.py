import sys
import os
current_directory = os.path.dirname(os.path.abspath(__file__))
project_directory = os.path.join(current_directory, '..')
sys.path.append(project_directory)
from backend.model_tool import *
from backend.ESE_metrics import *
import pandas as pd
import numpy as np
import random
import backend.input_data
# -----------------------------------------------------

LB_data = cal_stakeholder()
work_num = get_work_num()
pop_num = get_res_num()

#-----------------------------------------------------
# kendall sq program
#-----------------------------------------------------

mit_commuter_home_all = 8132 #person

mit_pop_profile = [   # = housing demand
    0.65, # single -> single occupancy
    0.15, # partners -> dual occupancy
    0.1, # partners+1 child ->triple occupancy
    0.05, # partners+2 children -> quad occupancy
    0.05, # partners+3 children -> family occupancy
]

mit_commuters = [
    int(mit_commuter_home_all * mit_pop_profile[0]),
    int(mit_commuter_home_all * mit_pop_profile[1] * 2),
    int(mit_commuter_home_all * mit_pop_profile[2] * 3),
    int(mit_commuter_home_all * mit_pop_profile[3] * 4),
    int(mit_commuter_home_all * mit_pop_profile[4] * 5)
]
mit_commuters_all = sum(mit_commuters)
# print('MIT commuters:', mit_commuters, mit_commuters_all)




# -----------------------------------------------------

def get_access_service(service_area):
    num_res = pop_num + backend.input_data.resident_space/ 50
    value = service_area / num_res
    return value

def get_access_LBO():
    business_area = backend.input_data.amenity_space + LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum()
    value = get_access_service(business_area)
    max = (backend.input_data.max_floor_area + LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum())/pop_num
    min = LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum()/(pop_num + backend.input_data.max_floor_area/50)
    score = norm(value, max, min)
    return score

# -----------------------------------------------------
def get_access_IG():
    value = LB_data[LB_data['stakeholder'] == 'IG']['floor_area'].sum()+ backend.input_data.amenity_space
    max = backend.input_data.max_floor_area + LB_data[LB_data['stakeholder'] == 'IG']['floor_area'].sum()
    min = LB_data[LB_data['stakeholder'] == 'IG']['floor_area'].sum()
    score = norm(value, max, min)
    return score

# -----------------------------------------------------
def get_access_police_4():
    police_area = 500
    value = get_access_service(police_area)
    max = police_area / pop_num
    min = police_area / (pop_num + backend.input_data.max_floor_area / 50)
    score = norm(value, max, min)
    return score

def compute_NPI():

    access_to_service = {
        "target": 'Local Business Owners',
        "value": get_access_LBO()
    }
    safety_security = {
        "target": 'Government',
        "value": get_access_police_4()
    }
    innovation = {
        "target": 'Industry Group',
        "value": get_access_IG()
    }

    access_score = get_before_after(0.55,  access_to_service['value'] )
    safety_security_score = get_before_after(1, safety_security['value'])
    innovation_score = get_before_after(0, innovation['value'])
    # non_profit_score = get_non_profit_score() *100

    def get_non_profit_score():
        weights = [1]
        scores_after = [
            access_score['after'],
            # safety_security_score['after'],
            # innovation_score['after'],
            # safety_security_score['after']
        ]
        scores_before = [
            access_score['before'],
            # safety_security_score['before'],
            # innovation_score['before'],
            # safety_security_score['before']
        ]
        score_before = int(sum(w * s for w, s in zip(weights, scores_before)) / sum(weights))
        score_after = int(sum(w * s for w, s in zip(weights, scores_after)) / sum(weights))
        return score_before, score_after

    def get_non_profit_radius():
        # radius = get_non_profit_score()[1]
        radius = 0
        return radius

    def get_non_profit_distance():
        # distance = get_non_profit_score()[1] - get_non_profit_score()[0]
        distance = 0
        return distance
    
    # --------------------------------------------#
    # Data for bubble: score
    # --------------------------------------------#
    
    score_non_profit = {
        "stakeholder": "Nonprofit Institution",
        "score": get_non_profit_score()[1],
        "radius": get_non_profit_radius(),
        'distance': get_non_profit_distance() * 2
        }

    # --------------------------------------------#
    # Data for chord chart: interaction
    # --------------------------------------------#
    indicator_non_profit = [
        {"stakeholder": "Nonprofit Institution", "indicator": "Access to service", "target": access_to_service["target"], "value": access_to_service["value"]},
        {"stakeholder": "Nonprofit Institution", "indicator": "Safety & security", "target": safety_security["target"], "value": safety_security["value"]},
        {"stakeholder": "Nonprofit Institution", "indicator": "Innovation", "target": innovation["target"], "value": innovation["value"]},
    ]

    # --------------------------------------------#
    # Data for indicator chart: indicator value
    # --------------------------------------------#
    index_non_profit = [
        {"stakeholder": "Nonprofit Institution","indicator": "Access to service", "baseline": access_score['before'],"score": access_score['after']},
        {"stakeholder": "Nonprofit Institution","indicator": "Safety & security", "baseline": safety_security_score['before'],"score": safety_security_score['after']},
        {"stakeholder": "Nonprofit Institution","indicator": "Innovation", "baseline": innovation_score['before'],"score": innovation_score['after']},
    ]
    
    return score_non_profit, indicator_non_profit, index_non_profit

# if __name__ == '__main__':
#     get_access_LBO()

