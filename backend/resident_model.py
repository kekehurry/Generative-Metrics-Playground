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


# -----------------------------------------------------

def get_access_service(service_area):
    num_res = pop_num + resident_space/ 50
    value = service_area / num_res
    return value

def get_access_business():
    business_area = amenity_space + LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum()
    value = get_access_service(business_area)
    max = (max_floor_area + LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum())/pop_num
    min = LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum()/(pop_num + max_floor_area/50)
    score = norm(value, max, min)
    return score

def get_access_NPI():
    MIT = 10000
    value = get_access_service(MIT)
    max = MIT/pop_num
    min = MIT/(pop_num + max_floor_area/50)
    score = norm(value, max, min)
    return score

# -----------------------------------------------------
def get_access_civic():
    civic_area = civic_space + LB_data[LB_data['stakeholder'] == 'GOV']['floor_area'].sum()
    value = get_access_service(civic_area)
    max = (max_floor_area + LB_data[LB_data['stakeholder'] == 'GOV']['floor_area'].sum()) /pop_num
    min = LB_data[LB_data['stakeholder'] == 'GOV']['floor_area'].sum()/(pop_num + max_floor_area/50)
    score = norm(value, max, min)
    return score

# -----------------------------------------------------
def get_access_police():
    police_area = 500
    value = get_access_service(police_area)
    max = police_area / pop_num
    min = police_area / (pop_num + max_floor_area / 50)
    score = norm(value, max, min)
    return score



if __name__ == '__main__':
    get_access_NPI()

