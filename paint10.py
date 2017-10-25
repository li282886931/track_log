# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 19:45:56 2017

@author: 58
"""

import matplotlib.pyplot as plt


def read(p="E:/hive.out.txt"):
    tracks=[]
    file=open(p)
    for line in file:
        track=[]
        #line=line.replace("\n","")
        line=line.replace("|",",")
        #line=line.replace(")","")
        a=line.split(",")
    
        for x in range(len(a)):
            if (x % 3 == 0):
                try:
                    point = (int(a[x]),int(a[x+1]),int(a[x+2]))
                except ValueError:
                    pass
                
                track.append(point)
        tracks.append(track)
        #print tracks
    return tracks
   
#x速度    
def x_speed(track):
    vs = []
    for i in range(1,len(track)):
        dis = track[i][0] - track[i-1][0]
        time = track[i][2] - track[i-1][2]
        if (time != 0):
            v = dis / time
            vs.append(v)
    return vs

#时间-x坐标
def t_x(track):
    t=[]
    dis=[]
    for point in track:
        t.append(point[2])
        dis.append(point[0])
    return t,dis

#x速度差
def x_v_diff(track):
    diff=[]
    x_v=x_speed(track)
    for i in range(1,len(x_v)):
        diff.append(x_v[i]-x_v[i-1])
    return diff

#x坐标差
def x_diff(track):
    diff=[]
    for i in range(1,len(track)):
        diff.append(abs(track[i][0]-track[i-1][0]))
    return diff

#y速度    
def y_speed(track):
    vs = []
    for i in range(1,len(track)):
        dis = track[i][1] - track[i-1][1]
        time = track[i][2] - track[i-1][2]
        if (time != 0):
            v = dis / time
            vs.append(v)
    return vs

#时间-y坐标
def t_y(track):
    t=[]
    dis=[]
    for point in track:
        t.append(point[2])
        dis.append(point[1])
    return t,dis

#y坐标查
def y_diff(track):
    diff=[]
    for i in range(1,len(track)):
        diff.append(abs(track[i][1]-track[i-1][1]))
    return diff
        
print("##############")
tracks=read()
tracks=tracks[-50:-1]
for track in tracks:
    t,x=t_y(track)
    plt.plot(t,x)
    plt.ylim(730,760)
#    res=x_speed(track)
#    print(sum(res)/len(res))
#    plt.plot(range(len(res)),res)
#    plt.ylim(-1,5)
    plt.show()
        


    
