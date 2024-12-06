import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
import csv

filename = "Sample2.csv"#在此修改读取文件的名称

# 读取CSV数据
def read_schedule(file):
    trainID, platformID, receivingTime, arrivalTime, departureTime, leavingTime, arrivalDelay, departureDelay = [], [], [], [], [], [], [], []
    with open(file, "r") as csvFile:
        reader = csv.reader(csvFile)
        next(reader)  # 跳过表头
        for item in reader:
            if len(item) > 5:
                trainID.append(int(item[0]))
                platformID.append(int(item[1]) + 1)
                receivingTime.append(int(item[4]))
                arrivalTime.append(int(item[5]))
                departureTime.append(int(item[6]))
                leavingTime.append(int(item[7]))
                arrivalDelay.append(int(item[8]))
                departureDelay.append(int(item[9]))
    return trainID, platformID, receivingTime, arrivalTime, departureTime, leavingTime, arrivalDelay, departureDelay

# 绘制矩形和三角形
def plot_schedule(trainID, platformID, arrivalTime, departureTime, receivingTime, leavingTime, arrivalDelay, departureDelay):
    max_platformID = max(platformID)
    max_leavingTime = max(leavingTime)
    
    plt.figure(figsize=(12, 6))
    plt.ylim(0, max_platformID + 1)
    plt.xlim(0, max_leavingTime + 50)
    plt.yticks(np.arange(0, max_platformID + 1, 1))
    plt.grid(True, linestyle='--', which='both')

    for i in range(len(trainID)):
        arrival = arrivalTime[i]
        departure = departureTime[i]
        platform = platformID[i]
        receiving_time = receivingTime[i]
        leaving_time = leavingTime[i]
        arrival_delay = arrivalDelay[i]
        departure_delay = departureDelay[i]

        width = departure - arrival
        color = 'blue' if arrival_delay > 0 or departure_delay > 0 else 'green'
        height = 0.6

        # 绘制矩形
        rect = Rectangle((arrival, platform), width, height, color=color, fill=False, edgecolor='black', alpha=0.8)
        plt.gca().add_patch(rect)
        plt.text(arrival + width / 2, platform + height / 2, str(trainID[i]), color=color, ha='center', va='center')

        # 绘制延误标签
        if arrival_delay > 0:
            plt.text(arrival - 2, platform, f'+{round(arrival_delay / 60, 2)}', color='orange', ha='right', va='center', fontsize=8)
        if departure_delay > 0:
            plt.text(departure + 200, platform + height, f'+{round(departure_delay / 60, 2)}', color='red', ha='right', va='center', fontsize=8)

        # 绘制接收时间三角形
        triangle = Polygon([(receiving_time, platform), (arrival, platform), (arrival, platform + height)], closed=True, edgecolor=color, facecolor=color, alpha=0.8)
        plt.gca().add_patch(triangle)

        # 绘制离开时间三角形
        triangle = Polygon([(departure, platform), (departure, platform + height), (leaving_time, platform)], closed=True, edgecolor=color, facecolor=color, alpha=0.8)
        plt.gca().add_patch(triangle)

# 主程序
def main():
    trainID, platformID, receivingTime, arrivalTime, departureTime, leavingTime, arrivalDelay, departureDelay = read_schedule(filename)
    plot_schedule(trainID, platformID, arrivalTime, departureTime, receivingTime, leavingTime, arrivalDelay, departureDelay)
    
    plt.xlabel('Time(sec)')
    plt.ylabel('Platform ID')
    plt.title('Platform Schedule')
    plt.show()

# 调用主程序
if __name__ == "__main__":
    main()