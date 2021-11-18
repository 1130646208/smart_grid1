# -- coding: utf-8 --
import math
import datetime
import bisect


def hellinger_distance(p: list, q: list, ruler: list):

    pass


def discrete(data: list, resolution: float, magnitude: int):
    maxi = data[0] / magnitude
    mini = data[0] / magnitude
    small_data = []
    for d in data:
        d /= magnitude
        if d < mini:
            mini = d
        if d > maxi:
            maxi = d
        small_data.append(d)
    res = []
    flag = 0
    discrete_list = [flag]
    while flag <= maxi:
        flag += resolution
        discrete_list.append(flag)
    for d in small_data:
        ind = bisect.bisect_right(discrete_list, d)
        left_dist = d - discrete_list[ind-1]
        right_dist = discrete_list[ind] - d
        res.append(discrete_list[ind-1] if left_dist < right_dist else discrete_list[ind])
    return res


def read_week_data(file_name):
    res = []
    with open(file_name) as f:
        while True:
            line = f.readline()
            if not line:
                break
            usage = float(line.strip('\n').split(',')[1])
            res.append(usage)
    return res


if __name__ == '__main__':
    start_time = datetime.datetime(2014, 3, 17)
    house = 'House12'

    week_data = []
    for week_num in range(6):
        time_span = [start_time, start_time + datetime.timedelta(days=7)]
        week_data.append(read_week_data('数据集/多个家庭/{}.csv_{}_{}_{}_{}.csv_week_usage.csv'.format(house, time_span[0].date(), time_span[1].date(), int(time_span[0].timestamp()), int(time_span[1].timestamp()))))
        start_time += datetime.timedelta(days=7)

    for d in week_data:
        r = discrete(d, 0.5, 10**7)
        print(r)
