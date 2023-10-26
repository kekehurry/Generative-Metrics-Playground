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
# accessiblity
# -----------------------------------------------------

def get_access_service(service_area, resident_space):
    num_res = pop_num + resident_space/ 50
    value = service_area / num_res
    return value

def get_access_LBO(amenity_space, resident_space):
    business_area = amenity_space + LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum()
    value = get_access_service(business_area, resident_space)
    max = (backend.input_data.max_floor_area + LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum())/pop_num
    min = LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum()/(pop_num + backend.input_data.max_floor_area/50)
    score = norm(value, max, min)
    return score

def cal_current_access():
    score = get_access_LBO(0, 0)
    return score

def cal_future_access():
    score = get_access_LBO(backend.input_data.amenity_space, backend.input_data.resident_space)
    return score

# def get_access_IG():
#     value = LB_data[LB_data['stakeholder'] == 'IG']['floor_area'].sum()+ backend.input_data.amenity_space
#     max = backend.input_data.max_floor_area + LB_data[LB_data['stakeholder'] == 'IG']['floor_area'].sum()
#     min = LB_data[LB_data['stakeholder'] == 'IG']['floor_area'].sum()
#     score = norm(value, max, min)
#     return score

# -----------------------------------------------------
# safety & security
# -----------------------------------------------------
def get_access_police_4(resident_space):
    police_area = 500
    value = get_access_service(police_area, resident_space)
    max = police_area / pop_num
    min = police_area / (pop_num + backend.input_data.max_floor_area / 50)
    score = norm(value, max, min)
    return score

def compute_NPI():

    access_score = get_before_after(cal_current_access()*100,  cal_future_access()*100)
    safety_security_score = get_before_after(get_access_police_4(0)*100, get_access_police_4(backend.input_data.resident_space)*100)
    # innovation_score = get_before_after(0, innovation['value'])
    # non_profit_score = get_non_profit_score() *100

    def get_non_profit_score():
        weights = [0.5, 0.5]
        scores_after = [
            access_score['after'],
            safety_security_score['after'],
            # innovation_score['after'],
        ]
        scores_before = [
            access_score['before'],
            safety_security_score['before'],
            # innovation_score['before'],
        ]
        score_before = int(sum(w * s for w, s in zip(weights, scores_before)) / sum(weights))
        score_after = int(sum(w * s for w, s in zip(weights, scores_after)) / sum(weights))
        return score_before, score_after

    def get_non_profit_radius():
        radius = get_non_profit_score()[1]
        # radius = 0
        return radius

    def get_non_profit_distance():
        distance = get_non_profit_score()[1]
        # distance = 0
        return distance
    
    # --------------------------------------------#
    # Data for bubble: score
    # --------------------------------------------#
    
    score_non_profit = {
        "stakeholder": "Nonprofit Institution",
        "score": get_non_profit_score()[1],
        "radius": get_non_profit_radius(),
        'distance': get_non_profit_distance(),
        'best': 50
        }
    # print(score_non_profit)

    # --------------------------------------------#
    # Data for chord chart: interaction
    # --------------------------------------------#
    indicator_non_profit = [
        {"stakeholder": "Nonprofit Institution", "indicator": "Access to service", "target": 'Local Business Owners', "value": cal_future_access()},
        {"stakeholder": "Nonprofit Institution", "indicator": "Safety & security", "target": 'Government', "value": get_access_police_4(backend.input_data.resident_space)},
        # {"stakeholder": "Nonprofit Institution", "indicator": "Innovation", "target": 'Industry Group', "value": get_access_IG()},
    ]
    # print(indicator_non_profit)

    # --------------------------------------------#
    # Data for indicator chart: indicator value
    # --------------------------------------------#
    index_non_profit = [
        {"stakeholder": "Nonprofit Institution","indicator": "Access to service", "baseline": access_score['before'],"score": access_score['after']},
        {"stakeholder": "Nonprofit Institution","indicator": "Safety & security", "baseline": safety_security_score['before'],"score": safety_security_score['after']},
        # {"stakeholder": "Nonprofit Institution","indicator": "Innovation", "baseline": innovation_score['before'],"score": innovation_score['after']},
    ]
    # print(index_non_profit)
    
    return score_non_profit, indicator_non_profit, index_non_profit

if __name__ == '__main__':
    compute_NPI()

