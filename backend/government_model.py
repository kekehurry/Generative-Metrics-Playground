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
import backend.input_data 
# from backend.developer_model import 
from backend.workforce_model import volpe_workforce_home_all
from backend.resident_model import new_resident_num
# -----------------------------------------------------

LB_data = cal_stakeholder()
work_num = get_work_num()
pop_num = get_res_num()

#-----------------------------------------------------
# kendall sq program
#-----------------------------------------------------

def property_tax_revenue(resident_space, office_space, amenity_space):
    res_develop_cost = 150 # $/sqft estimated value
    office_develop_cost = 300 # $/sqft estimated value  high-rise office: $660/sqft
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
    gross_income_res = house_rent_price * resident_space * 10.7639 * (1 - house_vacancy_rate)
    gross_income_office = office_rent_price * office_space * 10.7639 * (1 - office_vacancy_rate)
    gross_income_retail = retail_rent_price * amenity_space * 10.7639 * (1 - retail_vacancy_rate)
    
    res_expense = (
        operate_expense * resident_space * 10.7639
        + real_estate_tax * resident_space * 10.7639
        + replace_reserve * resident_space * 10.7639
    )
    office_expense = replace_reserve * office_space * 10.7639
    retail_expense = replace_reserve * amenity_space * 10.7639
    
    net_income_res = gross_income_res - res_expense
    net_income_office = gross_income_office - office_expense
    net_income_retail = gross_income_retail - retail_expense
 
    # sale price = net income / cap rate for sale (set as 6.9%)
    sale_price_res = net_income_res / 0.069
    
    # res_property_tax_1 = resident_space * 10.7639 * real_estate_tax
    # print("res_property_tax_1:", res_property_tax_1)
    
    # residential property tax rate: 5.92/1000 in Cambridge 2022 
    res_property_tax_2 = sale_price_res * 5.92/1000
    # print("res_property_tax_2:", res_property_tax_2)
    
    # commercial/industrial property tax rate: 11.23/$1000 in Cambridge 2022
    com_property_tax = (net_income_office+net_income_retail) / 0.069 * 11.23/1000
    # print("com_property_tax:", com_property_tax)
    
    return com_property_tax, res_property_tax_2

def sales_tax_revenue(amenity_space):
    # average sales density of us retail: $338.3/sqft/year
    sales_value = 338.3 * amenity_space * 10.7639
    sales_tax = sales_value * 0.0625
    # print("sales_tax:", sales_tax)
    return sales_tax

def income_tax_revenue(resident_space):
    # average small business owner salary in MA: $111,458 /year/person
    
    # average household income in kendall square: 101985
    # personal income tax rate: 5% in MA  
    new_residents = new_resident_num(resident_space)
    income_tax = 0.05 * new_residents * 101985
    # print("income_tax:", income_tax)
    return income_tax
    

def tax_revenue(resident_space, office_space, amenity_space):
    # property tax
    com_property_tax, res_property_tax = property_tax_revenue(resident_space, office_space, amenity_space)
    # print("com_property_tax:", com_property_tax)
    # sales tax
    sales_tax = sales_tax_revenue(amenity_space)
    # print("sales_tax:", sales_tax)
    # income tax
    income_tax = income_tax_revenue(resident_space)
    # print("income_tax:", income_tax)
    
    # total tax revenue
    total_tax_revenue = com_property_tax + res_property_tax + sales_tax + income_tax
    # print("total_tax_revenue:", total_tax_revenue)

    return total_tax_revenue

def tax_revenue_score(resident_space, office_space, amenity_space):
    total_tax_revenue = tax_revenue(resident_space, office_space, amenity_space)
    tax_score = tax_revenue_to_index(total_tax_revenue)
    # print("tax_index:", tax_score)
    return tax_score

def test_tax_revenue():
    num_points = 10
    resident_space_range = np.linspace(0, 100000, num_points)
    office_space_range = np.linspace(0, 100000, num_points)
    amenity_space_range = np.linspace(0, 100000, num_points)
    
    # 使用 meshgrid 函数创建一个 3D 参数网格
    rs, os, asp = np.meshgrid(resident_space_range, office_space_range, amenity_space_range, indexing='ij')

    # 初始化一个用于存储税收总额的数组
    total_tax_revenues = np.zeros_like(rs)

    # 计算每一组参数对应的税收总额
    for i in range(num_points):
        for j in range(num_points):
            for k in range(num_points):
                total_tax_revenues[i, j, k] = tax_revenue_score(rs[i, j, k], os[i, j, k], asp[i, j, k])

    # 创建一个 3D 散点图来表示结果
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # 可以选择一个合适的阈值，仅绘制税收总额高于此阈值的点
    threshold = 0  # 你需要设置这个值
    mask = total_tax_revenues > threshold

    ax.scatter(rs[mask], os[mask], asp[mask], c=total_tax_revenues[mask], cmap='viridis')

    curent_resident_space = backend.input_data.resident_space
    current_office_space = backend.input_data.office_space
    current_amenity_space = backend.input_data.amenity_space
    color = 'red'
    ax.scatter(curent_resident_space, current_office_space, current_amenity_space, c=color, s=100)
    
    ax.set_xlabel('Resident Space')
    ax.set_ylabel('Office Space')
    ax.set_zlabel('Amenity Space')
    ax.set_title('Tax Revenue by Parameter Value')

    plt.show()


    ## income tax is not a big part of the tax revenue
    # income_tax = 0.35 * taxable_income  

    
    # general business net income tax 8% in MA


    # personal property tax rate: 11.23/1000 in Cambridge 2022
    
    # residential tax exemptiom: 30%
    
# get tax revenue range 0-61921161
def test_tax_revenue_range():
    # 初始化变量来跟踪最小和最大税收值
    min_tax_revenue = float('inf')
    max_tax_revenue = float('-inf')

    # 使用嵌套循环来测试不同大小的空间组合
    for resident_space in np.linspace(0, 100000, 100):  # 这些数字只是示例，你可以根据实际情况调整
        for office_space in np.linspace(0, 100000, 100):
            for amenity_space in np.linspace(0, 100000, 100):
                current_tax_revenue = tax_revenue(resident_space, office_space, amenity_space)
                min_tax_revenue = min(min_tax_revenue, current_tax_revenue)
                max_tax_revenue = max(max_tax_revenue, current_tax_revenue)

    print(f"max tax revenue: {min_tax_revenue}")
    print(f"max tax revenue: {max_tax_revenue}")
    return min_tax_revenue, max_tax_revenue

def tax_revenue_to_index(tax_revenue, min_tax_revenue=0, max_tax_revenue=62000000):
    if tax_revenue < min_tax_revenue:
        return 0
    elif tax_revenue > max_tax_revenue:
        return 100
    else:
        return 100 * (tax_revenue - min_tax_revenue) / (max_tax_revenue - min_tax_revenue)

def cal_current_tax_revenue_index():
    score = 0
    return score

def cal_future_tax_revenue_index():
    score = tax_revenue_score(backend.input_data.resident_space, backend.input_data.office_space, backend.input_data.amenity_space)
    return score
# -----------------------------------------------------
def get_tax_LBO():
    unit = 10000
    value = unit * (LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum() +  backend.input_data.amenity_space)
    max = unit * ( backend.input_data.max_floor_area + LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum())
    min = unit * LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum()
    score = norm(value, max, min)
    return score

def get_tax_res():
    # personal income tax rate: 5% in MA
    unit = 5229 # MA data from https://taxadmin.memberclicks.net/2021-state-tax-revenue
    value = unit * (pop_num +  backend.input_data.resident_space/50)
    max =  unit * (pop_num +  backend.input_data.max_floor_area/50)
    min = unit * pop_num
    score = norm(value, max, min)
    return score

# def tax_dev():
#     income_tax = 0.35 * taxable_income

def get_tax_dev():
    value =  backend.input_data.floor_area
    max =  backend.input_data.max_floor_area
    min = 0
    score = norm(value, max, min)
    return score

def get_tax_IG():
    value =  backend.input_data.amenity_space
    max =  backend.input_data.max_floor_area
    min = 0
    score = norm(value, max, min)
    return score

def get_tax_work():
    value = work_num +  backend.input_data.office_space/200 +  backend.input_data.civic_space/200 +  backend.input_data.amenity_space/50
    max = work_num +  backend.input_data.max_floor_area/50
    min = work_num
    score = norm(value, max, min)
    return score

def get_manage_cost():
    value = LB_data[LB_data['stakeholder'] == 'GOV']['floor_area'].sum() +  backend.input_data.civic_space
    max = LB_data[LB_data['stakeholder'] == 'GOV']['floor_area'].sum() +  backend.input_data.max_floor_area
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
    value = police_area/ (pop_num +  backend.input_data.resident_space/50)
    max = police_area / pop_num
    min = police_area / (pop_num +  backend.input_data.max_floor_area/50)
    score = norm(value, max, min)
    return score

def get_access_police_work():
    police_area = 500
    value = police_area / (work_num +  backend.input_data.office_space/200 +  backend.input_data.civic_space/200 +  backend.input_data.amenity_space/50)
    max = police_area / work_num
    min = police_area / (work_num +  backend.input_data.max_floor_area/50)
    score = norm(value, max, min)
    return score

def compute_government():
    tax_revenue1 = {
        "target": 'Local Business Owners',
        "value": get_tax_LBO()
    }
    tax_revenue2 = {
        "target": 'Developer',
        "value": get_tax_dev()
    }
    tax_revenue3 = {
        "target": 'Industry Group',
        "value": get_tax_IG()
    }
    tax_revenue4 = {
        "target": 'Residents',
        "value": get_tax_res()
    }
    tax_revenue5 = {
        "target": 'Workforce',
        "value": get_tax_work()
    }
    manage_cost = {
        "target": 'Developer',
        "value": get_manage_cost()
    }
    safety_security1 = {
        "target": 'Residents',
        "value": get_access_police_res()
    }
    safety_security2 = {
        "target": 'Workforce',
        "value": get_access_police_work()
    }
    # safety_security3 = {
    #     "target": 'Local Business Owner',
    #     "value": round(random.uniform(0, 1), 2)
    # }
    # voting = {
    #     "target": 'Resident',
    #     "value": round(random.uniform(0, 1), 2)
    # }
    tax_revenue_score = get_before_after(
        cal_current_tax_revenue_index(),
        cal_future_tax_revenue_index()
    )
    finance_score = get_before_after(0, 0.2 * tax_revenue1['value'] + 0.2 * tax_revenue2['value'] + 0.2 * tax_revenue3['value'] + 0.1 * tax_revenue4['value'] + 0.1 * tax_revenue5['value'] - 0.2 *manage_cost['value'])
    safety_security_score = get_before_after(1, 0.5 * safety_security1['value'] + 0.5 * safety_security2['value'])
    # government_score = get_government_score() *100

    def get_government_score():
        weights = [1]
        scores_after = [
            tax_revenue_score['after'],
            # finance_score['after'], 
            # safety_security_score['after']
            ]
        scores_before = [
            tax_revenue_score['before'],
            # finance_score['before'],
            # safety_security_score['before']
            ]
        score_before = int(sum(w * s for w, s in zip(weights, scores_before)) / sum(weights))
        score_after = int(sum(w * s for w, s in zip(weights, scores_after)) / sum(weights))
        return score_before, score_after
    
    def get_government_radius():
        radius = get_government_score()[1]
        return radius
    
    def get_government_distance():
        distance = (get_government_score()[1] - get_government_score()[0]) * 2
        return distance



    # --------------------------------------------#
    # Data for chord chart: interaction
    # --------------------------------------------#
    score_gov = {
        "stakeholder": "Government",
        "score": get_government_score()[1],
        "radius": get_government_radius(),
        'distance': get_government_distance()
        }

    # --------------------------------------------#
    # Data for chord chart: interaction
    # --------------------------------------------#
    indicator_gov = [
        {"stakeholder": "Government", "indicator": "Tax revenue", "target": tax_revenue1["target"], "value": tax_revenue1["value"]},
        {"stakeholder": "Government", "indicator": "Tax revenue", "target": tax_revenue2["target"], "value": tax_revenue2["value"]},
        {"stakeholder": "Government", "indicator": "Tax revenue", "target": tax_revenue3["target"], "value": tax_revenue3["value"]},
        {"stakeholder": "Government", "indicator": "Tax revenue", "target": tax_revenue4["target"], "value": tax_revenue4["value"]},
        {"stakeholder": "Government", "indicator": "Tax revenue", "target": tax_revenue5["target"], "value": tax_revenue5["value"]},
        {"stakeholder": "Government", "indicator": "Management Cost", "target": manage_cost["target"], "value": manage_cost["value"]},
        {"stakeholder": "Government", "indicator": "Safety & security", "target": safety_security1["target"], "value": safety_security1["value"]},
        {"stakeholder": "Government", "indicator": "Safety & security", "target": safety_security2["target"], "value": safety_security2["value"]},
    ]

    # --------------------------------------------#
    # Data for indicator chart: indicator value
    # --------------------------------------------#
    index_gov = [
        {"stakeholder": "Government","indicator": "Tax revenue", "baseline": tax_revenue_score['before'],"score": tax_revenue_score['after']},
        # {"stakeholder": "Government","indicator": "Finance", "baseline": finance_score['before'],"score": finance_score['after']},
        # {"stakeholder": "Government","indicator": "Safety & security", "baseline": safety_security_score['before'],"score": safety_security_score['after']},
        ]
    
    return score_gov, indicator_gov, index_gov


# if __name__ == '__main__':
#     # tax_revenue_score(resident_space, office_space, amenity_space)
#     # test_tax_revenue()
#     # test_tax_revenue_range()
    
#     print("score_gov:", score_gov)
#     print("indicator_gov:", indicator_gov)
#     print("index_gov:", index_gov)