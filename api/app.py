from flask import Flask, request, jsonify
import json
import time
import pandas as pd
from flask_cors import CORS
from pathlib import Path
import subprocess

import sys
import os
current_directory = os.path.dirname(os.path.abspath(__file__))
project_directory = os.path.join(current_directory, '..')
sys.path.append(project_directory)
# sys.path.append('/Users/majue/Documents/MIT/multi_stakeholders_indicator_d3')
from backend.ESE_metrics import ese_test
from backend.stakeholders import stake_test



app = Flask(__name__)
CORS(app)  # Allow all origins to access this server
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# 用于存储接收到的数据
received_data = {
    'bcr': None,
    'tier': None,
    'residential': None,
    'office': None,
    'amenity': None,
    'civic': None
}

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/')
def index():
    return 'Welcome to My API!'

@app.route('/api/receive_values', methods=['POST'])
def receive_values():
    global received_data
    data = request.json
    received_data.update(data) # 将 data 中的值更新到 received_data 中

    residential = data.get('residential')
    office = data.get('office')
    amenity = data.get('amenity')
    civic = data.get('civic')
    bcr = data.get('bcr')  # Building Coverage Ratio
    tier = data.get('tier')
    
    # office_space, amenity_space, civic_space, resident_space = variables(
    #     residential, office, amenity, civic, bcr, tier, VOLPE_area)


    print("Residential:", residential)
    print("Office:", office)
    print("Amenity:", amenity)
    print("Civic:", civic)
    print("BCR:", bcr)
    print("Tier:", tier)
    print("Received data:", data)
    return jsonify({"message": "Values received successfully!"})


# @app.route('/api/save_data/<filename>', methods=['POST'])
# def save_data(filename):
#     data = request.json
#     print("Received data:", data)
    
#     if not data:
#         return jsonify({"message": "No data!"}), 400

#     print("Received data:", data)

#     # 保存 JSON 数据
#     try:
#         output_path = Path(f'output/{filename}.json')  # 添加 .json 扩展名
#         output_path.parent.mkdir(parents=True, exist_ok=True)  # 确保目录存在
#         with output_path.open('w') as json_file:
#             json.dump(data, json_file)
   
#     # # 将数据转回为DataFrame
#     # try:
#     #     df = pd.DataFrame(data)
#     # except Exception as e:
#     #     return jsonify({"message": f"将数据转换为DataFrame时出错: {e}"}), 500
    
#     # # 保存DataFrame
#     # try:
#     #     # output_path = f'{filename}'
#     #     output_path = f'output/{filename}'
#     #     df.to_csv(output_path, index=False)
#     except Exception as e:
#         return jsonify({"message": f"error when save data: {e}"}), 500
    
#     return jsonify({"message": f"data successfully saved to {output_path}!"}), 200

@app.route('/api/save_data/<filename>', methods=['POST'])
def save_data(filename):
    data = request.json
    print("Received data:", data)
    
    if not data:
        return jsonify({"message": "No data!"}), 400

    # 保存 JSON 数据
    try:
        output_path = Path(f'output/{filename}.json')  # 添加 .json 扩展名
        output_path.parent.mkdir(parents=True, exist_ok=True)  # 确保目录存在
        with output_path.open('w') as json_file:
            json.dump(data, json_file)
            
        # # 运行后端计算程序
        # result = subprocess.run(['python', 'ESE_metrics.py'], capture_output=True, text=True)
        # print(result.stdout)  # 打印后端程序的输出
        
        # return jsonify({"message": f"Radar data update!"}), 200

    except Exception as e:
        return jsonify({"message": f"Error when saving data: {e}"}), 500
    
    return jsonify({"message": f"Data successfully saved to {output_path}!"}), 200

@app.route('/api/get_data/<filename>', methods=['GET'])
def get_data(filename):
    try:
        # filepath = f'{filename}.csv'
        filepath = f'output/{filename}'
        # df = pd.read_csv(filepath)
        # return df.to_json(orient="records"), 200
        with open(filepath, 'r') as file:
            data = json.load(file)
        return  data, 200
    except Exception as e:
        return jsonify({"message": f"error when reading or sending data: {e}"}), 500

@app.route('/api/compute', methods=['POST'])
def compute():
    try:
        ese_test()  # 调用你的计算函数
        print('ESE metrics computed!')
        stake_test() 
        print('Stakeholder metrics computed!')
        return jsonify({"message": "Data updated!"}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "An error occurred during the computation"}), 500

if __name__ == '__main__':
    app.run(debug=True)

