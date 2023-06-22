from model_tool import *
from ESE_metrics import *
import pandas as pd
import numpy as np
import random

input = [0.3, 0.2, 0.1, 0.4]
VOLPE_area = 30593
max_FAR = 3.25  # from cambridge zoning regulation https://www.cambridgema.gov/~/media/Files/CDD/ZoningDevel/zoningguide/zguide.ashx
max_floor_area = 99427
floor_area = VOLPE_area * random.uniform(0, 3.25)
office_space = floor_area * input[0] # a
amenity_space = floor_area * input[1] # b
civic_space = floor_area * input[2] # c
resident_space = floor_area * input[3] # d

LB_data = cal_stakeholder()
work_num = get_work_num()
pop_num = get_res_num()


# -----------------------------------------------------
def get_tax_LBO():
    unit = 10000
    value = unit * (LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum() + amenity_space)
    max = unit * (max_floor_area + LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum())
    min = unit * LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum()
    score = norm(value, max, min)
    return score

def get_tax_res():
    unit = 5229 # MA data from https://taxadmin.memberclicks.net/2021-state-tax-revenue
    value = unit * (pop_num + resident_space/50)
    max =  unit * (pop_num + max_floor_area/50)
    min = unit * pop_num
    score = norm(value, max, min)
    return score

def get_tax_dev():
    value = floor_area
    max = max_floor_area
    min = 0
    score = norm(value, max, min)
    return score

def get_tax_IG():
    value = amenity_space
    max = max_floor_area
    min = 0
    score = norm(value, max, min)
    return score

def get_tax_work():
    value = work_num + office_space/200 + civic_space/200 + amenity_space/50
    max = work_num + max_floor_area/50
    min = work_num
    score = norm(value, max, min)
    return score

def get_manage_cost():
    value = LB_data[LB_data['stakeholder'] == 'GOV']['floor_area'].sum() + civic_space
    max = LB_data[LB_data['stakeholder'] == 'GOV']['floor_area'].sum() +max_floor_area
    min = LB_data[LB_data['stakeholder'] == 'GOV']['floor_area'].sum()
    score = norm(value, max, min)
    return score

# -----------------------------------------------------
# def get_crime_res():
#     crime = 158
#     value = crime / pop_num * (pop_num + resident_space/50)
#     max = crime / pop_num * (pop_num + max_floor_area/50)
#     min = 158
#     score = norm(value, max, min)
#     return score
#
# def get_crime_work():
#     crime = 158
#     value = crime / (work_num + office_space/200 + civic_space/200 + amenity_space/50)
#     max = crime / work_num
#     min = crime / (work_num + max_floor_area/50)
#     score = norm(value, max, min)
#     return score

def get_access_police_res():
    police_area = 500
    value = police_area/ (pop_num + resident_space/50)
    max = police_area / pop_num
    min = police_area / (pop_num + max_floor_area/50)
    score = norm(value, max, min)
    return score

def get_access_police_work():
    police_area = 500
    value = police_area / (work_num + office_space/200 + civic_space/200 + amenity_space/50)
    max = police_area / work_num
    min = police_area / (work_num + max_floor_area/50)
    score = norm(value, max, min)
    return score



if __name__ == '__main__':
    get_tax_dev()

