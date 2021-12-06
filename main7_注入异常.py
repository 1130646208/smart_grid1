# -- coding: utf-8 --

from fdi import FDI
from hdis import HDIS
from utils import *



if __name__ == '__main__':
    # 配置
    start_time = datetime.datetime(2014, 3, 17)
    house = 'House2'
    week_num = 6
    resolution = 0.5
    magnitude = 10 ** 7

    # 计算
    week_data = get_week_data(house, start_time, week_num)

    discrete_data = []
    # for i, d in zip(range(len(week_data)), week_data):
    #     if i == 1:
    #         r = HDIS.discrete(inject(d, FDI.fdi1, 1), resolution, magnitude)
    #     else:
    #         r = HDIS.discrete(d, resolution, magnitude)
    #     discrete_data.append(r)

    for i, d in zip(range(len(week_data)), week_data):
        if i == 1:
            r = HDIS.discrete(FDI.inject(d, FDI.fdi2, 3*10**7), resolution, magnitude)
        else:
            r = HDIS.discrete(d, resolution, magnitude)
        discrete_data.append(r)

    for i in range(len(discrete_data) - 1):
        u_d1, u_d2 = HDIS.uniform_scale(discrete_data[i], discrete_data[i + 1], resolution)
        print(HDIS.hellinger_distance(u_d1, u_d2), end='\t')
