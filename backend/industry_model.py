import sys
import os
current_directory = os.path.dirname(os.path.abspath(__file__))
project_directory = os.path.join(current_directory, '..')
sys.path.append(project_directory)

import pandas as pd
import numpy as np
import random

import backend.input_data
from backend.model_tool import *
from backend.ESE_metrics import *
# from backend.workforce_model import new_volpe_workforce
# -----------------------------------------------------

LB_data = cal_stakeholder()
work_num = get_work_num()
pop_num = get_res_num()

# -----------------------------------------------------
# accessibility
# -----------------------------------------------------

def get_access_service_2(service_area):
    num_work = work_num +  backend.input_data.office_space/ 200 +  backend.input_data.amenity_space/50 + backend.input_data.civic_space/200
    value = service_area / num_work
    return value

def get_access_business_2():
    business_area =  backend.input_data.amenity_space + LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum()
    value = get_access_service_2(business_area)
    max = ( backend.input_data.max_floor_area + LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum())/work_num
    min = LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum()/(work_num + backend.input_data.max_floor_area/200)
    score = norm(value, max, min) * 100
    return score

def current_access_business():
    business_area = LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum()
    value = business_area / work_num
    max = ( backend.input_data.max_floor_area + LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum())/work_num
    min = LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum()/(work_num + backend.input_data.max_floor_area/200)
    score = norm(value, max, min) * 100
    return score


# -----------------------------------------------------
def get_opportunity_LBO():
    LBO_area = LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum()
    value = LBO_area +  backend.input_data.amenity_space
    max =  backend.input_data.max_floor_area + LBO_area
    min = LBO_area
    score = norm(value, max, min)
    return score

def get_opportunity_IG():
    IG_area = LB_data[LB_data['stakeholder'] == 'IG']['floor_area'].sum()
    value = IG_area +  backend.input_data.office_space
    max =  backend.input_data.max_floor_area + IG_area
    min = IG_area
    score = norm(value, max, min)
    return score

# -----------------------------------------------------
def get_access_police_2():
    police_area = 500
    value = police_area / (work_num +  backend.input_data.office_space/200 +  backend.input_data.amenity_space/50 +  backend.input_data.civic_space/200)
    max = police_area / work_num
    min = police_area / (work_num +  backend.input_data.max_floor_area / 50)
    score = norm(value, max, min)
    return score

def compute_industry():

    access_to_service = {
        "target": 'Local Business Owners',
        "value": get_access_business_2()/100
    }
    safety_security = {
        "target": 'Government',
        "value": get_access_police_2() 
    }
    innovation = {
        "target": 'Nonprofit Institution',
        "value": get_access_police_2() 
    }

    access_score = get_before_after(current_access_business(),  access_to_service['value']*100 )
    safety_security_score = get_before_after(50, safety_security['value']*100)
    innovation_score = get_before_after(60, innovation['value']*100)
    # industry_score = get_industry_score() *100

    def get_industry_score(self):
        score = 0.33 * access_score['after'] + 0.33 * safety_security_score['after'] + 0.34 * innovation_score['after']
        return score
    
    def get_industry_score():
        weights = [1]
        scores_after = [
            access_score['after'],
            # safety_security_score['after'],
            # innovation_score['after'],
        ]
        scores_before = [
            access_score['before'],
            # safety_security_score['before'],
            # innovation_score['before'],
        ]
        score_before = int(sum(w * s for w, s in zip(weights, scores_before)) / sum(weights))
        score_after = int(sum(w * s for w, s in zip(weights, scores_after)) / sum(weights))
        return score_before, score_after

    def get_industry_radius():
        # radius = get_industry_score()[1]
        radius = 30
        return radius

    def get_industry_distance():
        # distance = get_industry_score()[1] - get_industry_score()[0]
        distance = 30
        return distance
    
    # --------------------------------------------#
    # Data for bubble: score
    # --------------------------------------------#
    
    score_ind = {
        "stakeholder": "Industry Group",
        "score": get_industry_score()[1],
        "radius": get_industry_radius(),
        'distance': get_industry_distance(),
        'best': 50
        }
    # print(score_ind)
    # --------------------------------------------#
    # Data for chord chart: interaction
    # --------------------------------------------#
    indicator_ind = [
        {"stakeholder": "Industry Group", "indicator": "Access to service", "target": access_to_service["target"], "value": access_to_service["value"]},
        {"stakeholder": "Industry Group", "indicator": "Safety & security", "target": safety_security["target"], "value": safety_security["value"]},
        {"stakeholder": "Industry Group", "indicator": "Innovation", "target": innovation["target"], "value": innovation["value"]}
    ]
    # print(indicator_ind)

    # --------------------------------------------#
    # Data for indicator chart: indicator value
    # --------------------------------------------#
    index_ind = [
        {"stakeholder": "Industry Group","indicator": "Access to service", "baseline": access_score['before'],"score": access_score['after']},
        {"stakeholder": "Industry Group","indicator": "Opportunity", "baseline": access_score['before'],"score": access_score['after']},
        {"stakeholder": "Industry Group","indicator": "Safety & security", "baseline": safety_security_score['before'],"score": safety_security_score['after']},
        {"stakeholder": "Industry Group","indicator": "Innovation", "baseline": innovation_score['before'],"score": innovation_score['after']}
      ]
    # print(index_ind)
    return score_ind, indicator_ind, index_ind
    
    

    

# if __name__ == '__main__':
#     compute_industry()

