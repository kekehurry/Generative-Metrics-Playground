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
def get_profit_res():
    unit = 20000
    value = unit * amenity_space
    max =  unit * floor_area
    min = 0
    score = norm(value, max, min)
    return score, value
    
#def get_profit_LBO():
    unit = 20000
    value = unit * (LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum() + amenity_space)
    max = unit * (max_floor_area + LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum())
    min = unit * LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum()
    score = norm(value, max, min)
    return score
    
def get_profit_res():
    unit = 10000
    value = unit * resident_space
    max =  unit * floor_area
    min = 0
    score = norm(value, max, min)
    return score, value
    
#def get_profit_res():
    unit = 10000
    value = unit * (LB_data[LB_data['stakeholder'] == 'RS']['floor_area'].sum() + resident_space)
    max =  unit * (max_floor_area + LB_data[LB_data['stakeholder'] == 'RS']['floor_area'].sum())
    min = unit * LB_data[LB_data['stakeholder'] == 'RS']['floor_area'].sum()
    score = norm(value, max, min)
    return score

def get_profit_off():
    unit = 20000
    value = unit * office_space
    max =  unit * floor_area
    min = 0
    score = norm(value, max, min)
    return score, value

#def get_profit_off():
    unit = 30000
    value = unit * (LB_data[LB_data['stakeholder'] == 'IG']['floor_area'].sum() + office_space)
    max = unit * (max_floor_area + LB_data[LB_data['stakeholder'] == 'IG']['floor_area'].sum())
    min = unit * LB_data[LB_data['stakeholder'] == 'IG']['floor_area'].sum()
    score = norm(value, max, min)
    return score

# -----------------------------------------------------
def get_profit_developer():
    standard =  (合适推荐数值)
    pro_LBO1, pro_LBO2 = get_profit_LBO()
    pro_res1, pro_res2 = get_profit_res()
    pro_off1, pro_off2 = get_profit_off()
    value = pro_LBO2 + pro_res2 + pro_off2
    max = floor_area * 30000
    min = 0
    score = 100 - 100 * abs(value - standard) / max(abs(max - standard), abs(min - standard))

def get_tax_cost():
    standard = (合适推荐数值)
    tax_LBO = 5000
    tax_res = 4000
    tax_off = 10000 
    tax_max = max(tax_LBO, tax_res, tax_off)
    pro_LBO1, pro_LBO2 = get_profit_LBO()
    pro_res1, pro_res2 = get_profit_res()
    pro_off1, pro_off2 = get_profit_off()
    value = pro_LBO2 + pro_res2 + pro_off2
    value = tax_LBO * pro_LBO2 + tax_res * pro_res2 + tax_off * pro_off2
    max = floor_area * tax_max
    min = 0
    score = 100 - 100 * abs(value - standard) / max(abs(max - standard), abs(min - standard))
    return score

# -----------------------------------------------------
def developer():
    #表达对整体环境的贡献情况，负数表示退步,weight不一定是定值？
    weight_profit = 0.3
    weight_tax = 0.7
    score = get_profit_developer() * weight_profit + get_tax_cost() * weight_tax
    return score


if __name__ == '__main__':
    get_profit_LBO()

