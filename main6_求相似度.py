# -- coding: utf-8 --
import math
import bisect


def hellinger_distance(p: list, q: list):
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
            usage = line.split(',')[1]
            res.append(usage)
    return res


if __name__ == '__main__':
    data = [22986914.0, 25156526.0, 35592972.5, 35064030.0, 26074722.5, 34903419.0, 45000000.0]
    print(discrete(data, 0.5, 10**7))
