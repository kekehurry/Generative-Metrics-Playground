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
from backend.input_data import input_value
# -----------------------------------------------------
VOLPE_area = 30593
max_FAR = 3.25  # from cambridge zoning regulation https://www.cambridgema.gov/~/media/Files/CDD/ZoningDevel/zoningguide/zguide.ashx
max_floor_area = 99427
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
    num_res = pop_num + resident_space/ 50
    value = service_area / num_res
    return value

def get_access_LBO():
    business_area = amenity_space + LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum()
    value = get_access_service(business_area)
    max = (max_floor_area + LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum())/pop_num
    min = LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum()/(pop_num + max_floor_area/50)
    score = norm(value, max, min)
    return score

# -----------------------------------------------------
def get_access_IG():
    value = LB_data[LB_data['stakeholder'] == 'IG']['floor_area'].sum()+ amenity_space
    max = max_floor_area + LB_data[LB_data['stakeholder'] == 'IG']['floor_area'].sum()
    min = LB_data[LB_data['stakeholder'] == 'IG']['floor_area'].sum()
    score = norm(value, max, min)
    return score

# -----------------------------------------------------
def get_access_police_4():
    police_area = 500
    value = get_access_service(police_area)
    max = police_area / pop_num
    min = police_area / (pop_num + max_floor_area / 50)
    score = norm(value, max, min)
    return score



if __name__ == '__main__':
    get_access_LBO()

