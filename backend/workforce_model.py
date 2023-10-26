import sys
import os
current_directory = os.path.dirname(os.path.abspath(__file__))
project_directory = os.path.join(current_directory, '..')
sys.path.append(project_directory)
import backend.input_data
from backend.model_tool import *
from backend.ESE_metrics import *
# from backend.developer_model import volpe_office
import pandas as pd
import numpy as np
import random

# -----------------------------------------------------

LB_data = cal_stakeholder()
work_num = get_work_num()
pop_num = get_res_num()

#-----------------------------------------------------
# kendall sq program
#-----------------------------------------------------

# this is an initial setting of office area
# volpe_office_all = 1700000 #sqft all
volpe_office_all = backend.input_data.office_space * 10.7639 #sqft all

volpe_office_profile = [
    0.5, # Office (250sqft/person)
    0.3, # Lab (1000sqft/person)
    0.2 #   Research Space (400 sqft/person)
]

volpe_office = [int(volpe_office_all * p) for p in volpe_office_profile]
# print(volpe_office)

## new workforce number comes from the new volpe program office area
volpe_workforce_home = [
    int(volpe_office[0] / 250), # for office
    int(volpe_office[1] / 1000), # for lab
    int(volpe_office[2] / 400) # for research
    ]
volpe_workforce_home_all = sum(volpe_workforce_home)
# print ("Volpe workforce num:", volpe_workforce, volpe_workforce_all)

work_pop_profile = [   # = housing demand
    0.65, # single -> single occupancy
    0.15, # partners -> dual occupancy
    0.1, # partners+1 child ->triple occupancy
    0.05, # partners+2 children -> quad occupancy
    0.05, # partners+3 children -> family occupancy
]

## new living pop from: volpe workforce + family members, in different housing types
volpe_workforce_family = [
    int(volpe_workforce_home_all * work_pop_profile[0]),
    int(volpe_workforce_home_all * work_pop_profile[1] * 2),
    int(volpe_workforce_home_all * work_pop_profile[2] * 3),
    int(volpe_workforce_home_all * work_pop_profile[3] * 4),
    int(volpe_workforce_home_all * work_pop_profile[4] * 5)
]
volpe_workforce_family_all = sum(volpe_workforce_family)
# print('Volpe workforce family:', volpe_workforce_family, volpe_workforce_family_all)

def new_volpe_workforce(office_space, civic_space, amenity_space):
    # this is an initial setting of office area
    # volpe_office_all = 1700000 #sqft all
    volpe_office_all = office_space * 10.7639 #sqft all

    volpe_office = [int(volpe_office_all * p) for p in volpe_office_profile]
    # print(volpe_office)

    ## new workforce number comes from the new volpe program office area
    volpe_workforce_home = [
        int(volpe_office[0] / 250), # for office
        int(volpe_office[1] / 1000), # for lab
        int(volpe_office[2] / 400) # for research
        ]
    volpe_workforce_home_all = sum(volpe_workforce_home)
    # print ("Volpe workforce num:", volpe_workforce, volpe_workforce_all)
    
    new_from_office = volpe_workforce_home_all
    new_from_civic = civic_space / 200
    new_from_amenity = amenity_space / 50
    num = new_from_office + new_from_civic + new_from_amenity
    return num


# -----------------------------------------------------
# accessibility
# -----------------------------------------------------

def get_access_service_2(service_area, office_space, amenity_space, civic_space):
    num_work = work_num + office_space/ 200 +  amenity_space/50 +  civic_space/200
    value = service_area / num_work
    return value

def get_access_business_2(amenity_space, office_space, civic_space):
    business_area =  amenity_space + LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum()
    value = get_access_service_2(business_area,office_space, amenity_space, civic_space)
    max = ( backend.input_data.max_floor_area + LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum())/work_num
    min = LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum()/(work_num +  backend.input_data.max_floor_area/200)
    score = norm(value, max, min)
    return score

def cal_current_access_business():
    score = get_access_business_2(0, 0, 0)
    return score

def cal_future_access_business():
    score = get_access_business_2( backend.input_data.amenity_space,  backend.input_data.office_space,  backend.input_data.civic_space)
    return score

# -----------------------------------------------------
# opportunity
# -----------------------------------------------------
def get_opportunity_LBO(amenity_space):
    LBO_area = LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum()
    value = LBO_area + amenity_space
    max =  backend.input_data.max_floor_area + LBO_area
    min = LBO_area
    score = norm(value, max, min)
    return score

# def get_opportunity_IG(office_space):
#     IG_area = LB_data[LB_data['stakeholder'] == 'IG']['floor_area'].sum()
#     value = IG_area + office_space
#     max =  backend.input_data.max_floor_area + IG_area
#     min = IG_area
#     score = norm(value, max, min)
#     return score

def cal_current_opportunity():
    score = (0.5 * get_opportunity_LBO(0) 
            #  + 0.5 * get_opportunity_IG(0)
             )
    return score

def cal_future_opportunity():
    score = ( get_opportunity_LBO( backend.input_data.amenity_space) 
            #  + 0.5 * get_opportunity_IG( backend.input_data.office_space)
             )
    return score

# -----------------------------------------------------
# safety & security
# -----------------------------------------------------
def get_access_police_2(office_space, amenity_space, civic_space):
    police_area = 1000
    value = police_area / (work_num +  new_volpe_workforce(office_space,civic_space, amenity_space))
    max = police_area / work_num
    min = police_area / (work_num +  backend.input_data.max_floor_area / 50)
    score = norm(value, max, min)
    return score

# -----------------------------------------------------

def compute_workforce():

    access_score = get_before_after(cal_current_access_business()*100, cal_future_access_business()*100)
    opportunity_score = get_before_after(cal_current_opportunity()*100, cal_future_opportunity()*100)
    safety_security_score = get_before_after(get_access_business_2(0,0,0)*100, get_access_police_2( backend.input_data.office_space,  backend.input_data.amenity_space,  backend.input_data.civic_space)*100)

    
    def get_workforce_score():
        weights = [0.4, 0.3, 0.3]
        scores_after = [
            access_score['after'],
            opportunity_score['after'],
            safety_security_score['after']
        ]
        scores_before = [
            access_score['before'],
            opportunity_score['before'],
            safety_security_score['before']
        ]
        score_before = int(sum(w * s for w, s in zip(weights, scores_before)) / sum(weights))
        score_after = int(sum(w * s for w, s in zip(weights, scores_after)) / sum(weights))
        return score_before, score_after

    def get_workforce_radius():
        radius = get_workforce_score()[1]
        # radius = 0
        return radius

    def get_workforce_distance():
        distance = get_workforce_score()[1]
        # distance = 0
        return distance
    
    # --------------------------------------------#
    # Data for bubble: score
    # --------------------------------------------#
    
    score_work = {
        "stakeholder": "Workforce",
        "score": get_workforce_score()[1],
        "radius": get_workforce_radius(),
        'distance': get_workforce_distance(),
        'best': 50
        }

    
    # --------------------------------------------#
    # Data for chord chart: interaction
    # --------------------------------------------#
    indicator_work = [
        {"stakeholder": "Workforce", "indicator": "Access to service", "target": 'Local Business Owners', "value": cal_future_access_business()},
        {"stakeholder": "Workforce", "indicator": "Opportunity", "target": 'Local Business Owners', "value": get_opportunity_LBO(backend.input_data.amenity_space)},
        # {"stakeholder": "Workforce", "indicator": "Opportunity", "target": 'Industry Group', "value": get_opportunity_IG(backend.input_data.office_space)},
        {"stakeholder": "Workforce", "indicator": "Safety & security", "target": 'Government', "value": get_access_police_2(backend.input_data.office_space, backend.input_data.amenity_space, backend.input_data.civic_space)},
    ]
    
    # --------------------------------------------#
    # Data for indicator chart: indicator value
    # --------------------------------------------#
    index_work = [
        {"stakeholder": "Workforce","indicator": "Access to service", "baseline": access_score['before'],"score": access_score['after']},
        {"stakeholder": "Workforce","indicator": "Opportunity", "baseline": opportunity_score['before'],"score": opportunity_score['after']},
        {"stakeholder": "Workforce","indicator": "Safety & security", "baseline": safety_security_score['before'],"score": safety_security_score['after']},
    ]
    # print(score_work)
    # print(indicator_work)
    # print(index_work)
    
    return score_work, indicator_work, index_work

# if __name__ == '__main__':
    # compute_workforce()
