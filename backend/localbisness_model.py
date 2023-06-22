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

def get_business_res():
    business_area = amenity_space + LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum()
    value = business_area/ (pop_num + resident_space/50)
    max = (max_floor_area + LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum())/pop_num
    min = LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum()/(pop_num + max_floor_area/50)
    score = norm(value, max, min)
    return score

def get_business_work():
    business_area = amenity_space + LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum()
    value = business_area/ (work_num + office_space/200 + amenity_space/50 + civic_space/200)
    max = (max_floor_area + LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum())/(work_num+amenity_space/50)
    min = LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum()/(work_num + max_floor_area/200)
    score = norm(value, max, min)
    return score


# -----------------------------------------------------
def get_access_police_3():
    police_area = 500
    value = police_area/ (LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum() + amenity_space)
    max = police_area / ( LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum())
    min = police_area / (LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum() + max_floor_area)
    score = norm(value, max, min)
    return score



if __name__ == '__main__':
    get_access_police_3()

