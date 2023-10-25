import numpy as np

def cal_surface_to_volume_ratio(state):
    matrix = (state!=0)
    volume = np.sum(matrix)
    surface_area = 0
    # 在三个维度上都填充一个0边界
    padded_matrix = np.pad(matrix, pad_width=1, mode='constant', constant_values=0)
    # 对于每一个方向，检查邻居是否存在
    directions = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    for dx, dy, dz in directions:
        # 使用numpy的roll函数来移动数组，使得对应的邻居可以对齐
        neighbor = np.roll(padded_matrix, shift=(dx, dy, dz), axis=(0, 1, 2))
        surface_area += np.sum(padded_matrix * (padded_matrix != neighbor))
    surface_to_volume_ratio = surface_area/volume
    return surface_to_volume_ratio

def cal_surface_to_volume_index(state):
    surface_to_volume_ratio = cal_surface_to_volume_ratio(state)
    surface_to_volume_index = get_normalized_score(surface_to_volume_ratio,target=2,sigma=1)*100
    return surface_to_volume_index

def cal_sky_view(state):
    matrix = (state!=0)
    sky_view = np.zeros((10, 10), dtype=int)
    for x in range(10):
        for y in range(10):
            if matrix[x, y, 0] == 0:
                directions = [
                    (1, 0, 2),   # x 30
                    (-1, 0, 2),  # x -30
                    (0, 1, 2),   # y 30
                    (0, -1, 2),  # y -30
                    (0, 0, 1)    # z vertical
                ]
                for dx, dy, dz in directions:
                    x_current, y_current, z_current = x, y, 0
                    while 0 <= x_current < 10 and 0 <= y_current < 10 and 0 <= z_current < 10:
                        x_current += dx
                        y_current += dy
                        z_current += dz
                        if 0 <= x_current < 10 and 0 <= y_current < 10 and 0 <= z_current < 10:
                            if matrix[x_current, y_current, z_current] == 0:
                                sky_view[x, y] += 1
                            else:
                                break

    return sky_view
def cal_sky_view_index(state):
    sky_view = cal_sky_view(state)
    sky_view_index = np.sum(sky_view/25)
    return sky_view_index


def get_normalized_score(value,target,sigma=1):
    score = np.exp(-((value - target) ** 2) / (2 * sigma ** 2))
    normalized_score = score
    return normalized_score