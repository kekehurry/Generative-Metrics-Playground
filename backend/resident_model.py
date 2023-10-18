import sys
import os

import pandas as pd
import numpy as np
import random
import math

current_directory = os.path.dirname(os.path.abspath(__file__))
project_directory = os.path.join(current_directory, '..')
sys.path.append(project_directory)
from backend.model_tool import *
from backend.ESE_metrics import *
from backend.input_data import *
from backend.workforce_model import volpe_workforce_family_all, volpe_workforce_home_all
from backend.NPI_model import mit_commuters_all, mit_commuter_home_all
# -----------------------------------------------------


LB_data = cal_stakeholder()
work_num = get_work_num()
pop_num = get_res_num()

#-----------------------------------------------------
# kendall sq program
#-----------------------------------------------------

## new residents want to live here: come from volpe workforce(family) + mit commuters(family)
## unit is number of person
new_resident_demand = volpe_workforce_family_all + mit_commuters_all
# print("New residents demand:", new_resident_demand)

## number of homes needed for MIT commuters(existing) + volpe workforce(future)
## unit is household number
##-----------------
# !!!we can adjust if consider the demand from mit commuters
##-----------------
# home_demand = volpe_workforce_home_all + mit_commuter_home_all  
home_demand = volpe_workforce_home_all 
# print("Home demand:", home_demand)

housing_demand_profile = [
    0.65, # single occupancy 1
    0.15, # dual occupancy 2
    0.1, # triple occupancy 2+1
    0.05, # quad occupancy 2+2
    0.05 # family occupancy 2+3
]

unit_area = [ # sqft
    300, 
    300,
    600,
    900,
    1200
]

## calculate the new demand of housing area
unit_num_type = [int(home_demand * p) for p in housing_demand_profile]
print("Unit number count by type:",unit_num_type)

net_area = [a * b for a, b in zip(unit_area, unit_num_type)]
net_area_sum = sum(net_area)
print("Net area by type:", net_area, net_area_sum)

net_to_gross = 1.2

gross_area = [a * net_to_gross for a in net_area]
gross_area_sum = sum(gross_area)
print("Gross area by type:", gross_area, gross_area_sum)

gross_area_demand = gross_area_sum * 0.8

## current data for the area
average_resident_income = 101985 # USD median household income in kendall sq year 2021
average_rent_price = 3658 * 12 # average rent in cambridge

## define a simple rent price model
def rent_price_model(demand=gross_area_sum, supply=0, current_rent_price = average_rent_price, max_increase=1.5, min_decrease=0.5):
    if supply == 0:  # 避免除以零的错误
        return max_increase * current_rent_price
    # print("Demand:", demand)
    # print("Supply:", supply)
    rent_price_change_ratio = demand / supply
    updated_rent_price = current_rent_price

    # 缓冲系数，当demand和supply相近时，减缓rent price的变化
    buffer_coefficient = np.exp(-abs(demand - supply) / 1000)  # 可根据实际情况调整
    # 调整这个参数可以控制变化的速度
    non_linear_coefficient = 0.05  # 新增一个非线性影响系数，值越大变动越大 
    
    if rent_price_change_ratio > 1:
        change = (rent_price_change_ratio**non_linear_coefficient - 1) * (1 - buffer_coefficient)  # 调整了这里的计算方式
        updated_rent_price *= (1 + change)
        # 设置上界限
        updated_rent_price = min(updated_rent_price, current_rent_price * max_increase)
    elif rent_price_change_ratio < 1:
        change = (1 - rent_price_change_ratio**non_linear_coefficient) * (1 - buffer_coefficient)  # 调整了这里的计算方式
        updated_rent_price /= (1 + change)
        # 设置下界限
        updated_rent_price = max(updated_rent_price, current_rent_price * min_decrease)
        
    return updated_rent_price

## test model for rent price, affordability and goodness index
def test_rent_price_model():
    initial_rent_price = 3658 * 12
    resident_space = np.linspace(0, gross_area_demand*1.5, 100000)
    rent_prices = [rent_price_model(gross_area_sum, space, initial_rent_price) for space in resident_space]
    
    ## rent price -- resident space
    # 绘制结果
    plt.figure(figsize=(10,6))
    plt.plot(resident_space, rent_prices, '-o', label="Average Rent Price")
    plt.axhline(y=initial_rent_price, color='r', linestyle='--', label="Initial Rent Price")
    plt.xlabel("Resident Space")
    plt.ylabel("Average Rent Price")
    plt.title("Effect of Resident Space on Rent Price")
    plt.legend()
    plt.grid(True)
    plt.show()
    ## resident space -- affordability
    affordabilities = [affordability(average_resident_income, rent) for rent in rent_prices]
    plt.figure(figsize=(10,6))
    plt.plot(resident_space, affordabilities, '-o', label="Affordability")
    plt.xlabel("Resident Space")
    plt.ylabel("Affordability")
    plt.title("Effect of Resident Space on Affordability")
    plt.legend()
    plt.grid(True)
    plt.show()
    
    ## rent price -- affordability
    # 生成一系列的rent值
    rents = np.linspace(average_rent_price * 0.5, average_rent_price * 1.5, 500)
    # 计算对应的affordability index
    affordability_indexes = [affordability(average_resident_income, rent) for rent in rents]

    # 绘图
    plt.figure(figsize=(10,6))
    plt.plot(rents, affordability_indexes, label="Affordability Index")
    plt.axhline(y=100, color='r', linestyle='--', label="Maximum Affordability Index")
    plt.axhline(y=0, color='g', linestyle='--', label="Minimum Affordability Index")
    plt.axvline(x=average_rent_price, color='b', linestyle='--', label="Average Rent Price")
    plt.xlabel("Rent Price")
    plt.ylabel("Affordability Index")
    plt.title("Affordability Index vs Rent Price")
    plt.legend()
    plt.grid(True)
    plt.show()

## --------------------------------------------
## calculate the affordability index
## --------------------------------------------
def cal_current_affordability_index():
    affordability_index = affordability(average_resident_income, average_rent_price)
    # print("Affordability index:", affordability_index)
    return round(affordability_index, 2)

def cal_future_affordability_index():
    volpe_resident_space = resident_space * 10.7639
    # volpe_office_space = office_space * 10.7639
    rent_price = rent_price_model(gross_area_sum, volpe_resident_space, average_rent_price, 1.5, 0.5)
    affordability_index = affordability(average_resident_income, rent_price)
    # print(volpe_resident_space, volpe_office_space)
    # print("Rent price:", rent_price)
    # print("Affordability index:", affordability_index)
    
    return round(affordability_index, 2)

# A typical renter household is defined as one that earns median renter household income 
# and a typical rental home is defined as a median-priced rental unit. The index assumes 
# that a household that qualifies for a lease has an annual rent that is no greater than 
# 30 percent of the household’s annual income, which is what most landlords require. The
# rental affordability index will equal 100 if the median income of renter households is 
# just high enough to qualify for the median-priced rental unit. An index value greater 
# than 100 indicates that the median income of renter households is more than enough to 
# qualify for the median-priced rental unit.
# calculate the affordability index from rent price and income
def affordability(income, rent):
    rent_to_income_ratio = rent / income
    max_rent_to_income_ratio = average_rent_price * 1.5 / income 

    # 归一化租金到收入比率到 [0, 1]
    normalized_ratio = (rent_to_income_ratio - 0.3) / (max_rent_to_income_ratio - 0.3)

    # 使用 Sigmoid 函数的倒数来模拟 affordability_index 的下降
    affordability_index = 100 / (1 + np.exp(10 * (normalized_ratio - 0.5)))

    return affordability_index


# -----------------------------------------------------
# def goodness(x,optimal_value):
#     variance = 0.1  # adjustable
#     goodness_index = math.exp(-((x - optimal_value)**2) / (2 * variance**2))
#     return goodness_index



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

class Resident():
    def __init__(self):

        self.access_to_service1 = {
            "target": 'Local Business Owners',
            "value": get_access_business()
        }
        self.access_to_service2 = {
            "target": 'Nonprofit Institution',
            "value": get_access_NPI()
        }
        # self.job_housing = {
        #     "target": 'Workforce',
        #     "value": round(random.uniform(0, 1), 2)
        # }
        self.civic_space = {
            "target": 'Government',
            "value": get_access_civic()
        }
        self.safety_security = {
            "target": 'Government',
            "value": get_access_police()
        }
        
        # self.tax_cost = {
        #     "target": 'Government',
        #     "value": round(random.uniform(0, 1), 2)
        # }
        # self.build_up_area = {
        #     "target": 'Developer',
        #     "value": round(random.uniform(0, 1), 2)
        # }
        
        self.affordable_score = get_before_after(
            cal_current_affordability_index(),
            cal_future_affordability_index())
        self.access_score = get_before_after(
            0.77, 
            0.5* self.access_to_service1['value']+ 0.5* self.access_to_service2['value']
            )
        self.civic_score =  get_before_after(
            0.76, self.civic_space['value'])
        self.safety_security_score = get_before_after(
            1, 
            self.safety_security['value'])
        # self.tax_cost_score = get_before_after(0, self.tax_cost['value'])


    def get_resident_score(self):
        weights = [1]
        scores_after = [
            self.affordable_score['after'],
            # self.access_score['after'],
            # self.civic_score['after'],
            # self.safety_security_score['after']
        ]
        scores_before = [
            self.affordable_score['before'],
            # self.access_score['before'],
            # self.civic_score['before'],
            # self.safety_security_score['before']
        ]
        score_before = int(sum(w * s for w, s in zip(weights, scores_before)) / sum(weights))
        score_after = int(sum(w * s for w, s in zip(weights, scores_after)) / sum(weights))
        return score_before, score_after
    
    def get_resident_radius(self):
        radius = self.get_resident_score()[1]
        return radius
    
    def get_resident_distance(self):
        distance = self.get_resident_score()[1] - self.get_resident_score()[0]
        return distance


##--------------------------------------------##
resident = Resident()
# --------------------------------------------#
# Data for chord chart: interaction
# --------------------------------------------#
score_res = {
    "stakeholder": "Residents",
    "score": resident.get_resident_score()[1],
    "radius": resident.get_resident_radius(),
    'distance': resident.get_resident_distance()
    }

# --------------------------------------------#
# Data for chord chart: interaction
# --------------------------------------------#
indicator_res = [
    # {"stakeholder": "Residents", "indicator": "Affordability", "target": resident.access_to_service1["target"], "value": resident.access_to_service1["value"]},
    {"stakeholder": "Residents", "indicator": "Access to service", "target": resident.access_to_service1["target"], "value": resident.access_to_service1["value"]},
    {"stakeholder": "Residents", "indicator": "Access to service", "target": resident.access_to_service2["target"], "value": resident.access_to_service2["value"]},
    # {"stakeholder": "Resident", "indicator": "Job-housing balance", "target": resident.job_housing["target"], "value": resident.job_housing["value"]},
    {"stakeholder": "Residents", "indicator": "Civic space", "target": resident.civic_space["target"], "value": resident.civic_space["value"]},
    {"stakeholder": "Residents", "indicator": "Safety & security", "target": resident.safety_security["target"], "value": resident.safety_security["value"]}
    # {"stakeholder": "Resident", "indicator": "Tax", "target": resident.tax_cost["target"], "value": resident.tax_cost["value"]},
    # {"stakeholder": "Resident", "indicator": "Build-up area", "target": resident.build_up_area["target"], "value": resident.build_up_area["value"]}
]

# --------------------------------------------#
# Data for indicator chart: indicator value
# --------------------------------------------#
index_res = [
    {"stakeholder": "Residents","indicator": "Affordability", "baseline": resident.affordable_score['before'],"score": resident.affordable_score['after']}
    # {"stakeholder": "Residents","indicator": "Access to service", "baseline": resident.access_score['before'],"score": resident.access_score['after']},
    # {"stakeholder": "Residents","indicator": "Civic space", "baseline": resident.civic_score['before'],"score": resident.civic_score['after']},
    # {"stakeholder": "Residents","indicator": "Safety & security", "baseline": resident.safety_security_score['before'],"score": resident.safety_security_score['after']}
    # {"stakeholder": "Resident","indicator": "Tax", "baseline": resident.tax_cost_score['before'],"score": resident.tax_cost_score['after']}
]


if __name__ == '__main__':
    # print(goodness(affordability(average_resident_income, average_rent_price), 0.3))
    # test_rent_price_model()
    print("score_res:\n",score_res)
    print("indicator_res:\n",indicator_res)
    print("index_res:\n",index_res)
    
