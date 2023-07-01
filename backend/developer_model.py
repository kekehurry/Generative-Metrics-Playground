from model_tool import *
from ESE_metrics import *
import pandas as pd
import numpy as np
import random
from input_data import input_values
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
def get_profit_LBO():
    unit = 20000
    value = unit * (LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum() + amenity_space)
    max = unit * (max_floor_area + LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum())
    min = unit * LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum()
    score = norm(value, max, min)
    return score

def get_profit_res():
    unit = 10000
    value = unit * (LB_data[LB_data['stakeholder'] == 'RS']['floor_area'].sum() + resident_space)
    max =  unit * (max_floor_area + LB_data[LB_data['stakeholder'] == 'RS']['floor_area'].sum())
    min = unit * LB_data[LB_data['stakeholder'] == 'RS']['floor_area'].sum()
    score = norm(value, max, min)
    return score

def get_profit_IG():
    unit = 30000
    value = unit * (LB_data[LB_data['stakeholder'] == 'IG']['floor_area'].sum() + office_space)
    max = unit * (max_floor_area + LB_data[LB_data['stakeholder'] == 'IG']['floor_area'].sum())
    min = unit * LB_data[LB_data['stakeholder'] == 'IG']['floor_area'].sum()
    score = norm(value, max, min)
    return score

def get_tax_cost():
    value = floor_area
    max = max_floor_area
    min = 0
    score = norm(value, max, min)
    return score

# -----------------------------------------------------




if __name__ == '__main__':
    get_profit_LBO()

