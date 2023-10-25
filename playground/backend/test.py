import math
import matplotlib.pyplot as plt
import numpy as np

# 假设的居民月收入和月租金
income = 5000  # 假设值
rent = 1500    # 假设值

# 计算affordability
affordability = rent / income

def gaussian_function(x):
    optimal_affordability = 0.3
    variance = 0.2
    goodness_index = math.exp(-((x - optimal_affordability)**2) / (2 * variance**2))
    return goodness_index

# 逻辑函数
def logistic_function(x):
    optimal_affordability = 0.3
    k = 10  # 控制曲线的陡峭程度
    return 1 / (1 + math.exp(-k * (x - optimal_affordability)))

# 指数衰减函数
def exponential_decay(x):
    optimal_affordability = 0.3
    lambda_ = 10  # 控制衰减速率
    return math.exp(-lambda_ * abs(x - optimal_affordability))

# 分段线性函数
def piecewise_linear(x):
    optimal_affordability = 0.3
    if x < optimal_affordability:
        return 1 - 2*(optimal_affordability - x)
    else:
        return 1 - 2*(x - optimal_affordability)

# 计算不同affordability下的goodness index
affordability_values = np.linspace(0, 1, 100)
gaussian_values = [gaussian_function(a) for a in affordability_values]
logistic_values = [logistic_function(a) for a in affordability_values]
exponential_values = [exponential_decay(a) for a in affordability_values]
piecewise_values = [piecewise_linear(a) for a in affordability_values]

# 绘图
plt.plot(affordability_values, gaussian_values, label="Gaussian Function")
plt.plot(affordability_values, logistic_values, label="Logistic Function")
plt.plot(affordability_values, exponential_values, label="Exponential Decay")
plt.plot(affordability_values, piecewise_values, label="Piecewise Linear")
plt.axvline(x=0.3, color='r', linestyle='--')
plt.xlabel('Affordability')
plt.ylabel('Goodness Index')
plt.title('Goodness Index for Different Affordability Values')
plt.legend()
plt.grid(True)
plt.show()