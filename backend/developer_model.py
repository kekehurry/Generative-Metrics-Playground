import sys
import os
current_directory = os.path.dirname(os.path.abspath(__file__))
project_directory = os.path.join(current_directory, '..')
sys.path.append(project_directory)

import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import backend.input_data
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

## --------------------------------------------
## calculate the affordability index
## --------------------------------------------

def cal_gross_income(resident_space, office_space, amenity_space):
    res_develop_cost = 150 # $/sqft estimated value
    office_develop_cost = 300 # $/sqft estimated value  high-rise office: $660/sqft
    ## 10% or residential space is affordable housing
    resident_space = resident_space * 0.9
    all_develop_cost = (
        (res_develop_cost * resident_space  + 
         office_develop_cost * (office_space + amenity_space)) * 10.7639
        )
    # here we didn't consider the land cost
    # print("All develop cost:", all_develop_cost)
    
    house_rent_price = 55 # /sqft/year estimated value median price of cambridge: $49/sqft/year 
    house_vacancy_rate = 0.084 # 
    operate_expense = 6.5 # /sqft/year estimated value
    real_estate_tax = 2.5 # /sqft/year estimated value 
    
    office_rent_price = 100  # /sqft/year average office rent in cambridge year 2021
    office_vacancy_rate = 0.042 # average office vacancy rate in cambridge year 2021
    
    retail_rent_price = 100 # /sqft/year estimated value
    retail_vacancy_rate = 0.033 # 
    
    replace_reserve = 1 # /sqft/year estimated value
    # parking_ratio = 2.79/1000
    # yearly gross income
    gross_income = (
        house_rent_price * resident_space * 10.7639 * (1 - house_vacancy_rate) 
        + office_rent_price * office_space * 10.7639 * (1 - office_vacancy_rate)
        + retail_rent_price * amenity_space * 10.7639 * (1 - retail_vacancy_rate)
        )
    expense = (
        operate_expense * resident_space * 10.7639
        + real_estate_tax * resident_space * 10.7639
        + replace_reserve * (resident_space + office_space + amenity_space) * 10.7639
    )
    return all_develop_cost, gross_income, expense

def pro_forma(resident_space, office_space, amenity_space):
    
    all_develop_cost, gross_income, expense = cal_gross_income(resident_space, office_space, amenity_space)
    
    net_income = gross_income - expense
    # print("Net income:", net_income)
    
    # use the return on total assets (ROTA) to measure the profitability of the project
    # tax not included here
    return_on_asset = net_income / all_develop_cost
    # print("Return on asset:", return_on_asset)
    roa_index = calculate_normalized_roa(return_on_asset, 0.265, 0.32)
    # print("ROA index:", roa_index)
    return roa_index

def test_pro_forma():
    resident_spaces = np.linspace(0, 100000, 100)
    office_spaces = np.linspace(0, 100000, 100)
    amenity_spaces = np.linspace(0, 100000, 100)

    combinations = [
        ('Resident', 'Office', 'Amenity', resident_spaces, office_spaces, backend.input_data.amenity_space),
        ('Resident', 'Amenity', 'Office', resident_spaces, amenity_spaces, backend.input_data.office_space),
        ('Office', 'Amenity', 'Resident', office_spaces, amenity_spaces, backend.input_data.resident_space)
    ]
    
    for comb in combinations:
        X_name, Y_name, Z_name, X_spaces, Y_spaces, Z_space_fixed = comb
        X_spaces, Y_spaces = np.meshgrid(X_spaces, Y_spaces)
        
        roas = np.array([pro_forma(x, y, Z_space_fixed)
                        for x, y in zip(np.ravel(X_spaces), np.ravel(Y_spaces))])
        roas = roas.reshape(X_spaces.shape)

        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection='3d')
        surf = ax.plot_surface(X_spaces, Y_spaces, roas, cmap='viridis')

        ax.set_title(f'Return on Asset vs {X_name} Space and {Y_name} Space\n'
                     f'{Z_name} Space Fixed at {Z_space_fixed} sqft')
        ax.set_xlabel(f'{X_name} Space (sqft)')
        ax.set_ylabel(f'{Y_name} Space (sqft)')
        ax.set_zlabel('Return on Asset')
        fig.colorbar(surf)

        plt.show()  # 这将会在每次循环结束时显示图像，关闭图像窗口后继续下一次循环

# 找到ROA的最大和最小值
def find_roa_extremes(res_spaces, off_spaces, amen_spaces):
    roas = np.array([pro_forma(res, off, amen) for res in res_spaces 
                     for off in off_spaces for amen in amen_spaces])
    # 检查是否有NaN值
    if np.isnan(roas).any():
        print("Warning: NaN values detected, they will be ignored.")
    return np.nanmin(roas), np.nanmax(roas)

# 计算标准化的资产回报率
def calculate_normalized_roa(roa, roa_min, roa_max):
    normalized_roa = 100 * (roa - roa_min) / (roa_max - roa_min)
    # 确保 normalized_roa 的值在 0-100 之间
    normalized_roa = max(0, min(100, normalized_roa))
    return round(normalized_roa, 2)

# def test_return_range():
#     # 设置参数范围
#     resident_spaces = np.linspace(10, 900000, 100)  # 示例值，可以调整
#     office_spaces = np.linspace(10, 900000, 100)    # 示例值，可以调整
#     amenity_spaces = np.linspace(10, 900000, 100)    # 示例值，可以调整

#     # 找到ROA的极值
#     roa_min, roa_max = find_roa_extremes(resident_spaces, office_spaces, amenity_spaces)
#     print("roa_min:", roa_min, "roa_max:", roa_max)
#     # 计算一个特定情况下的ROA
#     example_roa = pro_forma( backend.input_data.resident_space, backend.input_data.office_space, backend.input_data.amenity_space)  # 示例参数值，可以调整

#     # 标准化ROA到0-100的范围
#     normalized_roa = calculate_normalized_roa(example_roa, roa_min, roa_max)

#     print(f"Original ROA: {example_roa}")
#     print(f"Normalized ROA (0-100 scale): {normalized_roa}")
#     # get roa_min = 0.265, roa_max = 0.32
#     return normalized_roa

def test_return_range():
    # 设置参数范围
    resident_spaces = np.linspace(10, 900000, 100)  # 示例值，可以调整
    office_spaces = np.linspace(10, 900000, 100)    # 示例值，可以调整
    amenity_spaces = np.linspace(10, 900000, 100)    # 示例值，可以调整

    roas = []
    combinations = []

    # 计算不同参数组合下的 ROA
    for res in resident_spaces:
        for off in office_spaces:
            for ame in amenity_spaces:
                roa = pro_forma(res, off, ame)
                roas.append(roa)
                combinations.append((res, off, ame))

    # 画出 ROA 的散点图
    plt.figure(figsize=(10,6))
    plt.scatter(range(len(roas)), roas, c=roas, cmap='viridis', marker='o')
    plt.colorbar(label='ROA Value')
    plt.xlabel('Combination Index')
    plt.ylabel('ROA Value')
    plt.title('ROA for Different Parameter Combinations')
    plt.show()

    min_roa = min(roas)
    max_roa = max(roas)

    print(f"min ROA: {min_roa}")
    print(f"max ROA: {max_roa}")

    return min_roa, max_roa
    

def cal_current_profit_index():
    profit_index = 0
    return profit_index

def cal_future_profit_index():
    profit_index = pro_forma(backend.input_data.resident_space, 
                             backend.input_data.office_space, 
                             backend.input_data.amenity_space)
    return profit_index
    

# -----------------------------------------------------
# def get_profit_res():
#     unit = 20000
#     value = unit * amenity_space
#     max =  unit * floor_area
#     min = 0
#     score = norm(value, max, min)
#     return score, value
    
# def get_profit_LBO():
#     unit = 20000
#     value = unit * (LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum() +  backend.input_data.amenity_space)
#     max = unit * ( backend.input_data.max_floor_area + LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum())
#     min = unit * LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum()
#     score = norm(value, max, min)
#     return score
    
# def get_profit_res():
#     unit = 10000
#     value = unit * resident_space
#     max =  unit * floor_area
#     min = 0
#     score = norm(value, max, min)
#     return score, value
    
# def get_profit_res():
#     unit = 10000
#     value = unit * (LB_data[LB_data['stakeholder'] == 'RS']['floor_area'].sum() +  backend.input_data.resident_space)
#     max =  unit * ( backend.input_data.max_floor_area + LB_data[LB_data['stakeholder'] == 'RS']['floor_area'].sum())
#     min = unit * LB_data[LB_data['stakeholder'] == 'RS']['floor_area'].sum()
#     score = norm(value, max, min)
#     return score

# def get_profit_off():
#     unit = 20000
#     value = unit * office_space
#     max =  unit * floor_area
#     min = 0
#     score = norm(value, max, min)
#     return score, value

# def get_profit_IG():
#     unit = 30000
#     value = unit * (LB_data[LB_data['stakeholder'] == 'IG']['floor_area'].sum() +  backend.input_data.office_space)
#     max = unit * ( backend.input_data.max_floor_area + LB_data[LB_data['stakeholder'] == 'IG']['floor_area'].sum())
#     min = unit * LB_data[LB_data['stakeholder'] == 'IG']['floor_area'].sum()
#     score = norm(value, max, min)
#     return score

# -----------------------------------------------------
# def get_profit_developer():
#     standard = 100 # (合适推荐数值)
#     pro_LBO1, pro_LBO2 = get_profit_LBO()
#     pro_res1, pro_res2 = get_profit_res()
#     # pro_off1, pro_off2 = get_profit_off()
#     pro_IG1, pro_IG2 = get_profit_IG()
#     value = pro_LBO2 + pro_res2 + pro_IG2
#     max =  backend.input_data.floor_area * 30000
#     min = 0
#     score = 100 - 100 * abs(value - standard) / max(abs(max - standard), abs(min - standard))
#     return score

# def get_tax_cost():
#     standard = 10 #(合适推荐数值)
#     tax_LBO = 50
#     tax_res = 40
#     tax_IG = 10
#     tax_max = max(tax_LBO, tax_res, tax_IG)

#     # pro_LBO1, pro_LBO2 = get_profit_LBO()
#     # pro_res1, pro_res2 = get_profit_res()
#     # # pro_off1, pro_off2 = get_profit_off()
#     # pro_IG1, pro_IG2 = get_profit_IG()
#     pro_LBO2 = get_profit_LBO()
#     pro_res2 = get_profit_res()
#     pro_IG2 = get_profit_IG()
#     value = pro_LBO2 + pro_res2 + pro_IG2
#     # value = tax_LBO * pro_LBO2 + tax_res * pro_res2 + tax_off * pro_IG2
#     max_value =  backend.input_data.floor_area * tax_max
#     min_value = 0
#     score = 1 - 100 * abs(value - standard) / max(abs(max_value - standard), abs(min_value - standard))
#     return score

# -----------------------------------------------------

def compute_developer():

    profit_score = get_before_after(
        cal_current_profit_index(),
        cal_future_profit_index()
    )

    def get_developer_score():
        weights = [1]
        scores_after = [
            profit_score['after']
            # profit_construction_score['after'],
            # tax_cost_score['after']
        ]
        scores_before = [
            profit_score['before']
            # profit_construction_score['before'],
            # tax_cost_score['before']
        ]
        score_before = int(sum(w * s for w, s in zip(weights, scores_before)) / sum(weights))
        score_after = int(sum(w * s for w, s in zip(weights, scores_after)) / sum(weights))
        return score_before, score_after
    
    def get_developer_radius():
        radius = get_developer_score()[1]
        return radius
    
    def get_resident_distance():
        # distance = get_developer_score()[1] - get_developer_score()[0]
        distance = get_developer_score()[1]
        return distance
    

    # --------------------------------------------#
    # Data for chord chart: interaction
    # --------------------------------------------#
    score_dev = {
        "stakeholder": "Developer", 
        "score": get_developer_score()[1], 
        "initial_score": get_developer_score()[0],
        "radius": get_developer_radius(), 
        'distance': get_resident_distance(),
        'best': 50
        }

    # --------------------------------------------#
    # Data for chord chart: interaction
    # --------------------------------------------#
    indicator_dev = [
        {"stakeholder": "Developer", "indicator": "Profit", "target": 'Local Business Owners', "value": cal_future_profit_index()/2/100},
        {"stakeholder": "Developer", "indicator": "Profit", "target": 'Residents', "value": cal_future_profit_index()/2/100},
        # {"stakeholder": "Developer", "indicator": "Profit", "target": 'Industry Group', "value": profit_construction3["value"]},
        # {"stakeholder": "Developer", "indicator": "Tax", "target":'Government', "value": tax_cost["value"]}
        ]

    # --------------------------------------------#
    # Data for indicator chart: indicator value
    # --------------------------------------------#
    index_dev = [
        {"stakeholder": "Developer","indicator": "Profit", "baseline": profit_score['before'],"score": profit_score['after']},
        ]
    
    # print(score_dev)
    # print(indicator_dev)
    # print(index_dev)
    
    return score_dev, indicator_dev, index_dev


# if __name__ == '__main__':
#     compute_developer()
    # pro_forma()
    # test_pro_forma()
    # test_return_range()
    # cal_future_profit_index()
    
    # test the score for the best return
    # print(calculate_normalized_roa( , 0.265, 0.32))
        
#     print("score_dev:\n",score_dev)
#     print("indicator_dev:\n",indicator_dev)
#     print("index_dev:\n",index_dev)
    