from model_tool import *
from ESE_metrics import *
import pandas as pd
import numpy as np
import random

VOLPE_area = 30593
max_FAR = 3.25  # from cambridge zoning regulation https://www.cambridgema.gov/~/media/Files/CDD/ZoningDevel/zoningguide/zguide.ashx
max_floor_area = 99427
floor_area = VOLPE_area * random.uniform(0, 3.25)
office_space = floor_area * 0.3 # a
amenity_space = floor_area * 0.2 # b
civic_space = floor_area * 0.1 # c
resident_space = floor_area * 0.4 # d

LB_data = cal_stakeholder()
work_num = get_work_num()
pop_num = get_res_num()


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
    get_access_NPI()

