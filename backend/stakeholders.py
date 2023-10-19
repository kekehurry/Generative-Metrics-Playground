# import sys
# sys.path.append('/Users/majue/Documents/MIT/multi_stakeholders_indicator_d3')
import sys
import os
current_directory = os.path.dirname(os.path.abspath(__file__))
project_directory = os.path.join(current_directory, '..')
sys.path.append(project_directory)

from backend.model_tool import *
from backend.ESE_metrics import *
from backend.resident_model import compute_resident
from backend.workforce_model import compute_workforce
from backend.localbisness_model import compute_local_business_owner
from backend.government_model import compute_government
from backend.developer_model import compute_developer
from backend.NPI_model import compute_NPI
from backend.industry_model import compute_industry
import pandas as pd
import numpy as np
import random
from backend.input_data import input_value, refresh_input
import requests

import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

# -----------------------------------------------------
# input_value = [random.uniform(0, 3.25),0.3, 0.2, 0.1, 0.4]
# -----------------------------------------------------








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
    # workforce = Workforce()
    # local_business_owner = LocalBusinessOwner()
    # government = Government()
    # developer = Developer()
    # non_profit_institution = NonProfitInstitution()
    # industry_group = IndustryGroup()
    
    # --------------------------------------------#
    # Data for bubble: score
    # --------------------------------------------#
    # Creat a list of stakeholders
    score_res, indicator_res, index_res = compute_resident()
    # print(score_res)
    score_dev, indicator_dev, index_dev = compute_developer()
    # print(score_dev)
    score_gov, indicator_gov, index_gov = compute_government()
    # print(score_gov)
    score_work, indicator_work, index_work = compute_workforce()
    score_ind, indicator_ind, index_ind = compute_industry()
    score_local, indicator_local, index_local = compute_local_business_owner()
    score_non_profit, indicator_non_profit, index_non_profit = compute_NPI()
    
    score = [
        score_res,
        score_local,
        score_non_profit,
        score_gov,
        score_dev,
        score_work,
        score_ind
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
    indicator_list = (indicator_res + indicator_gov + indicator_dev
                      + indicator_work + indicator_ind + indicator_local + indicator_non_profit)
    indicator_df = pd.DataFrame(indicator_list)
    # indicator_df['value'] = indicator_df['value'].round(2)
    # print(indicator_df)
    # output_file = os.path.abspath("./backend/output/indicator.csv")
    # indicator_df.to_csv(output_file, index=False)

    # --------------------------------------------#
    # Data for indicator chart: indicator value
    # --------------------------------------------#
    # Create a list of index score
    index_score = (index_res + index_gov + index_dev
                   + index_work + index_ind + index_local + index_non_profit)
    index_score_df = pd.DataFrame(index_score)
    # index_score_df['score'] = index_score_df['score'].round(2)
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
    # print(data_json)
    # print(type(data_json))
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