from Passenger_flow_OD_chart_RunningTrainsPlot import plot_od_chart
import os

# 指定 CSV 文件路径
csv_file = "od_data.csv"  # 修改为实际的 CSV 文件路径

# 检查文件是否存在
if not os.path.exists(csv_file):
    print(f"CSV 文件不存在，请检查路径：{csv_file}")
else:
    print(f"找到 CSV 文件：{os.path.abspath(csv_file)}")
    # 调用绘图函数
    try:
        plot_od_chart(csv_file)
    except Exception as e:
        print(f"运行出错：{e}")
