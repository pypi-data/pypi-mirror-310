# -*- coding: utf-8 -*-
"""
This module is made for drawing a train platform schedule for high speed train station

Please check the data format for the schedule before you use the function

Created on Sep., 4th, 2023.
@author: Gongyuan Lu, Prof., Railsmart Lab, Southwest Jiaotong univeristy, lugongyuan@swjtu.cn
For education use only.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
import csv

# Before you drawing a Train platform schedule, read this carefully
# The train platform schedule is formatted as a csv file with following field:
# TrainID,PlatformID,ReceveingRouteID,DepartureRouteID,ReceivingTime,ArrivalTime,DepartureTime,LeavingTime,ArrivalDelay,DepartureDelay,,
# prepare the data before you use the functions
# "ReceveingRouteID,DepartureRouteID" are not necessary fields

#define each column
trainID=[]
platformID=[]
receivingRouteID=[]
departureRouteID=[]
eventTime=[[]]
receivingTime=[]
arrivalTime=[]
departureTime=[]
leavingTime=[]
arrivalDelay=[]
departureDelay=[]

# read Train Platform schedule file
csvFile = open("PlatformScheduleSample.csv", "r")
reader = csv.reader(csvFile)

#read schedule data
for item in reader:
    # 忽略第一行
    if reader.line_num == 1:
        continue
    if(len(item)>5):
        trainID.append(int(item[0]))
        platformID.append(int(item[1])+1)
        receivingRouteID.append(int(item[2]))
        departureRouteID.append(int(item[3]))
        receivingTime.append(int(item[4]))
        arrivalTime.append(int(item[5]))
        departureTime.append(int(item[6]))
        leavingTime.append(int(item[7]))
        arrivalDelay.append(int(item[8]))
        departureDelay.append(int(item[9]))
csvFile.close()
#

# Calculate the maximum platformID and leavingTime
max_platformID = max(platformID)
max_leavingTime = max(leavingTime)

# Create a blank figure without any data points
ax=plt.figure(figsize=(12, 6))  # Adjust the figure size as needed

# Set Y-axis limits based on the maximum platformID
plt.ylim(0, max_platformID + 1)

# Show gridlines at integer Y coordinates (platforms)
plt.yticks(np.arange(0, max_platformID + 1, 1))  # Set Y-axis ticks to integer values

# Show a grid for better readability
plt.grid(True, linestyle='--',which='both', axis='both')  # Show gridlines on both axes

# Set X-axis limits based on the maximum leavingTime
plt.xlim(0, max_leavingTime + 50)  # Add 10 for better visualization

# Show a grid for better readability
plt.grid(True)

# Plot rectangles for arrival and departure times of each train
for i in range(len(trainID)):

    train_id = trainID[i]  # Get TrainID
    arrival = arrivalTime[i]
    departure = departureTime[i]
    platform = platformID[i]

    receiving_time = receivingTime[i] 
    leaving_time=leavingTime[i]  

    arrival_delay = arrivalDelay[i]
    departure_delay = departureDelay[i]



    # Calculate the width of the rectangle
    width = departure - arrival

# Determine the color based on delays
    if arrival_delay > 0 or departure_delay > 0:
        color = 'blue'
        edgecolor = 'black'  # Set the border color to black
    else:
        color = 'green'
        edgecolor = 'black'  # Set the border color to black
    
    #set height of the rectangle
    height=0.6

    # Create and plot the rectangle for each train with the determined color and border color
    rect = plt.Rectangle((arrival, platform ), width, height, color=edgecolor, fill=False, alpha=0.8)
    plt.gca().add_patch(rect)

 # Add the TrainID in the middle of the rectangle
    text_x = arrival + width / 2
    text_y = platform+height/2
    plt.text(text_x, text_y, str(train_id), color=color, ha='center', va='center')

# Conditionally add arrival delay text label to the left of the rectangle
    if arrival_delay > 0:
        delay_label_x = arrival - 2  # Adjust the x-coordinate for the label
        delay_label_y = platform
        plt.text(delay_label_x, delay_label_y, f'+{round(arrival_delay/60,2)}', color='orange', ha='right', va='center', fontsize=8)
    if departure_delay > 0:
        delay_label_x = departure + 200 # Adjust the x-coordinate for the label
        delay_label_y = platform + height
        plt.text(delay_label_x, delay_label_y, f'+{round(departure_delay/60,2)}', color='red', ha='right', va='center', fontsize=8)


# Add triangle for receiving time
    if arrival_delay > 0:
        color = 'blue'
        edgecolor = 'black'  # Set the border color to black
    else:
        color = 'green'
        edgecolor = 'black'  # Set the border color to black
    triangle_x = receiving_time
    triangle_y1 = platform 
    triangle_y2 = platform + height
    triangle = Polygon([(triangle_x, triangle_y1), (arrival, triangle_y1), (arrival, triangle_y2)],
                      closed=True, edgecolor=color,facecolor=color,alpha=0.8)  
    plt.gca().add_patch(triangle)

# Add triangle for leaving time
    if departure_delay > 0:
        color = 'blue'
        edgecolor = 'black'  # Set the border color to black
    else:
        color = 'green'
        edgecolor = 'black'  # Set the border color to black
    triangle_x = leaving_time
    triangle_y1 = platform 
    triangle_y2 = platform + height
    triangle = Polygon([(departure, triangle_y1), (departure, triangle_y2),(triangle_x, triangle_y1)],
                      closed=True, edgecolor=color,facecolor=color,alpha=0.8)  
    plt.gca().add_patch(triangle)


# Set plot labels and title
plt.xlabel('Time(sec)')
plt.ylabel('Platform ID')
plt.title('Platform Schedule')

# Add a legend to label the rectangles
#plt.legend(loc='upper left')


# Show the plot
plt.show()