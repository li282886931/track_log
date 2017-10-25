#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from collections import Counter
import math


def readfile(path):
    # track = []
    points = []
    # for line in sys.stdin:
    for line in open(path, 'rU'):
        if len(line) < 8:
            continue
        for co in line.split('|'):
            point = co.split(',')
            if len(point) > 2:
                dpoint = (float(point[0]), float(point[1]), float(point[2]) / 1000)
                points.append(dpoint)

        # 计算移动距离
        sum_avg_distance(points)

        # 计算最大最小距离
        # find_max_min_dis(points)

        # 计算移动速度
        sum_avg_velocity(points)

        # 前%N坐标平均速度
        front_vel(points, 0.05)

        # 前%N坐标平均速度
        front_vel(points, 0.1)

        # 相邻坐标速度差
        adjacent_speed(points)


def writefile(data, path):
    pass


def sum_avg_distance(points):
    x_sum_m, x_sum_v, y_sum_m, y_sum_v = 0.0, 0.0, 0.0, 0.0
    x_data, y_data = [], []
    for i in range(1, len(points)):
        x_dis = abs(points[i][0] - points[i - 1][0])
        y_dis = abs(points[i][1] - points[0][1])

        x_data.append(x_dis)
        y_data.append(y_dis)

        x_sum_m += x_dis
        x_sum_v += x_dis ** 2
        y_sum_m += y_dis
        y_sum_v += y_dis ** 2

    x_avg_dis = x_sum_m / (len(points) - 1)
    x_mean_avg = x_sum_m / len(points)
    x_dis_var = x_sum_v / len(points) - x_mean_avg ** 2
    y_avg_dis = y_sum_m / (len(points) - 1)
    y_mean_avg = y_sum_m / len(points)
    y_dis_var = y_sum_v / len(points) - y_mean_avg ** 2
    x_left = x_sum_m / (points[-1][0] - points[0][0])
    #print '时间：%.2f'%(points[-1][2])
    #print "x总移动距离: %.2f, x轴左移比例:%.2f, x平均移动距离: %.2f, x移动距离均值: %.2f, x移动距离方差: %.2f, y总移动距离: %.2f, y平均移动距离: %.2f, y移动距离均值: %.2f, y移动距离方差: %.2f" % (x_sum_m,x_left, x_avg_dis, x_mean_avg, x_dis_var, y_sum_m, y_avg_dis, y_mean_avg, y_dis_var)
    print "%.2f, %.2f,%.2f,%.2f,%.2f, %.2f, %.2f" %(points[-1][2], x_left,max(x_data), min(x_data), x_mean_avg, max(x_data) - min(x_data), x_dis_var)


def find_max_min_dis(points):
    x_data, y_data = [], []
    for i in range(1, len(points)):
        x_dis = abs(points[i][0] - points[i - 1][0])
        y_dis = abs(points[i][1] - points[0][1])

        x_data.append(x_dis)
        y_data.append(y_dis)

    x_no_cnt = Counter(x_data).most_common(2)
    x_no_change = float(x_no_cnt[0][1]) / (len(x_data) - 1) * 100
    y_no_cnt = Counter(y_data).most_common(2)
    y_no_change = float(y_no_cnt[0][1]) / (len(y_data) - 1) * 100
    print "x相邻坐标最大距离: %.2f, x相邻坐标最小距离: %.2f, x区间长度:%.2f, x区间不变比例: %.2f%%, y相邻坐标最大距离: %.2f, y相邻坐标最小距离: %.2f, y区间长度:%.2f,y区间不变比例:%.2f%%" % (max(x_data), min(x_data), max(x_data) - min(x_data), x_no_change, max(y_data), min(y_data), max(y_data) - min(y_data), y_no_change)


def sum_avg_velocity(points):
    x_vel, y_vel = [], []
    x_sum, x_v_sum, y_sum, y_v_sum, x_v_sum_v, y_v_sum_v = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    for i in range(1, len(points)):
        x_dis = abs(points[i][0] - points[i - 1][0])
        y_dis = abs(points[i][1] - points[0][1])
        t = points[i - 1][2] * 1000

        x_v = x_dis / t
        y_v = y_dis / t

        x_vel.append(x_v)
        y_vel.append(y_v)

        x_v_sum += x_v
        x_v_sum_v += x_v ** 2
        y_v_sum += y_v
        y_v_sum_v += y_v ** 2

        x_sum += x_dis
        y_sum += y_dis

    x_avg_vel = x_sum / points[-1][2] / 1000
    y_avg_vel = y_sum / points[-1][2] / 1000

    cnt = Counter(x_vel).most_common(2)

    x_mean = x_v_sum / len(x_vel)
    x_val = x_v_sum_v / len(x_vel) - x_mean ** 2
    y_mean = y_v_sum / len(y_vel)
    y_val = y_v_sum_v / len(y_vel) - y_mean ** 2
    no_change = float(cnt[0][1]) / (len(x_vel) - 1) * 100

    # print "x平均速度: %.2f像素/毫秒, x最大速度:%.2f像素/毫秒,所在位置:%d, x最小速度:%.2f像素/毫秒, x速度区间长度:%.2f,x速度区间均值:%.2f, 方差:%.2f, 速度不变的比例: %.2f%% , y平均速度: %.2f像素/毫秒, y最大速度:%.2f像素/毫秒, 最小速度:%.2f像素/毫秒,,x区间长度:%.2f, y速度区间均值:%.2f, 方差:%.2f" % (x_avg_vel, max(x_vel), x_vel.index(max(x_vel)), min(x_vel), max(x_vel) - min(x_vel), x_mean, x_val, no_change, y_avg_vel, max(y_vel), min(y_vel), max(y_vel) - min(y_vel), y_mean, y_val)
    print "%.2f,%.2f,%d,%.2f,%.2f,%.2f,%.2f,%.2f" %(x_avg_vel, max(x_vel), x_vel.index(max(x_vel))/len(x_vel), min(x_vel), x_mean, max(x_vel) - min(x_vel), x_val, no_change)


def front_vel(points, ramdon=0.05):
    x_v_sum = 0.0
    x_vel = []
    for i in range(1, int(math.ceil(len(points) * ramdon + 1))):
        x_dis = abs(points[i][0] - points[0][0])
        t = points[i - 1][2] * 1000

        x_v = x_dis / t
        x_vel.append(x_v)
        x_v_sum += x_v

    x_avg_vel = x_v_sum / len(x_vel)
    # print "前 %.2f%% 坐标区间平均速度: %.2f像素/毫秒, 平均速度与最大速度的差绝对值:%.2f, 与最小速度的差绝对值:%.2f" % (ramdon*100, x_avg_vel, abs(x_avg_vel - max(x_vel)), abs(x_avg_vel - min(x_vel)))
    print "%.2f, %.2f" %(x_avg_vel, abs(x_avg_vel - max(x_vel)))


def adjacent_speed(points):
    x_vel, y_vel, x_mul_speed = [], [], []
    sum_x_mul_speed, sum_x_mul_speed_v = 0.0, 0.0
    for i in range(1, len(points)):
        x_dis = abs(points[i][0] - points[i - 1][0])
        y_dis = abs(points[i][1] - points[0][1])
        t = points[i - 1][2] * 1000

        x_v = x_dis / t
        y_v = y_dis / t

        x_vel.append(x_v)
        y_vel.append(y_v)

    for i in range(1, len(x_vel)):
        x_vel_mul = abs(x_vel[i] - x_vel[i - 1])
        sum_x_mul_speed += x_vel_mul
        sum_x_mul_speed_v += x_vel_mul ** 2
        x_mul_speed.append(x_vel_mul)

    cnt = Counter(x_mul_speed).most_common(2)
    x_mul_mean = sum_x_mul_speed / len(x_mul_speed)
    x_mul_val = sum_x_mul_speed_v / len(x_mul_speed) - x_mul_mean ** 2
    no_change = float(cnt[0][1]) / (len(x_mul_speed) - 1) * 100
    print "相邻坐标区间速度差最大值: %.2f 像素/毫秒, 最小值:%.2f 像素/毫秒, 区间长度:%.2f 像素/毫秒, 均值:%.2f, 标准差:%.2f, 速度差不变的比例: %.2f%%" % (max(x_mul_speed), min(x_mul_speed), max(x_mul_speed) - min(x_mul_speed), x_mul_mean, x_mul_val, no_change)


def main():
    readfile('E:/test00.txt')


if __name__ == '__main__':
    main()
