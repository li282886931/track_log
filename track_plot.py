# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 19:45:56 2017

@author: 58
"""

import matplotlib.pyplot as plt
import random


def read(f):
    tracks=[]
    file=open("./" + f + ".txt")
#    head=1;
    for line in file:
#        if  head== 1:
#            head=0
#            continue
        track=[]
        line=line.strip()
        line=line[0:-1]
        line=line.replace("|",",")
        line=line.replace("\n","")
        line=line.replace("(","")
        line=line.replace(")","")
        a=line.split(",");
        for x in range(len(a)):
            if (x % 3 == 0):
                point = (float(a[x]),float(a[x+1]),float(a[x+2]))
                track.append(point)
        tracks.append(track)
    return tracks

def x_y(track):
    x=[]
    y=[]
    for point in track:
        x.append(point[0])
        y.append(point[1])
    return x,y
   
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
tracks=read("17_ip_1")
a=[]
for i in range(len(tracks)):
  if i in xxx:
#for m in range(100):
#    i=random.randint(0,10000)
    track=tracks[i]
#    print("##"+str(i)+" time:" + str(track[-1][2]))
    a,b=x_y(track)
    plt.plot(a,b)
    plt.xlim(0,500)
    plt.ylim(-500,500)
    plt.title("x_y:"+str(i))
#    res=x_speed(track)
#    print(sum(res)/len(res))
#    plt.figure()
#    plt.title("x_speed:"+str(i))
#    plt.plot(range(len(res)),res)
#    plt.ylim(-1,5)
    plt.show()
#    if i % 20 == 0:
#        input()


#    gaps=[]
#    for i in range(1,len(track)):
#        t_gap=track[i][2]-track[i-1][2]
#        gaps.append(t_gap)
#    print("min:",min(gaps)," max:",max(gaps)," avg",sum(gaps)/len(gaps))

#    vs=x_speed(track)
#    print("min:",min(vs)," max:",max(vs)," avg:",sum(vs)/len(vs))
#    

        


    
