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


# -----------------------------------------------------
# finance
# -----------------------------------------------------

def get_business_res(amenity_space, resident_space):
    business_area = amenity_space + LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum()
    value = business_area/ (pop_num + resident_space/50)
    max = (backend.input_data.max_floor_area + LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum())/pop_num
    min = LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum()/(pop_num + backend.input_data.max_floor_area/50)
    score = norm(value, max, min)
    return score

def get_business_work(amenity_space, office_space,civic_space):
    business_area = amenity_space + LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum()
    value = business_area/ (work_num + office_space/200 + amenity_space/50 + civic_space/200)
    max = (backend.input_data.max_floor_area + LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum())/(work_num+amenity_space/50)
    min = LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum()/(work_num + backend.input_data.max_floor_area/200)
    score = norm(value, max, min)
    return score

def cal_current_finance():
    score = (0.5 * get_business_res(0, 0) 
             + 0.5 * get_business_work(0, 0, 0)
             )
    return score

def cal_future_finance():
    score = ( 0.5 * get_business_res(backend.input_data.amenity_space, backend.input_data.resident_space) 
             + 0.5 * get_business_work(backend.input_data.amenity_space, backend.input_data.office_space, backend.input_data.civic_space)
             )
    return score


# -----------------------------------------------------
# safety_security
# -----------------------------------------------------

def get_access_police_3(amenity_space):
    police_area = 1000
    value = police_area/ (LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum() + amenity_space)
    max = police_area / ( LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum())
    min = police_area / (LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum() + backend.input_data.max_floor_area)
    score = norm(value, max, min)
    return score

# -----------------------------------------------------

def compute_local_business_owner():

    # tax_cost = {
    #     "target": 'Government',
    #     "value": round(random.uniform(0, 1), 2)
    # }
    # build_up_area = {
    #     "target": 'Developer',
    #     "value": round(random.uniform(0, 1), 2)
    # }
    finance_score = get_before_after(cal_current_finance() *100, cal_future_finance() *100)
    safety_security_score = get_before_after(get_access_police_3(0)*100, get_access_police_3(backend.input_data.amenity_space)*100)
    
    # tax_cost_score = get_before_after(0, 1)

    def get_local_business_owner_score():
        weights = [0.5, 0.5]
        scores_after = [
            finance_score['after'],
            safety_security_score['after']
        ]
        scores_before = [
            finance_score['before'],
            safety_security_score['before']
        ]
        score_before = int(sum(w * s for w, s in zip(weights, scores_before)) / sum(weights))
        score_after = int(sum(w * s for w, s in zip(weights, scores_after)) / sum(weights))
        return score_before, score_after

    def get_local_radius():
        radius = get_local_business_owner_score()[1]
        # radius = 0
        return radius

    def get_local_distance():
        distance = get_local_business_owner_score()[1]
        # distance = 0
        return distance

    # --------------------------------------------#
    # Data for bubble: score
    # --------------------------------------------#
    
    score_local = {
        "stakeholder": "Local Business Owners",
        "score": get_local_business_owner_score()[1],
        "radius": get_local_radius(),
        'distance': get_local_distance(),
        'best': 50
        }

    # --------------------------------------------#
    # Data for chord chart: interaction
    # --------------------------------------------#
    indicator_local = [
        {"stakeholder": "Local Business Owners", "indicator": "Finance", "target": 'Residents', "value": get_business_res(backend.input_data.amenity_space, backend.input_data.resident_space)},
        {"stakeholder": "Local Business Owners", "indicator": "Finance", "target": 'Workforce', "value": get_business_work(backend.input_data.amenity_space, backend.input_data.office_space, backend.input_data.civic_space)},
        {"stakeholder": "Local Business Owners", "indicator": "Safety & security", "target": 'Government', "value": get_access_police_3(backend.input_data.amenity_space)},
        # {"stakeholder": "Local business owner", "indicator": "Tax", "target": tax_cost["target"], "value": tax_cost["value"]},
    ]

    # --------------------------------------------#
    # Data for indicator chart: indicator value
    # --------------------------------------------#
    index_local = [
        {"stakeholder": "Local Business Owners","indicator": "Finance", "baseline": finance_score['before'],"score": finance_score['after']},
        {"stakeholder": "Local Business Owners","indicator": "Safety & security", "baseline": safety_security_score['before'],"score": safety_security_score['after']},
        # {"stakeholder": "Local business owner","indicator": "Tax", "baseline": tax_cost_score['before'],"score": tax_cost_score['after']},
    ]
    
    # print(score_local)
    # print(indicator_local)
    # print(index_local)
    
    return score_local, indicator_local, index_local


if __name__ == '__main__':
    compute_local_business_owner()

