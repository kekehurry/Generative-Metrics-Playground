import sys
import os
current_directory = os.path.dirname(os.path.abspath(__file__))
project_directory = os.path.join(current_directory, '..')
sys.path.append(project_directory)
from backend.input_data import input_value
from backend.model_tool import *
from backend.ESE_metrics import *
# from backend.developer_model import volpe_office
import pandas as pd
import numpy as np
import random

# -----------------------------------------------------
VOLPE_area = 30593 # sqm
## could be changed by negotiation with government
# max_FAR = 3.25  ## from cambridge zoning regulation https://www.cambridgema.gov/~/media/Files/CDD/ZoningDevel/zoningguide/zguide.ashx
# max_floor_area = 99427
floor_area = VOLPE_area * input_value['bcr'] * input_value['tier']  # 0.6 is the bcr, 3 is the tier

office_space = floor_area * input_value['office'] 
amenity_space = floor_area * input_value['amenity']
civic_space = floor_area * input_value['civic']
resident_space = floor_area * input_value['residential'] 

LB_data = cal_stakeholder()
work_num = get_work_num()
pop_num = get_res_num()

#-----------------------------------------------------
# kendall sq program
#-----------------------------------------------------

# this is an initial setting of office area
# volpe_office_all = 1700000 #sqft all
volpe_office_all = office_space * 10.7639 #sqft all

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
    num_work = work_num + office_space/ 200 + amenity_space/50 + civic_space/200
    value = service_area / num_work
    return value

def get_access_business_2():
    business_area = amenity_space + LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum()
    value = get_access_service_2(business_area)
    max = (max_floor_area + LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum())/work_num
    min = LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum()/(work_num + max_floor_area/200)
    score = norm(value, max, min)
    return score


# -----------------------------------------------------
def get_opportunity_LBO():
    LBO_area = LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum()
    value = LBO_area + amenity_space
    max = max_floor_area + LBO_area
    min = LBO_area
    score = norm(value, max, min)
    return score

def get_opportunity_IG():
    IG_area = LB_data[LB_data['stakeholder'] == 'IG']['floor_area'].sum()
    value = IG_area + office_space
    max = max_floor_area + IG_area
    min = IG_area
    score = norm(value, max, min)
    return score

# -----------------------------------------------------
def get_access_police_2():
    police_area = 500
    value = police_area / (work_num + office_space/200 + amenity_space/50 + civic_space/200)
    max = police_area / work_num
    min = police_area / (work_num + max_floor_area / 50)
    score = norm(value, max, min)
    return score



if __name__ == '__main__':
    get_access_business_2()

