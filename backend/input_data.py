import os
import json

file_path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output/input.json'))

with open(file_path, 'r') as file:
    input_value = json.load(file)

# print(input_value)

VOLPE_area = 30593
## when we normalize the score, we use the max floor = 30 
max_FAR = 3.25  # from cambridge zoning regulation https://www.cambridgema.gov/~/media/Files/CDD/ZoningDevel/zoningguide/zguide.ashx
max_floor_area = 99427
# max_floor_area = 30 * VOLPE_area
floor_area = VOLPE_area * input_value['bcr'] * input_value['tier']  # 0.6 is the bcr, 3 is the tier

office_space = floor_area * input_value['office'] 
amenity_space = floor_area * input_value['amenity']
civic_space = floor_area * input_value['civic']
resident_space = floor_area * input_value['residential']

open_space = VOLPE_area * (1-input_value['bcr'])
green_space = open_space * 0.5

# print("office_space:", office_space, 
#       "amenity_space:", amenity_space, 
#       "civic_space:", civic_space, 
#       "resident_space:", resident_space, 
#       "open_space:", open_space, 
#       "green_space:", green_space)


def refresh_input(input_json=None):
    global input_value, resident_space, office_space, amenity_space, civic_space, open_space, green_space

    if input_json:
        input_value = input_json
    else:
        file_path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output/input.json'))
        with open(file_path, 'r') as file:
            input_value = json.load(file)

    VOLPE_area = 30593
    max_FAR = 3.25  # from cambridge zoning regulation https://www.cambridgema.gov/~/media/Files/CDD/ZoningDevel/zoningguide/zguide.ashx
    max_floor_area = 99427
    floor_area = VOLPE_area * input_value['bcr'] * input_value['tier']  # 0.6 is the bcr, 3 is the tier

    office_space = floor_area * input_value['office'] 
    amenity_space = floor_area * input_value['amenity']
    civic_space = floor_area * input_value['civic']
    resident_space = floor_area * input_value['residential']

    open_space = VOLPE_area * (1-input_value['bcr'])
    green_space = open_space * 0.5

    # print("office_space:", office_space, 
    #     "amenity_space:", amenity_space, 
    #     "civic_space:", civic_space, 
    #     "resident_space:", resident_space, 
    #     "open_space:", open_space, 
    #     "green_space:", green_space)

# input_value = [
#     0.6,  # bcr
#     3, # tier
#     0.2, # residential
#     0.5, # office
#     0.2, #amenity
#     0.1 # civic
#     ]


# 如果 received_data 中的值都不是 None，就使用它，否则使用默认值
# if all(value is not None for value in received_data.values()):
#     input_value = [
#         received_data['bcr'],
#         received_data['tier'],
#         received_data['residential'],
#         received_data['office'],
#         received_data['amenity'],
#         received_data['civic']
#     ]
# else:
#     # 默认值
#     input_value = [
#         0.6,  # bcr
#         3,    # tier
#         0.2,  # residential
#         0.5,  # office
#         0.2,  # amenity
#         0.1   # civic
#     ]

