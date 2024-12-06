# -*- coding: utf-8 -*-
"""
Created on Sun Sep 4 19:13:55 2023

@author: Gongyuan Lu, Southwest Jiaotong univeristy, lugongyuan@swjtu.cn
@Railsmart Lab
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
from matplotlib.path import Path
import csv


# 读取Train Platform schedule
csvFile = open("testSchedule.csv", "r")
reader = csv.reader(csvFile)



#读路径长度
trainid=[]
platform=[]
ReceivingRoute=[]
DepartureRoute=[]
EventTime=[[]]

arrivalDelay=[]
departureDelay=[]
EventTime.clear
for item in reader:
    # 忽略第一行
    if reader.line_num == 1:
        continue
    if(len(item)>5):
        trainid.append(int(item[0]))
        platform.append(int(item[1])+1)
        ReceivingRoute.append(int(item[2]))
        DepartureRoute.append(int(item[3]))
        EventTime.append([int(item[5]),int(item[6]),int(item[7]),int(item[8])])
        arrivalDelay.append(int(item[10]))
        departureDelay.append(int(item[11]))
csvFile.close()
#
print(trainid)

fig, ax = plt.subplots(figsize=(15,7))
plt.xlim(0,5300)
plt.ylim(1,16)

for i in range(30):
        j=i+1
        #draw rectangle to illustrate arrival and departure
        rect=plt.Rectangle((EventTime[j][1]-5,platform[i]+0.05),EventTime[j][2]-EventTime[j][1],0.55,fill=False,alpha=0.8)
        ax.add_patch(rect)
         #draw triangle 1 to illustrate receiving process      
        delta1=[[EventTime[j][0],platform[i]-0.001],[EventTime[j][1],platform[i]],[EventTime[j][1],platform[i]+0.6]]
        triangle1=plt.Polygon(delta1)
        ax.add_patch(triangle1)
        #draw triangle 2 to illustrate departure route
        delta2=[[EventTime[j][2],platform[i]],[EventTime[j][3],platform[i]],[EventTime[j][2],platform[i]+0.6]]
        triangle2=plt.Polygon(delta2)
        ax.add_patch(triangle2)
        if arrivalDelay[i]>0:#arrival delay
            ax.plot([EventTime[j][1]-arrivalDelay[i],EventTime[j][1]-arrivalDelay[i]],[platform[i]+0.05,platform[i]+0.55], color='red')
            ax.plot([EventTime[j][1]-arrivalDelay[i],EventTime[j][1]],[platform[i]+0.2,platform[i]+0.2], color='red')
        if departureDelay[i]>0:#departure delay
            ax.plot([EventTime[j][2]-departureDelay[i],EventTime[j][2]-departureDelay[i]],[platform[i]+0.05,platform[i]+0.55], color='orange')
            ax.plot([EventTime[j][2]-departureDelay[i],EventTime[j][2]],[platform[i]+0.4,platform[i]+0.4], color='orange')     
        #train id
        ax.text(EventTime[j][1],platform[i]+0.1,trainid[i],style='italic',c='black',fontsize='14')
        #receiving route id
        ax.text(EventTime[j][0]-80,platform[i]+0.1,ReceivingRoute[i],style='italic',c='orange',fontsize='14')
        #departure route id
        ax.text(EventTime[j][3],platform[i]+0.1,ReceivingRoute[i],style='italic',c='purple',fontsize='14')

ax.text(5,0,'@railsmart',style='italic',c='grey',fontsize='20')

ax.grid()
plt.show()


