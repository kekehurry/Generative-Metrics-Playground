from model_tool import *
from ESE_metrics import *
import pandas as pd
import numpy as np
import random
from stakeholders import input_values
# -----------------------------------------------------
VOLPE_area = 30593
max_FAR = 3.25  # from cambridge zoning regulation https://www.cambridgema.gov/~/media/Files/CDD/ZoningDevel/zoningguide/zguide.ashx
max_floor_area = 99427
floor_area = VOLPE_area * input_values[0]

office_space = floor_area * input_values[1] # a
amenity_space = floor_area * input_values[2] # b
civic_space = floor_area * input_values[3] # c
resident_space = floor_area * input_values[4] # d

LB_data = cal_stakeholder()
work_num = get_work_num()
pop_num = get_res_num()


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

