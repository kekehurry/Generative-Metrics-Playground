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



# -----------------------------------------------------

def get_access_service_2(service_area):
    num_work = work_num + backend.input_data.office_space/ 200 +  backend.input_data.amenity_space/50 +  backend.input_data.civic_space/200
    value = service_area / num_work
    return value

def get_access_business_2():
    business_area =  backend.input_data.amenity_space + LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum()
    value = get_access_service_2(business_area)
    max = ( backend.input_data.max_floor_area + LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum())/work_num
    min = LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum()/(work_num +  backend.input_data.max_floor_area/200)
    score = norm(value, max, min)
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

def compute_workforce():
    access_to_service = {
        "target": 'Local Business Owners',
        "value": get_access_business_2()
    }
    opportunity1 = {
        "target": 'Local Business Owners',
        "value": get_opportunity_LBO()
    }
    opportunity2 = {
        "target": 'Industry Group',
        "value": get_opportunity_IG()
    }
    safety_security = {
        "target": 'Government',
        "value": get_access_police_2()
    }

    access_score = get_before_after(0.05, access_to_service['value'])
    opportunity_score = get_before_after(0, 0.5 * opportunity1['value'] + 0.5 * opportunity2['value'])
    safety_security_score = get_before_after(1, safety_security['value'])
    # workforce_score = get_workforce_score() *100

    
    def get_workforce_score():
        weights = [1]
        scores_after = [
            access_score['after'],
            # civic_score['after'],
            # safety_security_score['after']
        ]
        scores_before = [
            access_score['before'],
            # civic_score['before'],
            # safety_security_score['before']
        ]
        score_before = int(sum(w * s for w, s in zip(weights, scores_before)) / sum(weights))
        score_after = int(sum(w * s for w, s in zip(weights, scores_after)) / sum(weights))
        return score_before, score_after

    def get_workforce_radius():
        # radius = get_workforce_score()[1]
        radius = 0
        return radius

    def get_workforce_distance():
        # distance = get_workforce_score()[1] - get_workforce_score()[0]
        distance = 0
        return distance
    
    # --------------------------------------------#
    # Data for bubble: score
    # --------------------------------------------#
    
    score_work = {
        "stakeholder": "Workforce",
        "score": get_workforce_score()[1],
        "radius": get_workforce_radius(),
        'distance': get_workforce_distance() * 2
        }
    
    # --------------------------------------------#
    # Data for chord chart: interaction
    # --------------------------------------------#
    indicator_work = [
        # {"stakeholder": "Workforce", "indicator": "Access to service", "target": access_to_service["target"], "value": access_to_service["value"]},
        # {"stakeholder": "Workforce", "indicator": "Opportunity", "target": opportunity1["target"], "value": opportunity1["value"]},
        # {"stakeholder": "Workforce", "indicator": "Opportunity", "target": opportunity2["target"], "value": opportunity2["value"]},
        # {"stakeholder": "Workforce", "indicator": "Safety & security", "target": safety_security["target"], "value": safety_security["value"]},
 ]

    # --------------------------------------------#
    # Data for indicator chart: indicator value
    # --------------------------------------------#
    index_work = [
        # {"stakeholder": "Workforce","indicator": "Access to service", "baseline": access_score['before'],"score": access_score['after']},
        # {"stakeholder": "Workforce","indicator": "Opportunity", "baseline": opportunity_score['before'],"score": opportunity_score['after']},
        # {"stakeholder": "Workforce","indicator": "Safety & security", "baseline": safety_security_score['before'],"score": safety_security_score['after']},
    ]
    
    return score_work, indicator_work, index_work

# if __name__ == '__main__':
#     get_access_business_2()

