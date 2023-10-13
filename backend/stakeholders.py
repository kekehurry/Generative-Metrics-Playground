# import sys
# sys.path.append('/Users/majue/Documents/MIT/multi_stakeholders_indicator_d3')
import sys
import os
current_directory = os.path.dirname(os.path.abspath(__file__))
project_directory = os.path.join(current_directory, '..')
sys.path.append(project_directory)

from backend.model_tool import *
from backend.ESE_metrics import *
from backend.resident_model import *
from backend.workforce_model import *
from backend.localbisness_model import *
from backend.government_model import *
from backend.developer_model import *
from backend.NPI_model import *
from backend.industry_model import *
import pandas as pd
import numpy as np
import random
from backend.input_data import input_value
import requests

import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

# -----------------------------------------------------
# input_value = [random.uniform(0, 3.25),0.3, 0.2, 0.1, 0.4]
# -----------------------------------------------------

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
        self.access_score = get_before_after(0.77, 0.5* self.access_to_service1['value']+ 0.5* self.access_to_service2['value'])
        self.civic_score =  get_before_after(0.76, self.civic_space['value'])
        self.safety_security_score = get_before_after(1, self.safety_security['value'])
        # self.tax_cost_score = get_before_after(0, self.tax_cost['value'])
        self.resident_score = self.get_resident_score() *100

    def get_resident_score(self):
        score = 0.33 * self.access_score['after'] + 0.33 * self.civic_score['after'] + 0.34 * self.safety_security_score['after']
        return score


class Workforce():
    def __init__(self):
        self.access_to_service = {
            "target": 'Local Business Owners',
            "value": get_access_business_2()
        }
        self.opportunity1 = {
            "target": 'Local Business Owners',
            "value": get_opportunity_LBO()
        }
        self.opportunity2 = {
            "target": 'Industry Group',
            "value": get_opportunity_IG()
        }
        self.safety_security = {
            "target": 'Government',
            "value": get_access_police_2()
        }

        self.access_score = get_before_after(0.05, self.access_to_service['value'])
        self.opportunity_score = get_before_after(0, 0.5 * self.opportunity1['value'] + 0.5 * self.opportunity2['value'])
        self.safety_security_score = get_before_after(1, self.safety_security['value'])
        self.workforce_score = self.get_workforce_score() *100

    def get_workforce_score(self):
        score = 0.33 * self.access_score['after'] + 0.33 * self.opportunity_score['after'] + 0.34 * self.safety_security_score['after']
        return score


class LocalBusinessOwner():
    def __init__(self):
        self.finance1 = {
            "target": 'Residents',
            "value": get_business_res()
        }
        self.finance2 = {
            "target": 'Workforce',
            "value": get_business_work()
        }
        self.safety_security = {
            "target": 'Government',
            "value": get_access_police_3()
        }
        # self.tax_cost = {
        #     "target": 'Government',
        #     "value": round(random.uniform(0, 1), 2)
        # }
        # self.build_up_area = {
        #     "target": 'Developer',
        #     "value": round(random.uniform(0, 1), 2)
        # }
        self.finance_score = get_before_after(0.3, 0.5 * self.finance1['value'] + 0.5 * self.finance2['value'])
        self.safety_security_score = get_before_after(1, self.safety_security['value'])
        # self.tax_cost_score = get_before_after(0, 1)
        self.local_business_owner_score = self.get_local_business_owner_score() *100

    def get_local_business_owner_score(self):
        score = 0.5 * self.finance_score['after'] + 0.5 * self.safety_security_score['after']
        return score


class Government():
    def __init__(self):
        self.tax_revenue1 = {
            "target": 'Local Business Owners',
            "value": get_tax_LBO()
        }
        self.tax_revenue2 = {
            "target": 'Developer',
            "value": get_tax_dev()
        }
        self.tax_revenue3 = {
            "target": 'Industry Group',
            "value": get_tax_IG()
        }
        self.tax_revenue4 = {
            "target": 'Residents',
            "value": get_tax_res()
        }
        self.tax_revenue5 = {
            "target": 'Workforce',
            "value": get_tax_work()
        }
        self.manage_cost = {
            "target": 'Developer',
            "value": get_manage_cost()
        }
        self.safety_security1 = {
            "target": 'Residents',
            "value": get_access_police_res()
        }
        self.safety_security2 = {
            "target": 'Workforce',
            "value": get_access_police_work()
        }
        # self.safety_security3 = {
        #     "target": 'Local Business Owner',
        #     "value": round(random.uniform(0, 1), 2)
        # }
        # self.voting = {
        #     "target": 'Resident',
        #     "value": round(random.uniform(0, 1), 2)
        # }

        self.finance_score = get_before_after(0, 0.2 * self.tax_revenue1['value'] + 0.2 * self.tax_revenue2['value'] + 0.2 * self.tax_revenue3['value'] + 0.1 * self.tax_revenue4['value'] + 0.1 * self.tax_revenue5['value'] - 0.2 *self.manage_cost['value'])
        self.safety_security_score = get_before_after(1, 0.5 * self.safety_security1['value'] + 0.5 * self.safety_security2['value'])
        self.government_score = self.get_government_score() *100

    def get_government_score(self):
        score = 0.5 * self.finance_score['after'] + 0.5 * self.safety_security_score['after']
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

class NonProfitInstitution():
    def __init__(self):
        self.access_to_service = {
            "target": 'Local Business Owners',
            "value": get_access_LBO()
        }
        self.safety_security = {
            "target": 'Government',
            "value": get_access_police_4()
        }
        self.innovation = {
            "target": 'Industry Group',
            "value": get_access_IG()
        }

        self.access_score = get_before_after(0.55,  self.access_to_service['value'] )
        self.safety_security_score = get_before_after(1, self.safety_security['value'])
        self.innovation_score = get_before_after(0, self.innovation['value'])
        self.non_profit_score = self.get_non_profit_score() *100

    def get_non_profit_score(self):
        score = 0.33 * self.access_score['after'] + 0.33 * self.safety_security_score['after'] + 0.34 * self.innovation_score['after']
        return score

class IndustryGroup():
    def __init__(self):
        self.access_to_service = {
            "target": 'Local Business Owners',
            "value": get_access_LBO()
        }
        self.safety_security = {
            "target": 'Government',
            "value": get_access_police_4()
        }
        self.innovation = {
            "target": 'Nonprofit Institution',
            "value": get_access_NPI()
        }

        self.access_score = get_before_after(0.55,  self.access_to_service['value'] )
        self.safety_security_score = get_before_after(1, self.safety_security['value'])
        self.innovation_score = get_before_after(0, self.innovation['value'])
        self.industry_score = self.get_industry_score() *100

    def get_industry_score(self):
        score = 0.33 * self.access_score['after'] + 0.33 * self.safety_security_score['after'] + 0.34 * self.innovation_score['after']
        return score
#--------------------------------------------#
# Test
#--------------------------------------------#

def create_indicator_list(stakeholder, stakeholder_name):
    indicator_list = []
    for indicator, value in stakeholder.__dict__.items():
        if isinstance(value, dict):
            indicator_list.append({
                "stakeholder": stakeholder_name,
                "indicator": indicator,
                "target": value["target"],
                "value": value["value"]
            })
    return indicator_list


def stake_test():
    resident = Resident()
    workforce = Workforce()
    local_business_owner = LocalBusinessOwner()
    government = Government()
    developer = Developer()
    non_profit_institution = NonProfitInstitution()
    industry_group = IndustryGroup()
    print(input_value)
    # --------------------------------------------#
    # Data for bubble: score
    # --------------------------------------------#
    # Creat a list of stakeholders
    score = [
        {"stakeholder": "Residents","score": (int(resident.resident_score) - 84), "radius": 40, 'distance': 40},
        {"stakeholder": "Local Business Owners", "score": (int(local_business_owner.local_business_owner_score) -65), "radius": 80, 'distance': 70},
        {"stakeholder": "Nonprofit Institution", "score": (int(non_profit_institution.non_profit_score) -51), "radius": 140, 'distance': 100},
        {"stakeholder": "Government", "score": (int(government.government_score) -10), "radius": 100, 'distance': 80},
        {"stakeholder": "Workforce", "score": (int(workforce.workforce_score) -35), "radius": 60, 'distance': 60},
        {"stakeholder": "Industry Group", "score": (int(industry_group.industry_score) -51), "radius": 160, 'distance': 140},
        {"stakeholder": "Developer", "score": (int(developer.developer_score) -0), "radius": 120, 'distance': 90}
    ]

    # Creat a dataframe of stakeholders
    score_df = pd.DataFrame(score)
    # print(score_df)
    # output_file = os.path.abspath("./backend/output/bubble_data.csv")
    # score_df.to_csv(output_file, index=False)

    #
    # --------------------------------------------#
    # Data for chord chart: interaction
    # --------------------------------------------#

    # Creat a list of stakeholders
    indicator_list = [
        {"stakeholder": "Residents", "indicator": "Access to service", "target": resident.access_to_service1["target"], "value": resident.access_to_service1["value"]},
        {"stakeholder": "Residents", "indicator": "Access to service", "target": resident.access_to_service2["target"], "value": resident.access_to_service2["value"]},
        # {"stakeholder": "Resident", "indicator": "Job-housing balance", "target": resident.job_housing["target"], "value": resident.job_housing["value"]},
        {"stakeholder": "Residents", "indicator": "Civic space", "target": resident.civic_space["target"], "value": resident.civic_space["value"]},
        {"stakeholder": "Residents", "indicator": "Safety & security", "target": resident.safety_security["target"], "value": resident.safety_security["value"]},
        # {"stakeholder": "Resident", "indicator": "Tax", "target": resident.tax_cost["target"], "value": resident.tax_cost["value"]},
        # {"stakeholder": "Resident", "indicator": "Build-up area", "target": resident.build_up_area["target"], "value": resident.build_up_area["value"]},
        {"stakeholder": "Workforce", "indicator": "Access to service", "target": workforce.access_to_service["target"], "value": workforce.access_to_service["value"]},
        {"stakeholder": "Workforce", "indicator": "Opportunity", "target": workforce.opportunity1["target"], "value": workforce.opportunity1["value"]},
        {"stakeholder": "Workforce", "indicator": "Opportunity", "target": workforce.opportunity2["target"], "value": workforce.opportunity2["value"]},
        {"stakeholder": "Workforce", "indicator": "Safety & security", "target": workforce.safety_security["target"], "value": workforce.safety_security["value"]},
        {"stakeholder": "Local Business Owners", "indicator": "Finance", "target": local_business_owner.finance1["target"], "value": local_business_owner.finance1["value"]},
        {"stakeholder": "Local Business Owners", "indicator": "Finance", "target": local_business_owner.finance2["target"], "value": local_business_owner.finance2["value"]},
        {"stakeholder": "Local Business Owners", "indicator": "Safety & security", "target": local_business_owner.safety_security["target"], "value": local_business_owner.safety_security["value"]},
        # {"stakeholder": "Local business owner", "indicator": "Tax", "target": local_business_owner.tax_cost["target"], "value": local_business_owner.tax_cost["value"]},
        {"stakeholder": "Government", "indicator": "Tax revenue", "target": government.tax_revenue1["target"], "value": government.tax_revenue1["value"]},
        {"stakeholder": "Government", "indicator": "Tax revenue", "target": government.tax_revenue2["target"], "value": government.tax_revenue2["value"]},
        {"stakeholder": "Government", "indicator": "Tax revenue", "target": government.tax_revenue3["target"], "value": government.tax_revenue3["value"]},
        {"stakeholder": "Government", "indicator": "Tax revenue", "target": government.tax_revenue4["target"], "value": government.tax_revenue4["value"]},
        {"stakeholder": "Government", "indicator": "Tax revenue", "target": government.tax_revenue5["target"], "value": government.tax_revenue5["value"]},
        {"stakeholder": "Government", "indicator": "Management Cost", "target": government.manage_cost["target"], "value": government.manage_cost["value"]},
        {"stakeholder": "Government", "indicator": "Safety & security", "target": government.safety_security1["target"], "value": government.safety_security1["value"]},
        {"stakeholder": "Government", "indicator": "Safety & security", "target": government.safety_security2["target"], "value": government.safety_security2["value"]},
        {"stakeholder": "Developer", "indicator": "Profit", "target": developer.profit_construction1["target"], "value": developer.profit_construction1["value"]},
        {"stakeholder": "Developer", "indicator": "Profit", "target": developer.profit_construction2["target"], "value": developer.profit_construction2["value"]},
        {"stakeholder": "Developer", "indicator": "Profit", "target": developer.profit_construction3["target"], "value": developer.profit_construction3["value"]},
        {"stakeholder": "Developer", "indicator": "Tax", "target": developer.tax_cost["target"], "value": developer.tax_cost["value"]},
        {"stakeholder": "Nonprofit Institution", "indicator": "Access to service", "target": non_profit_institution.access_to_service["target"], "value": non_profit_institution.access_to_service["value"]},
        {"stakeholder": "Nonprofit Institution", "indicator": "Safety & security", "target": non_profit_institution.safety_security["target"], "value": non_profit_institution.safety_security["value"]},
        {"stakeholder": "Nonprofit Institution", "indicator": "Innovation", "target": non_profit_institution.innovation["target"], "value": non_profit_institution.innovation["value"]},
        {"stakeholder": "Industry Group", "indicator": "Access to service", "target": industry_group.access_to_service["target"], "value": industry_group.access_to_service["value"]},
        {"stakeholder": "Industry Group", "indicator": "Safety & security", "target": industry_group.safety_security["target"], "value": industry_group.safety_security["value"]},
        {"stakeholder": "Industry Group", "indicator": "Innovation", "target": industry_group.innovation["target"], "value": industry_group.innovation["value"]}
         ]
    indicator_df = pd.DataFrame(indicator_list)
    indicator_df['value'] = indicator_df['value'].round(2)
    # print(indicator_df)
    # output_file = os.path.abspath("./backend/output/indicator.csv")
    # indicator_df.to_csv(output_file, index=False)

    # --------------------------------------------#
    # Data for indicator chart: indicator value
    # --------------------------------------------#
    # Create a list of index score
    index_score = [
        {"stakeholder": "Residents","indicator": "Access to service", "baseline": resident.access_score['before'],"score": resident.access_score['after']},
        {"stakeholder": "Residents","indicator": "Civic space", "baseline": resident.civic_score['before'],"score": resident.civic_score['after']},
        {"stakeholder": "Residents","indicator": "Safety & security", "baseline": resident.safety_security_score['before'],"score": resident.safety_security_score['after']},
        # {"stakeholder": "Resident","indicator": "Tax", "baseline": resident.tax_cost_score['before'],"score": resident.tax_cost_score['after']},
        {"stakeholder": "Workforce","indicator": "Access to service", "baseline": workforce.access_score['before'],"score": workforce.access_score['after']},
        {"stakeholder": "Workforce","indicator": "Opportunity", "baseline": workforce.opportunity_score['before'],"score": workforce.opportunity_score['after']},
        {"stakeholder": "Workforce","indicator": "Safety & security", "baseline": workforce.safety_security_score['before'],"score": workforce.safety_security_score['after']},
        {"stakeholder": "Local Business Owners","indicator": "Finance", "baseline": local_business_owner.finance_score['before'],"score": local_business_owner.finance_score['after']},
        {"stakeholder": "Local Business Owners","indicator": "Safety & security", "baseline": local_business_owner.safety_security_score['before'],"score": local_business_owner.safety_security_score['after']},
        # {"stakeholder": "Local business owner","indicator": "Tax", "baseline": local_business_owner.tax_cost_score['before'],"score": local_business_owner.tax_cost_score['after']},
        {"stakeholder": "Government","indicator": "Finance", "baseline": government.finance_score['before'],"score": government.finance_score['after']},
        {"stakeholder": "Government","indicator": "Safety & security", "baseline": government.safety_security_score['before'],"score": government.safety_security_score['after']},
        {"stakeholder": "Developer","indicator": "Profit", "baseline": developer.profit_construction_score['before'],"score": developer.profit_construction_score['after']},
        # {"stakeholder": "Developer","indicator": "Innovation", "baseline": developer.innovation_score['before'],"score": developer.innovation_score['after']},
        {"stakeholder": "Developer","indicator": "Tax", "baseline": developer.tax_cost_score['before'],"score": developer.tax_cost_score['after']},
        {"stakeholder": "Nonprofit Institution","indicator": "Access to service", "baseline": non_profit_institution.access_score['before'],"score": non_profit_institution.access_score['after']},
        {"stakeholder": "Nonprofit Institution","indicator": "Safety & security", "baseline": non_profit_institution.safety_security_score['before'],"score": non_profit_institution.safety_security_score['after']},
        {"stakeholder": "Nonprofit Institution","indicator": "Innovation", "baseline": non_profit_institution.innovation_score['before'],"score": non_profit_institution.innovation_score['after']},
        {"stakeholder": "Industry Group","indicator": "Access to service", "baseline": industry_group.access_score['before'],"score": industry_group.access_score['after']},
        {"stakeholder": "Industry Group","indicator": "Opportunity", "baseline": industry_group.access_score['before'],"score": industry_group.access_score['after']},
        {"stakeholder": "Industry Group","indicator": "Safety & security", "baseline": industry_group.safety_security_score['before'],"score": industry_group.safety_security_score['after']},
        {"stakeholder": "Industry Group","indicator": "Innovation", "baseline": industry_group.innovation_score['before'],"score": industry_group.innovation_score['after']}
    ]
    index_score_df = pd.DataFrame(index_score)
    index_score_df['score'] = index_score_df['score'].round(2)
    # print(index_score_df)
    # output_file = os.path.abspath("./backend/output/index_score.csv")
    # index_score_df.to_csv(output_file, index=False)
    
    # Instead of saving to CSV, convert dataframe to JSON
    # data_json = score_df.to_json(orient="records")
    # output_file = os.path.abspath("./backend/output/bubble_data.csv")
    # send_to_api(data_json, output_file)

    # data_json = indicator_df.to_json(orient="records")
    # output_file = os.path.abspath("./backend/output/indicator.csv")
    # send_to_api(data_json, output_file)

    # data_json = index_score_df.to_json(orient="records")
    # output_file = os.path.abspath("./backend/output/index_score.csv")
    # send_to_api(data_json, output_file)
    
    # Instead of saving to CSV, convert dataframe to JSON
    data_json = score_df.to_json(orient="records")
    print(data_json)
    print(type(data_json))
    send_to_api(data_json, "bubble_data")

    data_json = indicator_df.to_json(orient="records")
    send_to_api(data_json, "indicator")

    data_json = index_score_df.to_json(orient="records")
    send_to_api(data_json, "index_score")

def send_to_api(data_json, filename):
    # Define the API endpoint (assuming Flask app is running on localhost:5000)
    api_url = f'http://127.0.0.1:5000/api/save_data/{filename}'
    # api_url = f'http://localhost:5000/api/save_data'
    
    # Adding filename as a parameter or in the data body
    # params = {'filename': filename}
    # Use the POST method to send data
    # response = requests.post(api_url, params=params, data=data_json, headers={'Content-Type': 'application/json'})
    print(api_url)
    response = requests.post(api_url, data=data_json, headers={'Content-Type': 'application/json'})
    print(response.text)

    # Check the response
    if response.status_code == 200:
        console_log(f"Data successfully sent to API for {filename}!")
        print(f"Data successfully sent to API for {filename}!")
    else:
        print(f"Failed to send data for {filename}. Status code: {response.status_code}, Response: {response.text}")

def console_log(message):
    print("[CONSOLE.LOG]", message)


if __name__ == '__main__':
    stake_test()