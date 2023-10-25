# import numpy as np
# import matplotlib.pyplot as plt

# # 需求方程
# def demand(price):
#     return 1000 - 2*price

# # 供应方程
# def supply(price):
#     return -500 + 3*price

# # 找到均衡价格和均衡数量
# prices = np.linspace(0, 500, 500)
# equilibrium_price = next(p for p in prices if demand(p) <= supply(p))
# equilibrium_quantity = demand(equilibrium_price)

# # 绘制供需曲线
# plt.figure(figsize=(10, 6))
# plt.plot([demand(p) for p in prices], prices, label="Demand Curve")
# plt.plot([supply(p) for p in prices], prices, label="Supply Curve")

# # 标记均衡价格和数量
# plt.plot(equilibrium_quantity, equilibrium_price, 'ro') 
# plt.annotate(f'Equilibrium\nPrice: {equilibrium_price:.2f}\nQuantity: {equilibrium_quantity:.2f}', 
#              xy=(equilibrium_quantity, equilibrium_price), 
#              xytext=(equilibrium_quantity+50, equilibrium_price+50),
#              arrowprops=dict(facecolor='black', arrowstyle='->'),
#              fontsize=9)

# # 设置图表标签和标题
# plt.xlabel("Quantity")
# plt.ylabel("Price")
# plt.title("Supply and Demand Curve for Rental Price")
# plt.legend()
# plt.grid(True)
# plt.show()

import numpy as np
import matplotlib.pyplot as plt

# 初始情况
initial_price = 3658 * 12   # 当前的年房价
initial_demand = 20000      # 当前的需求面积
initial_supply = 18000      # 当前的供应面积

# 预计的未来情况
additional_demand = 5000    # 额外的需求面积
additional_supply = 4000    # 额外的供应面积

# 计算未来的需求和供应
future_demand = initial_demand + additional_demand
future_supply = initial_supply + additional_supply

# 定义需求和供应与价格之间的关系
def price_from_demand_supply(demand, supply):
    # 这里我们简单假设价格是需求和供应的线性函数，你可以根据实际情况调整
    return initial_price * demand / supply

# 计算未来的均衡价格
future_price = price_from_demand_supply(future_demand, future_supply)

# 打印未来的均衡价格
print(f"Future equilibrium price: {future_price}")

# 画图显示变化
plt.figure(figsize=(10, 6))
plt.bar(['Current Price', 'Future Price'], [initial_price, future_price], color=['blue', 'green'])
plt.title("Comparison of Current and Future Prices")
plt.ylabel("Price")
plt.show()
