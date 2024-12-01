
from multiprocessing import Process

from flask import Flask, render_template, request, jsonify
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from torch.distributions import Normal, Categorical
from PIL import Image
import requests
import os
import sys
current_directory = os.path.dirname(os.path.abspath(__file__))
project_directory = os.path.join(current_directory, '..')
sys.path.append(project_directory)

from backend.input_data import refresh_input
from backend.developer_model import cal_future_profit_index
from backend.government_model import cal_future_tax_revenue_index
from backend.resident_model import cal_future_affordability_index
from backend.compute_core import cal_sky_view_index, cal_surface_to_volume_index, get_normalized_score

ncols = 10
nrows = 10
num_state = 1000
num_action = 200
max_height = 10

device = torch.device("cpu")
actor_net_pkl = "playground/param/actor_net/latest.pkl"
ref_path = "playground/static/ref.png"
server_address = "http://127.0.0.1:5001"

app = Flask(__name__)
seed = 42
torch.manual_seed(seed)
np.random.seed(seed)

app = Flask(__name__)


class Actor(nn.Module):
    def __init__(self):
        super(Actor, self).__init__()
        self.fc1 = nn.Linear(num_state, 100)
        self.fc2 = nn.Linear(num_state, 100)
        self.action_head = nn.Linear(100, num_action)

    def forward(self, x):
        x = x.view(-1, num_state)
        x = F.relu(self.fc1(x))
        x = self.action_head(x)
        x = F.softmax(x, dim=1)
        return x


actor_net = Actor().to(device)
actor_net.load_state_dict(torch.load(actor_net_pkl))
ref_img = Image.open(ref_path).resize((nrows, ncols)).convert('L')
ref_state = np.array(ref_img)/255.


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/playground')
def playground():
    return render_template('playground.html')


@app.route('/get_server_address')
def get_server_address():
    return jsonify(server_address=server_address)


@app.route('/get_score', methods=['POST'])
async def get_score():
    data = request.get_json()
    state = np.array(data['state'])
    link_to_citymatrix = data['link_to_citymatrix']
    # aesthetic_score
    # aesthetic_index = np.sum(get_normalized_score(np.count_nonzero(state,axis=-1),ref_state,sigma=0.1))
    aesthetic_index = np.sum(ref_state*np.count_nonzero(state, axis=-1))
    # city matrix score
    bcr = np.count_nonzero(state[:, :, 0]) / 100
    far = np.count_nonzero(state)/100
    osr = 1-bcr
    max_L = int(np.max(np.count_nonzero(state, axis=-1)))/max_height
    r_ratio = np.count_nonzero(state == 1)/np.count_nonzero(state)*0.5
    o_ratio = 0.5 - r_ratio
    input_json = {"bcr": bcr, "tier": 3, "residential": r_ratio,
                  "office": o_ratio, "amenity": 0.2, "civic": 0.3}
    refresh_input(input_json)
    affordability_index = cal_future_affordability_index()
    tax_revenue_index = cal_future_tax_revenue_index()*5
    profit_index = cal_future_profit_index()
    sky_view_index = cal_sky_view_index(state)
    surface_to_volume_index = cal_surface_to_volume_index(state)
    environment_index = (sky_view_index + surface_to_volume_index)/2
    # aesthetic_index = sky_view_index
    environment_index = surface_to_volume_index
    total = aesthetic_index+affordability_index + \
        tax_revenue_index+profit_index+environment_index
    scores = [aesthetic_index, affordability_index, tax_revenue_index,
              profit_index, sky_view_index, surface_to_volume_index]
    indexes = [bcr, far, osr, max_L, r_ratio, o_ratio]
    if link_to_citymatrix:
        await update_radar(input_json)
    return jsonify(scores=scores, indexes=indexes)


@app.route('/get_suggestion', methods=['POST'])
async def select_action():
    state_data = request.get_json()
    state = np.array(state_data)
    state = torch.from_numpy(state).float().unsqueeze(0).to(device)
    with torch.no_grad():
        action_prob = actor_net(state)
    c = Categorical(action_prob)
    action = c.sample().item()
    return jsonify(action=action)


async def update_radar(input_json):
    try:
        requests.post(server_address+'/api/receive_values', json=input_json)
        requests.post(server_address+"/api/save_data/input", json=input_json)
        requests.get(server_address+"/api/compute")
        requests.get(server_address+"/api/refresh")
    except Exception:
        pass
    return


def run_citymatrixserver():
    os.system("python api/app.py")


if __name__ == '__main__':

    p = Process(target=run_citymatrixserver)
    p.start()
    app.run(debug=True, port=5002, host='0.0.0.0')
