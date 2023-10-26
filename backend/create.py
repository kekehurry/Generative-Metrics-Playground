import json
import os

data = [
    {"stakeholder": "Residents", "score": 5, "initial_score": 0.0, "radius": 5, "distance": 5, "best": 20.0},
    {"stakeholder": "Local Business Owners", "score": 9, "initial_score": 0, "radius": 9, "distance": 9, "best": 50},
    {"stakeholder": "Nonprofit Institution", "score": 9, "initial_score": 0, "radius": 9, "distance": 9, "best": 50},
    {"stakeholder": "Government", "score": 5, "initial_score": 0.0, "radius": 5, "distance": 5, "best": 60.0},
    {"stakeholder": "Developer", "score": 8, "initial_score": 0.0, "radius": 8, "distance": 8, "best": 50.0},
    {"stakeholder": "Workforce", "score": 11, "initial_score": 0, "radius": 11, "distance": 11, "best": 50},
    {"stakeholder": "Industry Group", "score": 13, "initial_score": 0, "radius": 13, "distance": 13, "best": 35}
]

increment = 1  # 每次循环增加的分数
num_updates = 25  # 设置更新的次数
folder_path = 'api/output/create'

# 检查文件夹是否存在，如果不存在则创建
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

for update_num in range(1, num_updates + 1):
    # 更新 stakeholder 的值
    for i in range(len(data)):
        data[i]['score'] += increment
        data[i]['radius'] += increment
        data[i]['distance'] += increment
        # 您可以在这里添加一个条件来确保 'score'、'radius' 和 'distance' 不超过 'best' 或其他最大值

    # 保存更新后的数据到指定文件夹
    filename = os.path.join(folder_path, f'bubble_data_{update_num}.json')
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

    print(f'Data updated and saved to {filename}')



