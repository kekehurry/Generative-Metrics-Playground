import sys
import os
current_directory = os.path.dirname(os.path.abspath(__file__))
project_directory = os.path.join(current_directory, '..')
sys.path.append(project_directory)

import pandas as pd
import numpy as np
import random

from backend.input_data import *
from backend.model_tool import *
from backend.ESE_metrics import *
from backend.NPI_model import mit_commuter_home_all
from backend.workforce_model import volpe_workforce_home_all
# -----------------------------------------------------

LB_data = cal_stakeholder()
work_num = get_work_num()
pop_num = get_res_num()

#-----------------------------------------------------
# kendall sq program
#-----------------------------------------------------

# ## number of homes needed for MIT commuters(existing) + volpe workforce(future)
# ## unit is household number
# home_demand = volpe_workforce_home_all + mit_commuter_home_all
# print("Home demand:", home_demand)





net_to_gross = 1.2



# -----------------------------------------------------
# def get_profit_res():
#     unit = 20000
#     value = unit * amenity_space
#     max =  unit * floor_area
#     min = 0
#     score = norm(value, max, min)
#     return score, value
    
def get_profit_LBO():
    unit = 20000
    value = unit * (LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum() + amenity_space)
    max = unit * (max_floor_area + LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum())
    min = unit * LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum()
    score = norm(value, max, min)
    return score
    
# def get_profit_res():
#     unit = 10000
#     value = unit * resident_space
#     max =  unit * floor_area
#     min = 0
#     score = norm(value, max, min)
#     return score, value
    
def get_profit_res():
    unit = 10000
    value = unit * (LB_data[LB_data['stakeholder'] == 'RS']['floor_area'].sum() + resident_space)
    max =  unit * (max_floor_area + LB_data[LB_data['stakeholder'] == 'RS']['floor_area'].sum())
    min = unit * LB_data[LB_data['stakeholder'] == 'RS']['floor_area'].sum()
    score = norm(value, max, min)
    return score

# def get_profit_off():
#     unit = 20000
#     value = unit * office_space
#     max =  unit * floor_area
#     min = 0
#     score = norm(value, max, min)
#     return score, value

def get_profit_IG():
    unit = 30000
    value = unit * (LB_data[LB_data['stakeholder'] == 'IG']['floor_area'].sum() + office_space)
    max = unit * (max_floor_area + LB_data[LB_data['stakeholder'] == 'IG']['floor_area'].sum())
    min = unit * LB_data[LB_data['stakeholder'] == 'IG']['floor_area'].sum()
    score = norm(value, max, min)
    return score

# -----------------------------------------------------
def get_profit_developer():
    standard = 100 # (合适推荐数值)
    pro_LBO1, pro_LBO2 = get_profit_LBO()
    pro_res1, pro_res2 = get_profit_res()
    # pro_off1, pro_off2 = get_profit_off()
    pro_IG1, pro_IG2 = get_profit_IG()
    value = pro_LBO2 + pro_res2 + pro_IG2
    max = floor_area * 30000
    min = 0
    score = 100 - 100 * abs(value - standard) / max(abs(max - standard), abs(min - standard))
    return score

def get_tax_cost():
    standard = 10 #(合适推荐数值)
    tax_LBO = 50
    tax_res = 40
    tax_IG = 10
    tax_max = max(tax_LBO, tax_res, tax_IG)

    # pro_LBO1, pro_LBO2 = get_profit_LBO()
    # pro_res1, pro_res2 = get_profit_res()
    # # pro_off1, pro_off2 = get_profit_off()
    # pro_IG1, pro_IG2 = get_profit_IG()
    pro_LBO2 = get_profit_LBO()
    pro_res2 = get_profit_res()
    pro_IG2 = get_profit_IG()
    value = pro_LBO2 + pro_res2 + pro_IG2
    # value = tax_LBO * pro_LBO2 + tax_res * pro_res2 + tax_off * pro_IG2
    max_value = floor_area * tax_max
    min_value = 0
    score = 1 - 100 * abs(value - standard) / max(abs(max_value - standard), abs(min_value - standard))
    return score

# -----------------------------------------------------
def developer():
    #表达对整体环境的贡献情况，负数表示退步,weight不一定是定值？
    weight_profit = 0.3
    weight_tax = 0.7
    score = get_profit_developer() * weight_profit + get_tax_cost() * weight_tax
    return score

class Developer():
    def __init__(self):
        self.profit_construction1 = {
            "target": 'Local Business Owners',
            "value": get_profit_LBO()
        }
        self.profit_construction2 = {
            "target": 'Residents',
            "value": get_profit_res()
        }
        self.profit_construction3 = {
            "target": 'Industry Group',
            "value": get_profit_IG()
        }
        self.tax_cost = {
            "target": 'Government',
            "value": get_tax_cost()
        }
        # self.innovation = {
        #     "target": 'Non-Profit Institution',
        #     "value": round(random.uniform(0, 1), 2)
        # }

        self.profit_construction_score = get_before_after(0, 0.33 * self.profit_construction1['value'] + 0.33 * self.profit_construction2['value'] + 0.34 * self.profit_construction3['value'])
        self.tax_cost_score = get_before_after(0, self.tax_cost['value'])
        # self.innovation_score = get_before_after(0, 1)
        self.developer_score = self.get_developer_score() *100

    def get_developer_score(self):
        score = 0.5 * self.profit_construction_score['after'] + 0.5 * self.tax_cost_score['after']
        return score

if __name__ == '__main__':
    get_profit_LBO()

