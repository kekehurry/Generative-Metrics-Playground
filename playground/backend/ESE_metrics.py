import pandas as pd
import numpy as np
import random

import sys
import os
current_directory = os.path.dirname(os.path.abspath(__file__))
project_directory = os.path.join(current_directory, '..')
sys.path.append(project_directory)

# sys.path.append('/Users/majue/Documents/MIT/multi_stakeholders_indicator_d3')
from backend.model_tool import *
import backend.input_data
import requests

import warnings

warnings.filterwarnings("ignore", category=FutureWarning)


# Economic nested classes

class Employment:
    def __init__(self, office_space, amenity_space, civic_space):
        self.office_space = office_space
        self.amenity_space = amenity_space
        self.civic_space = civic_space

        self.current_employment_score = self.get_employment_score(self.get_current_unemployment_rate(), self.get_current_job_creation())
        self.future_employment_score = self.get_employment_score(self.get_future_unemployment_rate(), self.get_future_job_creation())

    def get_current_unemployment_rate(self):
        current_rate = (4.91 + 4.91 + 5.7 +5.7) / 4  # data from census
        value = norm(current_rate, 5.7, 4.91)
        return 1-value

    def get_future_unemployment_rate(self): # should be improved
        random_number = round(random.uniform(4.91, 5.7), 2)  # now the future unemployment rate is randomly generated

        value = norm(random_number, 5.7, 4.91)
        return 1-value

    def get_local_job_creation(self):
        office_job = self.office_space /200
        amenity_job = self.amenity_space /50
        civic_job = self.civic_space /50
        local_job_creation = office_job + amenity_job + civic_job

        return local_job_creation

    def get_current_job_creation(self):
        VOLPE_area = 30593
        max_FAR = 3.25 # from cambridge zoning regulation https://www.cambridgema.gov/~/media/Files/CDD/ZoningDevel/zoningguide/zguide.ashx
        max_value = VOLPE_area * max_FAR / 50
        norm_value = norm(0, max_value , 0)
        return norm_value

    def get_future_job_creation(self):
        VOLPE_area = 30593
        max_FAR = 3.25 # from cambridge zoning regulation https://www.cambridgema.gov/~/media/Files/CDD/ZoningDevel/zoningguide/zguide.ashx
        max_value = VOLPE_area * max_FAR / 50
        norm_value = norm(self.get_local_job_creation(), max_value , 0)
        return norm_value

    def get_employment_score(self, normalize_local_job_creation, normalize_unemployment_rate):
        score = 0.5 * normalize_local_job_creation + 0.5 * normalize_unemployment_rate
        score = round(score, 2)
        return round(score, 2)


# class Equity:
#     def __init__(self, resident_space, VOLPE_area):
#         self.resident_space = resident_space
#         self.VOLPE_area = 30593

#         self.current_equity_score = self.get_equity_score(self.get_current_affordability(), self.get_current_cost_of_housing())
#         self.future_equity_score = self.get_equity_score(self.get_future_affordability(), self.get_future_cost_of_housing())

#     def get_current_affordability(self):
#         value = 0.1
#         return value
#         # return value

#     def get_future_affordability(self):
#         # 25 % of the new housing will be below market rate, with 20% inclusionary housing and 5% middle income housing (https://courbanize.com/projects/kendall-sq-urban-renewal/information)
#         value = (0.1 * self.VOLPE_area + 0.25 * self.resident_space)/self.VOLPE_area
#         return value

#     def get_current_cost_of_housing(self):
#         score = (148 + 171 + 135 + 137) / 4  # data from https://www.city-data.com/neighborhood/Kendall-Square-Cambridge-MA.html
#         value = norm(score, 171, 135)
#         return value

#     def get_future_cost_of_housing(self): # should be improved
#         score = round(random.uniform(135* (1- self.resident_space/max_floor_area), 135), 2)  # now it is randomly generated
#         value = norm(score, 171, 0)
#         return value

#     def get_equity_score(self, normalize_affordability, normalize_cost_of_housing):
#         score = 0.5 * normalize_affordability + 0.5 * normalize_cost_of_housing
#         score = round(score, 2)
#         return round(score, 2)

class Income:
    def __init__(self):
        self.current_income_score = self.get_income_score(self.get_current_mdi())
        self.future_income_score = self.get_income_score(self.get_future_mdi())
    #     median household income

    def get_current_mdi(self):
        score = (79917 + 162708 + 140682 + 65804)/4  # data from https://www.city-data.com/neighborhood/Kendall-Square-Cambridge-MA.html
        value = norm(score, 162708, 65804)
        return value

    def get_future_mdi(self):
        value = self.get_current_mdi() * 1.1
        return value

    def get_income_score(self, normalize_mdi):
        score = normalize_mdi
        score = round(score, 2)
        return round(score, 2)

class Innovation:
    def __init__(self, office_space):
        self.office_space = office_space

        self.current_innovation_score = self.get_innovation_score(self.get_current_creative(),
                                                          self.get_current_research())
        self.future_innovation_score = self.get_innovation_score(self.get_future_creative(),
                                                         self.get_future_research())

    def get_current_creative(self):
        LB_data = cal_stakeholder()
        work_num = get_work_num()
        create_num = LB_data[LB_data['Category'] == 'Office/R&D'].pop_num.sum()
        value = create_num / work_num
        norm_value = norm(value, 1, 0)
        return norm_value
        # return value

    def get_future_creative(self):
        LB_data = cal_stakeholder()
        work_num = get_work_num() + self.office_space / 200
        create_num = LB_data[LB_data['Category'] == 'Office/R&D'].pop_num.sum() + self.office_space * 20 / 200 # 20% Office/R&D
        value = create_num / work_num
        norm_value = norm(value, 1, 0)
        return norm_value

    def get_current_research(self):
        value = 0
        return value

    def get_future_research(self):
        value = 0
        return value

    def get_innovation_score(self, normalize_creative, normalize_research):
        score = 1 * normalize_creative + 0 * normalize_research
        score = round(score, 2)
        return round(score, 2)

class AttractivenessCompetitiveness:
    def __init__(self):
        self.current_AC_score = self.get_AC_score(self.get_current_congestion(),
                                                          self.get_current_public(),
                                                          self.get_current_population(),
                                                            self.get_current_tourism(),
                                                            self.get_current_visitor(),
                                                            self.get_current_travel_time())
        self.future_AC_score = self.get_AC_score(self.get_future_congestion(),
                                                            self.get_future_public(),
                                                            self.get_future_population(),
                                                            self.get_future_tourism(),
                                                            self.get_future_visitor(),
                                                            self.get_future_travel_time())

    def get_current_congestion(self):
        value = 0
        return value

    def get_future_congestion(self):
        value = 0
        return value

    def get_current_public(self):
        value = 0
        return value

    def get_future_public(self):
        value = 0
        return value

    def get_current_population(self):
        value = 0
        return value

    def get_future_population(self):
        value = 0
        return value

    def get_current_tourism(self):
        value = 0
        return value

    def get_future_tourism(self):
        value = 0
        return value

    def get_current_visitor(self):
        value = 0
        return value

    def get_future_visitor(self):
        value = 0
        return value

    def get_current_travel_time(self):
        value = 0
        return value

    def get_future_travel_time(self):
        value = 0
        return value

    def get_AC_score(self, normalize_congestion, normalize_public, normalize_population, normalize_tourism, normalize_visitor, normalize_travel_time):
        score = 0.2 * normalize_congestion + 0.2 * normalize_public + 0.2 * normalize_population + 0.2 * normalize_tourism + 0.1 * normalize_visitor + 0.1 * normalize_travel_time
        score = round(score, 2)
        return round(score, 2)

class BuildUpArea:
    def __init__(self, floor_area):
        self.floor_area = floor_area

        self.current_build_up_score = self.get_build_up_score(self.get_current_built_area())
        self.future_build_up_score = self.get_build_up_score(self.get_future_built_area())

    def get_current_built_area(self):
        value = 0
        return value

    def get_future_built_area(self):
        max_floor_area=99427
        area = self.floor_area
        value = norm(area, max_floor_area , 0)
        return value

    def get_build_up_score(self, normalize_built_area):
        score = normalize_built_area
        score = round(score, 2)
        return round(score, 2)

class Displacement:
    def __init__(self, floor_area, amenity_space, resident_space):
        self.amenity_space = amenity_space
        self.resident_space = resident_space
        self.floor_area = floor_area

        self.current_displacement_score = self.get_displacement_score(self.get_current_business(),self.get_current_resident())
        self.future_displacement_score = self.get_displacement_score(self.get_future_business(),self.get_future_resident())

    def get_current_business(self):
        LB_data = cal_stakeholder()
        business = LB_data[LB_data['Category'] == 'LBO'].floor_area.sum()
        all = LB_data.floor_area.sum()
        ratio = business / all
        value = norm(ratio, 1, 0)
        return value

    def get_future_business(self):
        LB_data = cal_stakeholder()
        business = LB_data[LB_data['Category'] == 'LBO'].floor_area.sum() + self.amenity_space
        all = LB_data.floor_area.sum() + self.floor_area
        ratio = business / all
        max = (LB_data[LB_data['Category'] == 'LBO'].floor_area.sum() +self.floor_area) / all
        value = norm(ratio, max, 0)
        return value

    def get_current_resident(self):
        LB_data = cal_stakeholder()
        resident = LB_data[LB_data['Category'] == 'RS'].floor_area.sum()
        all = LB_data.floor_area.sum()
        ratio = resident / all
        value = norm(ratio, 1, 0)
        return value

    def get_future_resident(self):
        LB_data = cal_stakeholder()
        resident = LB_data[LB_data['Category'] == 'RS'].floor_area.sum() + self.resident_space
        all = LB_data.floor_area.sum() + self.floor_area
        ratio = resident / all
        max = (LB_data[LB_data['Category'] == 'RS'].floor_area.sum() + self.floor_area) / all
        value = norm(ratio, max, 0)
        return value

    def get_displacement_score(self, normalize_business, normalize_resident):
        score = 0.5 * normalize_business + 0.5 * normalize_resident
        score = round(score, 2)
        return round(score, 2)

class ProfitConstruction:
    def __init__(self, floor_area, resident_space, amenity_space, office_space):
        self.resident_space = resident_space
        self.amenity_space = amenity_space
        self.office_space = office_space
        self.floor_area = floor_area

        self.current_profit_score = self.get_profit_score(self.get_current_profit())
        self.future_profit_score = self.get_profit_score(self.get_future_profit())

    def get_current_profit(self):
        value = round(random.uniform(0, 1), 2)
        return value

    def get_future_profit(self):
        value = self.resident_space * 0.4 + self.amenity_space * 0.5 + self.office_space * 0.8
        max = self.floor_area * 0.8
        value = norm(value, max, 0)
        return value

    def get_profit_score(self, normalize_profit):
        score = normalize_profit
        return round(score, 2)

class Economic:
    def __init__(self):
        self.employment = Employment(backend.input_data.office_space, backend.input_data.amenity_space, backend.input_data.civic_space)
        # self.equity = Equity(backend.input_data.resident_space)
        self.income = Income()
        self.innovation = Innovation(backend.input_data.office_space)
        self.attractive_competitive = AttractivenessCompetitiveness()
        self.build_up_area = BuildUpArea(backend.input_data.floor_area)
        self.displacement = Displacement(backend.input_data.floor_area, backend.input_data.amenity_space, backend.input_data.resident_space)
        self.profit_construction = ProfitConstruction(backend.input_data.floor_area, backend.input_data.resident_space, backend.input_data.amenity_space, backend.input_data.office_space)
        # self._preprocess(data)

    # def _preprocess(self, data):
    #     data.fillna(0, inplace=True)
    #
    # def get_statistics(self):
    #     return self.data.describe()

# Environmental nested classes

class Pollution:
    def __init__(self,floor_area):
        self.floor_area = floor_area

        self.current_pollution_score = self.get_pollution_score(self.get_current_air_quality(), self.get_current_noise_pollution())
        self.future_pollution_score = self.get_pollution_score(self.get_future_air_quality(), self.get_future_noise_pollution())

    def get_current_air_quality(self):
        value = 29.73 # AQI get from https://www.city-data.com/neighborhood/Kendall-Square-Cambridge-MA.html
        value = norm(value, 100, 0)
        return value

    def get_future_air_quality(self):
        value = 29.73
        value = norm(value, 100, 0)
        return value

    def get_current_noise_pollution(self):
        value = (12.14 + 14.58 + 12.14 + 10.75)/4
        value = norm(value, 14.58, 10.75)
        return value

    def get_future_noise_pollution(self):
        VOLPE_area = 30593
        value = (12.14 + 14.58 + 12.14 + 10.75)/4 + (self.floor_area/VOLPE_area)
        value = norm(value, 14.58, 10.75)
        return value

    def get_pollution_score(self, normalize_air_quality, normalize_noise_pollution):
        score = 0.5 * normalize_air_quality + 0.5 * normalize_noise_pollution
        score = round(score, 2)
        return round(score, 2)


class Ecosystem:
    def __init__(self, civic_space, floor_area):
        self.civic_space = civic_space
        self.floor_area = floor_area

        self.current_ecosystem_score = self.get_ecosystem_score(self.get_current_green_space())
        self.future_ecosystem_score = self.get_ecosystem_score(self.get_future_green_space())

    def get_current_green_space(self):
        LB_data = cal_stakeholder()
        green_space = LB_data[LB_data['Category'] == 'Public Open Space'].floor_area.sum()
        value = green_space / LB_data.floor_area.sum() * 10
        return value

    def get_future_green_space(self):
        LB_data = cal_stakeholder()
        green_space = LB_data[LB_data['Category'] == 'Public Open Space'].floor_area.sum() + self.civic_space/2
        value = green_space / (LB_data.floor_area.sum() + self.floor_area) * 10
        return value

    def get_ecosystem_score(self, normalize_green_space):
        score = normalize_green_space
        return round(score, 2)

class PublicService:
    def __init__(self, civic_space, floor_area):
        self.civic_space = civic_space
        self.floor_area = floor_area

        self.current_public_service_score = self.get_public_service_score(self.get_current_public_service())
        self.future_public_service_score = self.get_public_service_score(self.get_future_public_service())

    def get_current_public_service(self):
        LB_data = cal_stakeholder()
        public_service = LB_data[LB_data['Category'] == 'Utility'].floor_area.sum() + LB_data[LB_data['Category'] == 'Government Operations'].floor_area.sum()
        value = public_service / LB_data.floor_area.sum() * 10
        return value

    def get_future_public_service(self):
        LB_data = cal_stakeholder()
        public_service = LB_data[LB_data['Category'] == 'Utility'].floor_area.sum() + LB_data[LB_data['Category'] == 'Government Operations'].floor_area.sum() + self.civic_space
        value = public_service / (LB_data.floor_area.sum() + self.floor_area) * 10
        return value

    def get_public_service_score(self, normalize_public_service):
        score = normalize_public_service
        return round(score, 2)

class Energy:
    def __init__(self):
        self.current_energy_score = self.get_energy_score(self.get_current_emission_mobility(), self.get_current_emission_building())
        self.future_energy_score = self.get_energy_score(self.get_future_emission_mobility(), self.get_future_emission_building())

    def get_current_emission_mobility(self):
        value = 0.5
        return value

    def get_future_emission_mobility(self):
        value = 0.5
        return value

    def get_current_emission_building(self):
        value = 1
        return value

    def get_future_emission_building(self):
        LB_data = cal_stakeholder()
        num_building = len(LB_data[LB_data['floor_area'] != 0 ]) + 1
        value = num_building/ (num_building - 1)
        value = norm(value, 1, 0)
        return value

    def get_energy_score(self, normalize_emission_mobility, normalize_emission_building):
        score = 0.5 * normalize_emission_mobility + 0.5 * normalize_emission_building
        score = round(score, 2)
        return round(score, 2)


class Land:
    def __init__(self):
        self.current_land_score = self.get_land_score(self.get_current_land())
        self.future_land_score = self.get_land_score(self.get_future_land())

    def get_current_land(self):
        value = 0.5
        return value

    def get_future_land(self):
        value = 0.5
        return value

    def get_land_score(self, normalize_land):
        score = normalize_land
        return round(score, 2)


class Environmental:
    def __init__(self):
        self.pollution = Pollution(backend.input_data.floor_area)
        self.ecosystem = Ecosystem(backend.input_data.civic_space, backend.input_data.floor_area)
        self.public_service = PublicService(backend.input_data.civic_space, backend.input_data.floor_area)
        self.energy = Energy()
        self.land = Land()
        # self._preprocess(data)

    # def _preprocess(self, data):
    #     data.fillna(0, inplace=True)
    #
    # def get_statistics(self):
    #     return self.data.describe()

# Social nested classes

class Health:
    def __init__(self):
        self.current_health_score = self.get_health_score(self.get_current_health())
        self.future_health_score = self.get_health_score(self.get_future_health())

    def get_current_health(self):
        value = 0.5
        return value

    def get_future_health(self):
        value = 0.5
        return value

    def get_health_score(self, normalize_health):
        score = normalize_health
        return round(score, 2)


class SafetySecurity:
    def __init__(self):
        self.current_safety_security_score = self.get_safety_security_score(self.get_current_traffic_accidents(), self.get_current_crime_rate())
        self.future_safety_security_score = self.get_safety_security_score(self.get_future_traffic_accidents(), self.get_future_crime_rate())

    def get_current_traffic_accidents(self):
        value = 0.5
        return value

    def get_future_traffic_accidents(self):
        value = 0.5
        return value

    def get_current_crime_rate(self):
        value = 0.5
        return value

    def get_future_crime_rate(self):
        value = 0.5
        return value

    def get_safety_security_score(self, normalize_traffic_accidents, normalize_crime_rate):
        score = 0.5 * normalize_traffic_accidents + 0.5 * normalize_crime_rate
        return round(score, 2)

class AccessToService:
    def __init__(self):
        self.current_access_to_service_score = self.get_access_to_service_score(self.get_current_access_to_transport(), self.get_current_access_to_sharing(), self.get_current_access_to_public_amenities(), self.get_current_access_to_commercial_amenities())
        self.future_access_to_service_score = self.get_access_to_service_score(self.get_future_access_to_transport(), self.get_future_access_to_sharing(), self.get_future_access_to_public_amenities(), self.get_future_access_to_commercial_amenities())

    def get_current_access_to_transport(self):
        value = 0.5
        return value

    def get_future_access_to_transport(self):
        value = round(random.uniform(0, 1), 2)
        return value

    def get_current_access_to_sharing(self):
        value = round(random.uniform(0, 1), 2)
        return value

    def get_future_access_to_sharing(self):
        value = round(random.uniform(0, 1), 2)
        return value

    def get_current_access_to_public_amenities(self):
        value = round(random.uniform(0, 1), 2)
        return value

    def get_future_access_to_public_amenities(self):
        value = round(random.uniform(0, 1), 2)
        return value

    def get_current_access_to_commercial_amenities(self):
        value = round(random.uniform(0, 1), 2)
        return value

    def get_future_access_to_commercial_amenities(self):
        value = round(random.uniform(0, 1), 2)
        return value

    def get_access_to_service_score(self, normalize_access_to_transport, normalize_access_to_sharing, normalize_access_to_public_amenities, normalize_access_to_commercial_amenities):
        score = 0.25 * normalize_access_to_transport + 0.25 * normalize_access_to_sharing + 0.25 * normalize_access_to_public_amenities + 0.25 * normalize_access_to_commercial_amenities
        return round(score, 2)

class Education:
    def __init__(self):
        self.current_education_score = self.get_education_score(self.get_current_educational())
        self.future_education_score = self.get_education_score(self.get_future_educational())

    def get_current_educational(self):
        value = round(random.uniform(0, 1), 2)
        return value

    def get_future_educational(self):
        value = round(random.uniform(0, 1), 2)
        return value

    def get_education_score(self, normalize_educational):
        score = normalize_educational
        return round(score, 2)

class Housing:
    def __init__(self):
        self.current_housing_score = self.get_housing_score(self.get_current_diversity_of_housing(), self.get_current_preservation_of_cultural_heritage(), self.get_current_ground_floor_usage(), self.get_current_public_outdoor_recreation_space(), self.get_current_green_space())
        self.future_housing_score = self.get_housing_score(self.get_future_diversity_of_housing(), self.get_future_preservation_of_cultural_heritage(), self.get_future_ground_floor_usage(), self.get_future_public_outdoor_recreation_space(), self.get_future_green_space())

    def get_current_diversity_of_housing(self):
        value = round(random.uniform(0, 1), 2)
        return value

    def get_future_diversity_of_housing(self):
        value = round(random.uniform(0, 1), 2)
        return value

    def get_current_preservation_of_cultural_heritage(self):
        value = round(random.uniform(0, 1), 2)
        return value

    def get_future_preservation_of_cultural_heritage(self):
        value = round(random.uniform(0, 1), 2)
        return value

    def get_current_ground_floor_usage(self):
        value = round(random.uniform(0, 1), 2)
        return value

    def get_future_ground_floor_usage(self):
        value = round(random.uniform(0, 1), 2)
        return value

    def get_current_public_outdoor_recreation_space(self):
        value = round(random.uniform(0, 1), 2)
        return value

    def get_future_public_outdoor_recreation_space(self):
        value = round(random.uniform(0, 1), 2)
        return value

    def get_current_green_space(self):
        value = round(random.uniform(0, 1), 2)
        return value

    def get_future_green_space(self):
        value = round(random.uniform(0, 1), 2)
        return value

    def get_housing_score(self, normalize_diversity_of_housing, normalize_preservation_of_cultural_heritage, normalize_ground_floor_usage, normalize_public_outdoor_recreation_space, normalize_green_space):
        score = 0.2 * normalize_diversity_of_housing + 0.2 * normalize_preservation_of_cultural_heritage + 0.2 * normalize_ground_floor_usage + 0.2 * normalize_public_outdoor_recreation_space + 0.2 * normalize_green_space
        return round(score, 2)

class SocialExposure:
    def __init__(self):
        self.current_social_exposure_score = self.get_social_exposure_score(self.get_current_exposure())
        self.future_social_exposure_score = self.get_social_exposure_score(self.get_future_exposure())

    def get_current_exposure(self):
        value = round(random.uniform(0, 1), 2)
        return value

    def get_future_exposure(self):
        value = round(random.uniform(0, 1), 2)
        return value

    def get_social_exposure_score(self, normalize_exposure):
        score = normalize_exposure
        return round(score, 2)

class Density:
    def __init__(self):
        self.current_density_score = self.get_density_score(self.get_current_population_density(), self.get_current_building_density())
        self.future_density_score = self.get_density_score(self.get_future_population_density(), self.get_future_building_density())

    def get_current_population_density(self):
        value = round(random.uniform(0, 1), 2)
        return value

    def get_future_population_density(self):
        value = round(random.uniform(0, 1), 2)
        return value

    def get_current_building_density(self):
        value = round(random.uniform(0, 1), 2)
        return value

    def get_future_building_density(self):
        value = round(random.uniform(0, 1), 2)
        return value

    def get_density_score(self, normalize_population_density, normalize_building_density):
        score = 0.5 * normalize_population_density + 0.5 * normalize_building_density
        return round(score, 2)

class JobHousing:
    def __init__(self):
        self.current_job_housing_score = self.get_job_housing_score(self.get_current_job_housing_ratio())
        self.future_job_housing_score = self.get_job_housing_score(self.get_future_job_housing_ratio())

    def get_current_job_housing_ratio(self):
        value = round(random.uniform(0, 1), 2)
        return value

    def get_future_job_housing_ratio(self):
        value = round(random.uniform(0, 1), 2)
        return value

    def get_job_housing_score(self, normalize_job_housing_ratio):
        score = normalize_job_housing_ratio
        return round(score, 2)

class Social:
    def __init__(self):
        self.health = Health()
        self.safety_security = SafetySecurity()
        self.access_to_service = AccessToService()
        self.education = Education()
        self.housing = Housing()
        self.social_exposure = SocialExposure()
        self.density = Density()
        self.job_housing = JobHousing()
        # self._preprocess(data)
    #
    # def _preprocess(self, data):
    #     data.fillna(0, inplace=True)
    #
    # def get_statistics(self):
    #     return self.data.describe()

#--------------------------------------------#
# Test
#--------------------------------------------#

# output format：
# -------------------------------------------#
# category          indicator               baseline        value
#
#  economic         employment              5              10
#  economic         equity                  5              6
#  social           safety_security         5              7
#  social           access_to_service       5              3
#  environmental    pollution               5              5
#  environmental    ecosystem               5              2
# -------------------------------------------#



def ese_test():
    economic = Economic()
    environmental = Environmental()
    social = Social()

    # Create a list of dictionaries for storing the information
    #  data[0] for baseline value / data[1] for simulated value
    data = [[{"category": "Economic", "indicator": "Employment", "value": economic.employment.current_employment_score},
        # {"category": "Economic", "indicator": "Equity", "value": economic.equity.current_equity_score},
        {"category": "Economic", "indicator": "Income", "value": economic.income.current_income_score},
        {"category": "Economic", "indicator": "Innovation", "value": economic.innovation.current_innovation_score},
        {"category": "Economic", "indicator": "Attractiv & Competitive", "value": economic.attractive_competitive.current_AC_score},
        {"category": "Economic", "indicator": "Build up area", "value": economic.build_up_area.current_build_up_score},
        {"category": "Economic", "indicator": "Displacement", "value": economic.displacement.current_displacement_score},
        {"category": "Economic", "indicator": "ProfitConstruction", "value": economic.profit_construction.current_profit_score},
        {"category": "Environmental", "indicator": "Pollution", "value": environmental.pollution.current_pollution_score},
        {"category": "Environmental", "indicator": "Ecosystem", "value": environmental.ecosystem.current_ecosystem_score},
        {"category": "Environmental", "indicator": "Public Service", "value": environmental.public_service.current_public_service_score},
        {"category": "Environmental", "indicator": "Energy", "value": environmental.energy.current_energy_score},
        {"category": "Environmental", "indicator": "Land", "value": environmental.land.current_land_score},
        {"category": "Social", "indicator": "Health", "value": social.health.current_health_score},
        {"category": "Social", "indicator": "Safety & Security", "value": social.safety_security.current_safety_security_score},
        {"category": "Social", "indicator": "Access to Service", "value": social.access_to_service.current_access_to_service_score},
        {"category": "Social", "indicator": "Education", "value": social.education.current_education_score},
        {"category": "Social", "indicator": "Housing", "baseline": social.housing.current_housing_score},
        {"category": "Social", "indicator": "Social Exposure", "value": social.social_exposure.current_social_exposure_score},
        {"category": "Social", "indicator": "Density", "value": social.density.current_density_score},
        {"category": "Social", "indicator": "Job Housing", "value": social.job_housing.current_job_housing_score}],
        [{"category": "Economic", "indicator": "Employment", "value": economic.employment.future_employment_score},
        # {"category": "Economic", "indicator": "Equity", "value": economic.equity.future_equity_score},
        {"category": "Economic", "indicator": "Income", "value": economic.income.future_income_score},
        {"category": "Economic", "indicator": "Innovation", "value": economic.innovation.future_innovation_score},
        {"category": "Economic", "indicator": "Attractiv & Competitive", "value": economic.attractive_competitive.future_AC_score},
        {"category": "Economic", "indicator": "Build up area", "value": economic.build_up_area.future_build_up_score},
        {"category": "Economic", "indicator": "Displacement", "value": economic.displacement.future_displacement_score},
        {"category": "Economic", "indicator": "ProfitConstruction", "value": economic.profit_construction.future_profit_score},
        {"category": "Environmental", "indicator": "Pollution", "value": environmental.pollution.future_pollution_score},
        {"category": "Environmental", "indicator": "Ecosystem", "value": environmental.ecosystem.future_ecosystem_score},
        {"category": "Environmental", "indicator": "Public Service", "value": environmental.public_service.future_public_service_score},
        {"category": "Environmental", "indicator": "Energy", "value": environmental.energy.future_energy_score},
        {"category": "Environmental", "indicator": "Land", "value": environmental.land.future_land_score},
        {"category": "Social", "indicator": "Health", "value": social.health.future_health_score},
        {"category": "Social", "indicator": "Safety & Security", "value": social.safety_security.future_safety_security_score},
        {"category": "Social", "indicator": "Access to Service", "value": social.access_to_service.future_access_to_service_score},
        {"category": "Social", "indicator": "Education", "value": social.education.future_education_score},
        {"category": "Social", "indicator": "Housing", "value": social.housing.future_housing_score},
        {"category": "Social", "indicator": "Social Exposure", "value": social.social_exposure.future_social_exposure_score},
        {"category": "Social", "indicator": "Density", "value": social.density.future_density_score},
        {"category": "Social", "indicator": "Job Housing", "value": social.job_housing.future_job_housing_score}]]

    # Print the information in the desired format
    # print(f"{'category':<15} {'indicator':<20} {'baseline'} {'value'}")
    # for row in data:
    #     print(f"{row['category']:<15} {row['indicator']:<20} {row['baseline']} {row['value']}")
    # print(data)
    console_log(f"ESE data updated!")
    print('ESE data updated')

    # Create a dataframe for storing the information
    # df = pd.DataFrame(data)
    # save dataframe to csv file
    # output_file = os.path.abspath("./backend/output/radar_data.csv")
    # df.to_csv(output_file, index=False)
    
    # Convert data to JSON format
    data_json = json.dumps(data)
    send_to_api(data_json, "radar_data")


    # print(environmental.pollution.air_quality)
    # print(environmental.get_statistics())
    #
    # social = Social("social.csv")
    # print(social.safety_security.traffic_accidents)
    # print(social.get_statistics())
    
def send_to_api(data_json, filename):
    # Define the API endpoint (assuming Flask app is running on localhost:5000)
    api_url = f'http://127.0.0.1:5001/api/save_data/{filename}'
    # Use the POST method to send data
    response = requests.post(api_url, data=data_json, headers={'Content-Type': 'application/json'})

    # Check the response
    if response.status_code == 200:
        console_log(f"Data successfully sent to API for {filename}!")
        print(f"Data successfully sent to API for {filename}!")
    else:
        print(f"Failed to send data for {filename}. Status code: {response.status_code}, Response: {response.text}")
        
def console_log(message):
    print("[CONSOLE.LOG]", message)
    
if __name__ == '__main__':
    ese_test()
