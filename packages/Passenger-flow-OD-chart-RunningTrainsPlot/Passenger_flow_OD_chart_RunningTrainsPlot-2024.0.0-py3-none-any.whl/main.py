import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path
import pandas as pd
import numpy as np
from matplotlib import rcParams

# 配置中文字体
rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 从 CSV 文件读取数据
file_path = "od_data.csv"  # 替换为你的文件路径
df = pd.read_csv("D:\Desktop\Pythontest\od_data.csv")

# 定义节点的垂直位置
nodes = list(set(df["origin"].tolist() + df["destination"].tolist()))
nodes.sort()
node_pos = {node: i for i, node in enumerate(nodes)}

# 设置颜色
colors = plt.cm.Paired(np.linspace(0, 1, len(nodes)))

# 创建图形
fig, ax = plt.subplots(figsize=(10, 8))

# 绘制 S 型曲线
for i, row in df.iterrows():
    origin = row["origin"]
    destination = row["destination"]
    value = row["value"]

    # 起点和终点的 y 位置
    y_origin = node_pos[origin]
    y_destination = node_pos[destination]

    # S 型曲线的控制点
    path = Path(
        [
            (0, y_origin),  # 起点
            (0.25, y_origin + 0.5),  # 第一个控制点，向外扩展
            (0.75, y_destination - 0.5),  # 第二个控制点，回收靠近终点
            (1, y_destination),  # 终点
        ],
        [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
    )
    patch = PathPatch(path, lw=value / 10, edgecolor=colors[y_origin], facecolor="none", alpha=0.6)
    ax.add_patch(patch)

# 设置节点标签（左侧）
ax.set_yticks(range(len(nodes)))
ax.set_yticklabels(nodes, fontsize=12, color="black")

# 在右侧添加站点轴并对齐
for i, node in enumerate(nodes):
    ax.text(1.02, i, node, fontsize=12, va="center", color="black")  # 右侧文字对齐

# 美化图形
ax.set_xlim(-0.1, 1.2)
ax.set_ylim(-0.5, len(nodes) - 0.5)
ax.set_xticks([0, 1])
ax.set_xticklabels(["出发", "到达"], fontsize=12)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

# 添加标题
plt.title("OD 流量图", fontsize=16)
plt.tight_layout()
plt.show()
