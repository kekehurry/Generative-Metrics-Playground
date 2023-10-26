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

#------------------------------------------------------------
# Tax Revenue
#------------------------------------------------------------

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

def tax_revenue_to_index(tax_revenue, min_tax_revenue=0, max_tax_revenue=55736183):
    if tax_revenue < min_tax_revenue:
        return 0
    elif tax_revenue > max_tax_revenue:
        return 100
    else:
        return 100 * (tax_revenue - min_tax_revenue) / (max_tax_revenue - min_tax_revenue)

def test_tax_revenue():
    num_points = 10
    resident_space_range = np.linspace(0, 900000, num_points)
    office_space_range = np.linspace(0, 900000, num_points)
    amenity_space_range = np.linspace(0, 900000, num_points)
    
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

    scatter = ax.scatter(rs[mask], os[mask], asp[mask], c=total_tax_revenues[mask], cmap='viridis')

    curent_resident_space = backend.input_data.resident_space
    current_office_space = backend.input_data.office_space
    current_amenity_space = backend.input_data.amenity_space
    color = 'red'
    ax.scatter(curent_resident_space, current_office_space, current_amenity_space, c=color, s=100)
    
    ax.set_xlabel('Resident Space')
    ax.set_ylabel('Office Space')
    ax.set_zlabel('Amenity Space')
    ax.set_title('Tax Revenue by Parameter Value')
    
    # 添加色彩栏和图例
    fig.colorbar(scatter, ax=ax, label='Tax Revenue')
    ax.legend()

    plt.show()


    ## income tax is not a big part of the tax revenue
    # income_tax = 0.35 * taxable_income  

    
    # general business net income tax 8% in MA


    # personal property tax rate: 11.23/1000 in Cambridge 2022
    
    # residential tax exemptiom: 30%
    
# get tax revenue range 0-557540313
def test_tax_revenue_range():
    min_tax_revenue = float('inf')
    max_tax_revenue = float('-inf')
    
    # 用于存储所有的税收值，以便之后绘图
    all_tax_revenues = []
    
    for resident_space in np.linspace(0, 90000, 100):  # 修改这里的值以改变测试范围和精度
        for office_space in np.linspace(0, 90000, 100):
            for amenity_space in np.linspace(0, 90000, 100):
                current_tax_revenue = tax_revenue(resident_space, office_space, amenity_space)
                
                all_tax_revenues.append(current_tax_revenue)
                
                min_tax_revenue = min(min_tax_revenue, current_tax_revenue)
                max_tax_revenue = max(max_tax_revenue, current_tax_revenue)

    # 输出最小和最大税收值
    print(f"min tax revenue: {min_tax_revenue}")
    print(f"max tax revenue: {max_tax_revenue}")
    
    # 绘制税收值的直方图
    plt.figure(figsize=(10, 6))
    plt.hist(all_tax_revenues, bins=50, color='blue', alpha=0.7)  # bins 控制直方图的柱子数量
    plt.xlabel('Tax Revenue Value')
    plt.ylabel('Frequency')
    plt.title('Distribution of Tax Revenues for Different Parameter Combinations')
    plt.grid(True)
    plt.show()
    
    return min_tax_revenue, max_tax_revenue

def cal_current_tax_revenue_index():
    score = 0
    return score

def cal_future_tax_revenue_index():
    score = tax_revenue_score(backend.input_data.resident_space, backend.input_data.office_space, backend.input_data.amenity_space)
    return score

#------------------------------------------------------------
# Public Cost
#------------------------------------------------------------
def public_cost(resident_space, civic_space, green_space):
    ## 1. affordable housing cost
    ## we assume the affordable housing cost increase with the resident space increase
    ## 10% of the resident space is affordable housing
    res_develop_cost = 150 # $/sqft estimated value
    affordable_housing_cost = 0.1 * resident_space * 10.7639 * res_develop_cost
    ## 2. civic space cost
    civic_develop_cost = 200 # $/sqft estimated value
    civic_manage_cost = civic_space * 10.7639 * civic_develop_cost
    ## 3. green space cost
    ## green infrastructure cost: https://terrascope2024.mit.edu/?page_id=657
    ## average cost of green infrastructure: $85/sqft
    green_manage_cost = green_space * 10.7639 * 85
    
    # everage public cost
    public_cost = affordable_housing_cost + civic_manage_cost+ green_manage_cost
    return public_cost
    
def public_cost_score(resident_space, civic_space, green_space):
    total_public_cost = public_cost(resident_space, civic_space, green_space)
    public_score = public_cost_to_index(total_public_cost)
    # print("public_index:", public_score)
    return public_score

def test_public_cost():
    num_points = 20
    resident_space_range = np.linspace(0, 900000, num_points)
    civic_space_range = np.linspace(0, 900000, num_points)
    green_space_range = np.linspace(0, 30000, num_points)
    
    # 使用 meshgrid 函数创建一个 3D 参数网格
    rs, os, asp = np.meshgrid(resident_space_range, civic_space_range, green_space_range, indexing='ij')

    # 初始化一个用于存储税收总额的数组
    total_public_cost = np.zeros_like(rs)

    # 计算每一组参数对应的税收总额
    for i in range(num_points):
        for j in range(num_points):
            for k in range(num_points):
                total_public_cost[i, j, k] = public_cost_score(rs[i, j, k], os[i, j, k], asp[i, j, k])

    # 创建一个 3D 散点图来表示结果
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # 可以选择一个合适的阈值，仅绘制税收总额高于此阈值的点
    threshold = 0  # 你需要设置这个值
    mask = total_public_cost > threshold

    scatter = ax.scatter(rs[mask], os[mask], asp[mask], c=total_public_cost[mask], cmap='viridis')

    curent_resident_space = backend.input_data.resident_space
    current_civic_space = backend.input_data.civic_space
    current_green_space = backend.input_data.green_space
    color = 'red'
    ax.scatter(curent_resident_space, current_civic_space, current_green_space, c=color, s=50)
    
    ax.set_xlabel('Resident Space')
    ax.set_ylabel('Civic Space')
    ax.set_zlabel('Green Space')
    ax.set_title('Public Cost by Parameter Value')
    # 添加色彩栏和图例
    fig.colorbar(scatter, ax=ax, label='Public Cost')
    ax.legend()

    plt.show()

# get public cost range 0-213679278
def test_public_cost_range():
    # 初始化变量来跟踪最小和最大税收值
    min_public_cost = float('inf')
    max_public_cost = float('-inf')

    # 使用嵌套循环来测试不同大小的空间组合
    for resident_space in np.linspace(0, 900000, 100):  # 这些数字只是示例，你可以根据实际情况调整
        for civic_space in np.linspace(0, 900000, 200):
            for green_space in np.linspace(0, 30000, 100):
                current_tax_revenue = tax_revenue(resident_space, civic_space, green_space)
                min_public_cost = min(min_public_cost, current_tax_revenue)
                max_public_cost = max(max_public_cost, current_tax_revenue)

    print(f"min public cost: {min_public_cost}")
    print(f"max public cost: {max_public_cost}")
    return min_public_cost, max_public_cost

def public_cost_to_index(public_cost, min_public_cost=0, max_public_cost=220000000):
    if public_cost < min_public_cost:
        return 0
    elif public_cost > max_public_cost:
        return 100
    else:
        return 100 * (public_cost - min_public_cost) / (max_public_cost - min_public_cost)

def cal_current_public_cost_index():
    score = 0
    return score

def cal_future_public_cost_index(): 
    score = public_cost_score(backend.input_data.resident_space, backend.input_data.civic_space, backend.input_data.green_space)
    return score

#------------------------------------------------------------
# Tax Revenue / Public Cost
#------------------------------------------------------------
def revenue_cost_ratio(resident_space, office_space, amenity_space, civic_space, green_space):
    total_tax_revenue = tax_revenue(resident_space, office_space, amenity_space)
    total_public_cost = public_cost(resident_space, civic_space, green_space)
    # 处理特殊情况
    if total_public_cost == 0:
        return 0
    ratio = total_tax_revenue / total_public_cost
    return ratio

## get ratio range 0-166, but the change become smooth below 10
def test_ratio_range():
    ratios = []
    params = []

    # 使用嵌套循环来测试不同大小的空间组合
    for resident_space in np.linspace(0, 90000, 10):
        for office_space in np.linspace(0, 90000, 10):
            for amenity_space in np.linspace(0, 90000, 10):
                for civic_space in np.linspace(0, 90000, 10):
                    for green_space in np.linspace(0, 30000, 10):
                        current_ratio = revenue_cost_ratio(resident_space, office_space, amenity_space, civic_space, green_space)
                        ratios.append(current_ratio)
                        params.append((resident_space, office_space, amenity_space, civic_space, green_space))

    min_ratio = min(ratios)
    max_ratio = max(ratios)

    print(f"min ratio: {min_ratio}")
    print(f"max ratio: {max_ratio}")

    # 画出比率的散点图
    plt.figure(figsize=(10,6))
    plt.scatter(range(len(ratios)), ratios, c=ratios, cmap='viridis')
    plt.colorbar(label='Ratio Value')
    plt.xlabel('Parameter Combination Index')
    plt.ylabel('Ratio Value')
    plt.title('Scatter Plot of Ratio Values for Different Parameter Combinations')
    plt.show()

    return min_ratio, max_ratio

def ratio_to_index(ratio, min_ratio=0, max_ratio=10):
    if ratio < min_ratio:
        return 0
    elif ratio > max_ratio:
        return 100
    else:
        return norm(ratio, max_ratio, min_ratio)
    
def revenue_cost_ratio_score(resident_space, office_space, amenity_space, civic_space, green_space):
    ratio = revenue_cost_ratio(resident_space, office_space, amenity_space, civic_space, green_space)
    ratio_score = ratio_to_index(ratio)
    # print("ratio_index:", ratio_score)
    return ratio_score

def test_ratio():
    num_points = 20
    resident_space_range = np.linspace(0, 90000, num_points)
    office_space_range = np.linspace(0, 90000, num_points)
    amenity_space_range = np.linspace(0, 90000, num_points)
    
    # 使用 meshgrid 函数创建一个 3D 参数网格
    rs, os, asp = np.meshgrid(resident_space_range, office_space_range, amenity_space_range, indexing='ij')

    # 初始化一个用于存储税收总额的数组
    score = np.zeros_like(rs)

    # 计算每一组参数对应的税收总额
    for i in range(num_points):
        for j in range(num_points):
            for k in range(num_points):
                score[i, j, k] = revenue_cost_ratio_score(rs[i, j, k],  os[i, j, k], asp[i, j, k], 16520, 6118)

    # 创建一个 3D 散点图来表示结果
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # 可以选择一个合适的阈值，仅绘制税收总额高于此阈值的点
    threshold = 0  # 你需要设置这个值
    mask = score > threshold

    scatter = ax.scatter(rs[mask], os[mask], asp[mask], c=score[mask], cmap='viridis')

    curent_resident_space = backend.input_data.resident_space
    current_office_space = backend.input_data.office_space
    current_amenity_space = backend.input_data.amenity_space
    color = 'red'
    ax.scatter(curent_resident_space, current_office_space, current_amenity_space, c=color, s=50)
    
    ax.set_xlabel('Resident Space')
    ax.set_ylabel('Office Space')
    ax.set_zlabel('Amenity Space')
    ax.set_title('Revenue/Cost by Parameter Value')
    # 添加色彩栏和图例
    fig.colorbar(scatter, ax=ax, label='Score')
    ax.legend()

    plt.show()
    
def cal_current_ratio_index():
    score = 0
    return score

def cal_future_ratio_index():
    score = revenue_cost_ratio_score(backend.input_data.resident_space, backend.input_data.office_space, backend.input_data.amenity_space, backend.input_data.civic_space, backend.input_data.green_space)
    return score
    
# -----------------------------------------------------
def get_tax_LBO(amenity_space):
    unit = 10000
    value = unit * (LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum() + amenity_space)
    max = unit * ( backend.input_data.max_floor_area + LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum())
    min = unit * LB_data[LB_data['stakeholder'] == 'LBO']['floor_area'].sum()
    score = norm(value, max, min)
    return score

def get_tax_res(resident_space):
    # personal income tax rate: 5% in MA
    unit = 5229 # MA data from https://taxadmin.memberclicks.net/2021-state-tax-revenue
    value = unit * (pop_num + resident_space/50)
    max =  unit * (pop_num + backend.input_data.max_floor_area/50)
    min = unit * pop_num
    score = norm(value, max, min)
    return score

# def tax_dev():
#     income_tax = 0.35 * taxable_income

def get_tax_dev(floor_area):
    value =  floor_area
    max =  backend.input_data.max_floor_area
    min = 0
    score = norm(value, max, min)
    if score > 1:
        score = 1
    else:
        score = score
    return score

# def get_tax_IG(amenity_space):
#     value =  amenity_space
#     max =  backend.input_data.max_floor_area
#     min = 0
#     score = norm(value, max, min)
#     return score

def get_tax_work(office_space, civic_space, amenity_space):
    value = work_num + office_space/200 + civic_space/200 + amenity_space/50
    max = work_num +  backend.input_data.max_floor_area/50
    min = work_num
    score = norm(value, max, min)
    return score

def get_manage_cost(civic_space):
    value = LB_data[LB_data['stakeholder'] == 'GOV']['floor_area'].sum() + civic_space
    max = LB_data[LB_data['stakeholder'] == 'GOV']['floor_area'].sum() +  backend.input_data.max_floor_area
    min = LB_data[LB_data['stakeholder'] == 'GOV']['floor_area'].sum()
    score = norm(value, max, min)
    return score

# -----------------------------------------------------
# safety_security
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

def get_access_police_res(resident_space):
    police_area = 500
    value = police_area/ (pop_num + resident_space/50)
    max = police_area / pop_num
    min = police_area / (pop_num +  backend.input_data.max_floor_area/50)
    score = norm(value, max, min)
    if score > 1:
        score = 1
    else:
        score = score
    return score

def get_access_police_work(office_space, civic_space, amenity_space):
    police_area = 500
    value = police_area / (work_num + office_space/200 + civic_space/200 + amenity_space/50)
    max = police_area / work_num
    min = police_area / (work_num +  backend.input_data.max_floor_area/50)
    score = norm(value, max, min)
    if score > 1:
        score = 1
    else:
        score = score
    return score

def cal_current_safety_security():
    score = 0.5 * get_access_police_res(0) + 0.5 * get_access_police_work(0, 0, 0)
    return score

def cal_future_safety_security():
    score = 0.5 * get_access_police_res(backend.input_data.resident_space) + 0.5 * get_access_police_work(backend.input_data.office_space, backend.input_data.civic_space, backend.input_data.amenity_space)
    return score

# -----------------------------------------------------

def compute_government():
    # safety_security3 = {
    #     "target": 'Local Business Owner',
    #     "value": round(random.uniform(0, 1), 2)
    # }
    # voting = {
    #     "target": 'Resident',
    #     "value": round(random.uniform(0, 1), 2)
    # }
    tax_revenue_index = get_before_after(
        cal_current_tax_revenue_index(),
        cal_future_tax_revenue_index()
    )
    public_cost_index = get_before_after(
        cal_current_public_cost_index(),
        cal_future_public_cost_index()
    )
    revenue_cost_ratio_index = get_before_after(
        cal_current_ratio_index(),
        cal_future_ratio_index()
    )
        
    safety_security_score = get_before_after(
        cal_current_safety_security()*100, 
        cal_future_safety_security()*100
        )

    def get_government_score():
        weights = [0.5, 0.5]
        scores_after = [
            revenue_cost_ratio_index['after'],
            safety_security_score['after']
            ]
        scores_before = [
            revenue_cost_ratio_index['before'],
            safety_security_score['before']
            ]
        score_before = int(sum(w * s for w, s in zip(weights, scores_before)) / sum(weights))
        score_after = int(sum(w * s for w, s in zip(weights, scores_after)) / sum(weights))
        return score_before, score_after
    
    def get_government_radius():
        radius = get_government_score()[1]
        return radius
    
    def get_government_distance():
        # distance = (get_government_score()[1] - get_government_score()[0]) * 2
        distance = get_government_score()[1]
        return distance
    

    # --------------------------------------------#
    # Data for chord chart: interaction
    # --------------------------------------------#
    score_gov = {
        "stakeholder": "Government",
        "score": get_government_score()[1],
        "initial_score": get_government_score()[0],
        "radius": get_government_radius(),
        'distance': get_government_distance(),
        'best': 50
        }

    # --------------------------------------------#
    # Data for chord chart: interaction
    # --------------------------------------------#
    indicator_gov = [
        {"stakeholder": "Government", "indicator": "Tax revenue", "target": 'Local Business Owners', "value": get_tax_LBO(backend.input_data.amenity_space)},
        {"stakeholder": "Government", "indicator": "Tax revenue", "target": 'Developer', "value": get_tax_dev(backend.input_data.floor_area)},
        # {"stakeholder": "Government", "indicator": "Tax revenue", "target": 'Industry Group', "value": tax_revenue3["value"]},
        {"stakeholder": "Government", "indicator": "Tax revenue", "target": 'Residents', "value": get_tax_res(backend.input_data.resident_space)},
        {"stakeholder": "Government", "indicator": "Tax revenue", "target": 'Workforce', "value": get_tax_work(backend.input_data.office_space, backend.input_data.civic_space, backend.input_data.amenity_space)},
        {"stakeholder": "Government", "indicator": "Management Cost", "target": 'Developer', "value": cal_future_public_cost_index()/100},
        {"stakeholder": "Government", "indicator": "Safety & security", "target": 'Residents', "value": get_access_police_res(backend.input_data.resident_space)},
        {"stakeholder": "Government", "indicator": "Safety & security", "target": 'Workforce', "value": get_access_police_work(backend.input_data.office_space, backend.input_data.civic_space, backend.input_data.amenity_space)},
    ]

    # --------------------------------------------#
    # Data for indicator chart: indicator value
    # --------------------------------------------#
    index_gov = [
        {"stakeholder": "Government","indicator": "Tax revenue", "baseline": tax_revenue_index['before'],"score": tax_revenue_index['after']},
        {"stakeholder": "Government","indicator": "Public Cost", "baseline": public_cost_index['before'],"score": public_cost_index['after']},
        # {"stakeholder": "Government","indicator": "Finance", "baseline": finance_score['before'],"score": finance_score['after']},
        {"stakeholder": "Government","indicator": "Safety & security", "baseline": safety_security_score['before'],"score": safety_security_score['after']},
        ]
    
    # print("score_gov:", score_gov)
    # print("indicator_gov:", indicator_gov)
    # print("index_gov:", index_gov)
    
    return score_gov, indicator_gov, index_gov


# if __name__ == '__main__':
#     compute_government()
    # tax_revenue = tax_revenue(backend.input_data.resident_space, backend.input_data.office_space, backend.input_data.amenity_space)
    # public_cost = public_cost(backend.input_data.resident_space, backend.input_data.civic_space, backend.input_data.green_space)
    # print(tax_revenue)
    # print(public_cost)
    # print(tax_revenue/ public_cost)
    
    # tax_revenue_score(resident_space, office_space, amenity_space)
    # test_tax_revenue()
    # test_tax_revenue_range()

    # test_public_cost_range()
    # test_public_cost()
    
    # print(cal_future_tax_revenue_index())
    # print(cal_future_public_cost_index())
    
    # test_ratio_range()
    # test_ratio()
    
#     print("score_gov:", score_gov)
#     print("indicator_gov:", indicator_gov)
#     print("index_gov:", index_gov)