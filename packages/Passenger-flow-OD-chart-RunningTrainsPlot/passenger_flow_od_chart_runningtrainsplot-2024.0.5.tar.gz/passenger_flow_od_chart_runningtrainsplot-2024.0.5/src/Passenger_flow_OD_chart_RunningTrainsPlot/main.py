import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path
import pandas as pd
import numpy as np
from matplotlib import rcParams
import os

# 配置中文字体
rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

def validate_csv(file_path):
    """
    验证 CSV 文件的格式和内容
    """
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        raise ValueError(f"无法读取 CSV 文件，请检查文件格式是否正确：{e}")

    required_columns = {"origin", "destination", "value"}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"CSV 文件缺少必要的列：{required_columns - set(df.columns)}")
    return df

def plot_od_chart(file_path=None):
    """
    绘制 OD 流量图
    """
    if not file_path:
        print("未提供数据文件路径。请输入路径：")
        file_path = input("请输入 CSV 文件路径: ").strip()

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"指定的文件路径不存在：{file_path}")

    try:
        df = validate_csv(file_path)
    except ValueError as e:
        print(f"CSV 文件验证失败：{e}")
        return

    nodes = list(set(df["origin"].tolist() + df["destination"].tolist()))
    nodes.sort()
    node_pos = {node: i for i, node in enumerate(nodes)}

    colors = plt.cm.Paired(np.linspace(0, 1, len(nodes)))

    fig, ax = plt.subplots(figsize=(10, 8))
    for i, row in df.iterrows():
        origin = row["origin"]
        destination = row["destination"]
        value = row["value"]

        y_origin = node_pos[origin]
        y_destination = node_pos[destination]

        path = Path(
            [
                (0, y_origin),
                (0.25, y_origin + 0.5),
                (0.75, y_destination - 0.5),
                (1, y_destination),
            ],
            [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
        )
        patch = PathPatch(path, lw=value / 10, edgecolor=colors[y_origin], facecolor="none", alpha=0.6)
        ax.add_patch(patch)

    ax.set_yticks(range(len(nodes)))
    ax.set_yticklabels(nodes, fontsize=12, color="black")

    for i, node in enumerate(nodes):
        ax.text(1.02, i, node, fontsize=12, va="center", color="black")

    ax.set_xlim(-0.1, 1.2)
    ax.set_ylim(-0.5, len(nodes) - 0.5)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["出发", "到达"], fontsize=12)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    plt.title("OD 流量图", fontsize=16)
    plt.tight_layout()
    plt.show()
