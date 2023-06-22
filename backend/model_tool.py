import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from pyproj import Transformer

import os
import json
import codecs

try:
    apply = apply
except NameError:
    def apply(f,*args,**kw):
        return f(*args,**kw)

# -----------------------------------------------------
"""
resident
%101% Single family - 4
%104% Two family - 8
%105% Three family - 12
%111% 4-8 units -24
%112% >8 units  -40
%121% Boarding house

Commercial

Office

#'Cemetery','Charitable/Religious','Government Operations',
#设施可用 -'Health','Higher Education','Education'，'Mixed Use Education'，'Privately-Owned Open Space'，'Public Open Space'，'Transportation'，Utilty
#空置 - 'Vacant Commercial'，'Vacant Industrial'，'Vacant Residential'

#resident
#'Assisted Living/Boarding House'
#'Education Residential'，'Residential'
#'Mixed Use Residential'

#Local business
#'Commercial'
#'Mixed Use Commercial'

#Industry group
#'Industrial'
#'Office'
#'Office/R&D'
"""
# -----------------------------------------------------
# Data Preparation
# -----------------------------------------------------
#读取数据
land_file = './data/CDD_LandUseKD.geojson'
building_file = './data/BASEMAP_BuildingsKD.geojson'
boundary_file ='./data/kendallsquare.geojson'
pop_file = './data/replica-residents_dataset.csv'
work_file = './data/replica-workforce_dataset.csv'
bgrp_file = './data/bgrp_cambridge.geojson'

def get_land_data(land_file):
    land_data = gpd.read_file(land_file)
    land_data = land_data.to_crs("EPSG:3857")
    land_data['ld_area_sqm'] = land_data.geometry.area
    land_data = land_data.to_crs("EPSG:4326")
    return land_data

def get_building_data(building_file):
    building_data = gpd.read_file(building_file)
    # 定义转换器，从 EPSG:4326 到 EPSG:3857
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
    # 转换图层的坐标参考系统
    building_data = building_data.to_crs("EPSG:3857")
    # 计算多边形的面积，并转换为平方米
    building_data['bu_area_sqm'] = building_data.geometry.area
    building_data = building_data.to_crs("EPSG:4326")
    return building_data

def get_boundary_data(boundary_file):
    boundary_data =gpd.read_file(boundary_file)
    return boundary_data

def get_population_data(pop_file):
    pop_data = pd.read_csv(pop_file)
    return pop_data

def get_workforce_data(work_file):
    work_data = pd.read_csv(work_file)
    return work_data

def get_bgrp_data(bgrp_file):
    bgrp_data = gpd.read_file(bgrp_file)
    return bgrp_data


# -----------------------------------------------------

# 按地块和用地类型分组，并计算建筑面积总和
def join_land_building():
    land_data = get_land_data(land_file)
    building_data = get_building_data(building_file)

    groupedLandBuilding_data = gpd.sjoin(land_data, building_data, op='intersects')

    # groupedLandBuilding_data['floor'] = np.floor(groupedLandBuilding_data['TOP_GL'] / 4.23)
    groupedLandBuilding_data['floor'] = np.floor(groupedLandBuilding_data['ELEV_GL'] / 4.23)
    #计算建筑面积
    groupedLandBuilding_data['floor_area'] = groupedLandBuilding_data['floor'] * groupedLandBuilding_data['bu_area_sqm']

    # calculate FAR
    groupedLandBuilding_data['FAR'] = groupedLandBuilding_data['floor_area'] / groupedLandBuilding_data['ld_area_sqm']

    columns = ['ML','Location','LandArea','LUCode','LUDesc','Category','ExistUnits','TYPE','BldgID','floor','floor_area','FAR','geometry']
    land_building = groupedLandBuilding_data[columns]

    return land_building

# -----------------------------------------------------
# VOLPE: ML= 29-50
# ML
# Location
# LandArea
# LUCode
# LUDesc
# Category
# ExistUnits
# TYPE
# BldgID
# building_area

# -----------------------------------------------------
# -----------------------------------------------------
# calculate the stakeholder number -1
# -----------------------------------------------------

def cal_stakeholder():
    LB_data = join_land_building().copy()
    LB_data = LB_data.reset_index(drop=True)
    LB_data['stakeholder'] = ''

    # select and label different 'stakeholder'
    LB_data.loc[LB_data['Category'].isin(
        ['Commercial', 'Mixed Use Commercial', 'Privately-Owned Open Space']), 'stakeholder'] = 'LBO'
    LB_data.loc[LB_data['Category'].isin(['Industrial', 'Office', 'Office/R&D']), 'stakeholder'] = 'IG'
    LB_data.loc[LB_data['Category'].isin(['Assisted Living/Boarding House', 'Education Residential', 'Residential',
                                          'Mixed Use Residential']), 'stakeholder'] = 'RS'
    LB_data.loc[LB_data['Category'].isin(
        ['Utility', 'Transportation', 'Government Operations', 'Public Open Space']), 'stakeholder'] = 'GOV'
    LB_data.loc[LB_data['Category'].isin(['Charitable/Religious', 'Higher Education']), 'stakeholder'] = 'NPI'
    LB_data.loc[LB_data['Category'].isin(['Vacant Commercial']), 'stakeholder'] = 'DEV'
    LB_data.loc[LB_data['ML'].isin(['29-50']), 'stakeholder'] = 'DEV'  # VOLPE LAND

    # get stakeholder pop_num from building area per capita
    LB_data['pop_num'] = 0
    LB_data.loc[LB_data['stakeholder'].isin(['LBO']), 'pop_num'] = LB_data[
                                                                       'floor_area'] / 40  # workforce 40 sqm/person
    LB_data.loc[LB_data['stakeholder'].isin(['IG']), 'pop_num'] = LB_data[
                                                                      'floor_area'] / 200  # workforce 200 sqm/person
    LB_data.loc[LB_data['stakeholder'].isin(['RS']), 'pop_num'] = LB_data[
                                                                      'floor_area'] / 50  # resident 50 sqm/person  US average
    LB_data.loc[LB_data['stakeholder'].isin(['GOV']), 'pop_num'] = LB_data[
                                                                        'floor_area'] / 200  # workforce 50 sqm/person
    LB_data.loc[LB_data['stakeholder'].isin(['NPI']), 'pop_num'] = LB_data[
                                                                        'floor_area'] / 200  # workforce 50 sqm/person

    return LB_data

def get_res_num():
    LB_data = cal_stakeholder()
    res_num = LB_data[LB_data['stakeholder']=='RS'].pop_num.sum()
    return res_num

def get_work_num():
    LB_data = cal_stakeholder()
    work_IG = LB_data[LB_data['stakeholder']=='IG'].pop_num.sum()
    work_LBO = LB_data[LB_data['stakeholder']=='LBO'].pop_num.sum()
    work_GOV = LB_data[LB_data['stakeholder']=='GOV'].pop_num.sum()
    work_NPI = LB_data[LB_data['stakeholder']=='NPI'].pop_num.sum()
    work_num = work_IG + work_LBO + work_GOV + work_NPI
    return work_num

# -----------------------------------------------------
# calculate the residents number -2
# -----------------------------------------------------
def count_pop_bgrp():
    pop = get_population_data(pop_file)
    bgrp = get_bgrp_data(bgrp_file)
    # 统计人口数据，bgrp level
    # 根据 'home_trct' 分组并计算每个地块的人数
    people_count = pop.groupby('home_bgrp').size().reset_index(name='count')
    # 合并 'bgrp' DataFrame 和 'people_count' DataFrame，根据 'home_trct' 进行匹配
    merged_pop = bgrp.merge(people_count, left_on='name', right_on='home_bgrp', how='left')

    return merged_pop

def get_residents_num():
    merged_data = count_pop_bgrp()
    # select the analysis area by bgrp
    bgrp_name = ['1 (Tract 3521.02, Middlesex, MA)','1 (Tract 3523, Middlesex, MA)','2 (Tract 3523, Middlesex, MA)','1 (Tract 3524, Middlesex, MA)',
                 '2 (Tract 3524, Middlesex, MA)', '1 (Tract 3526, Middlesex, MA)','2 (Tract 3531.01, Middlesex, MA)','2 (Tract 3531.02, Middlesex, MA)']
    bgrp_id = ['250173521021','250173523001','250173523002','250173524001','250173524002','250173526001','250173531012','250173531022']

    analysis_area = merged_data[merged_data['id'].isin(bgrp_id)]

    res_num = analysis_area['count'].sum()

    return res_num

# -----------------------------------------------------
# calculate the employees number
# -----------------------------------------------------
def count_work_bgrp():
    work = get_workforce_data(work_file)
    bgrp = get_bgrp_data(bgrp_file)
    # 统计人口数据，bgrp level
    # 根据 'work_trct' 分组并计算每个地块的人数
    work_count = work.groupby('work_bgrp').size().reset_index(name='count')
    # 合并 'bgrp' DataFrame 和 'people_count' DataFrame，根据 'home_trct' 进行匹配
    merged_data = bgrp.merge(work_count, left_on='name', right_on='work_bgrp', how='left')

    return merged_data

def get_workforce_num():
    merged_data = count_work_bgrp()
    # select the analysis area by bgrp
    bgrp_id = ['250173521021','250173523001','250173523002','250173524001','250173524002','250173526001','250173531012','250173531022']

    analysis_area = merged_data[merged_data['id'].isin(bgrp_id)]

    workforce_num = analysis_area['count'].sum()

    return workforce_num


def norm(data, max_value, min_value):
    normalized_value = (data - min_value) / (max_value - min_value)
    return normalized_value

def get_before_after(before,after):
    return {
        "before": before,
        "after": after
    }





# -----------------------------------------------------

def test():
    land_building = join_land_building(land_file, building_file)
    LB_data = cal_stakeholder(land_building)
    print(LB_data.head())
    print(LB_data['stakeholder'].value_counts())
    print(LB_data['pop_num'].sum())


if __name__ == '__main__':
    test()