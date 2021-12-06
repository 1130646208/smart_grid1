# -- coding: utf-8 --
from fdi import FDI
from hdis import HDIS
from utils import *


if __name__ == '__main__':
    # 配置
    start_time = datetime.datetime(2014, 3, 17)
    houses = ['House2', 'House3', 'House5', 'House12']
    week_num = 6
    resolution = 0.4
    magnitude = 10 ** 8

    house_data = []
    # 运算
    for h in houses:
        house_data.append(get_week_data(h, start_time, week_num))

    sum_data = []
    for i in range(week_num):
        w_data = []
        for j in range(7):
            s = 0
            for h in range(len(houses)):
                s += house_data[h][i][j]
            w_data.append(s)
        sum_data.append(w_data)
    print('sum: ', sum_data)

    discrete_data = []
    for s in sum_data:
        r = HDIS.discrete(s, resolution, magnitude)
        discrete_data.append(r)

    for i in range(len(discrete_data) - 1):
        u_d1, u_d2 = HDIS.uniform_scale(discrete_data[i], discrete_data[i + 1], resolution)
        print(HDIS.hellinger_distance(u_d1, u_d2), end='\t')
    #
    # fig = plt.figure()
    # draw('test', fig, *([i for i in range(7)], sum_data[0]))

