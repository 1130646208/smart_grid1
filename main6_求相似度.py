# -- coding: utf-8 --
import math
import datetime
import bisect


def hellinger_distance(p: list, q: list):
    """
    根据H距离的定义计算
    :param p: pi
    :param q: qi
    :return: H距离
    """
    part = 0
    for p_i, q_i in zip(p, q):
        part += math.pow(math.sqrt(p_i) - math.sqrt(q_i), 2)
    return 1 / math.sqrt(2) * math.sqrt(part)


def uniform_scale(data1: list, data2: list, resolution: float):
    """
    统一data1和data2的标度
    :param data2: data2
    :param data1: data1
    :param resolution: 精度
    :return: 统一标度后，每个值出现的概率
    """
    assert len(data1) == len(data2) and len(data1) > 0
    mini = data1[0]
    maxi = data2[0]
    factor = 1 / len(data1)
    data1_freq = {}
    data2_freq = {}
    for d1, d2 in zip(data1, data2):
        mini = min(d1, d2, mini)
        maxi = max(d1, d2, maxi)
        if not data1_freq.get(d1):
            data1_freq[d1] = factor
        else:
            data1_freq[d1] += factor
        if not data2_freq.get(d2):
            data2_freq[d2] = factor
        else:
            data2_freq[d2] += factor

    res1, res2 = [], []
    scale = mini
    while scale <= maxi:
        if data1_freq.get(scale):
            res1.append(data1_freq.get(scale))
        else:
            res1.append(0.0)
        if data2_freq.get(scale):
            res2.append(data2_freq.get(scale))
        else:
            res2.append(0.0)
        scale += resolution
    return res1, res2


def discrete(data: list, resolution: float, magnitude: int):
    """
    将数据离散化
    :param data: 原始数据
    :param resolution: 离散化之后的精度
    :param magnitude: 数据的量级
    :return: 离散化的数据
    """
    maxi = data[0] / magnitude
    mini = data[0] / magnitude
    small_data = []
    for _d in data:
        _d /= magnitude
        if _d < mini:
            mini = _d
        if _d > maxi:
            maxi = _d
        small_data.append(_d)
    res = []
    flag = 0
    discrete_list = [flag]
    while flag <= maxi:
        flag += resolution
        discrete_list.append(flag)
    for _d in small_data:
        ind = bisect.bisect_right(discrete_list, _d)
        left_dist = _d - discrete_list[ind - 1]
        right_dist = discrete_list[ind] - _d
        res.append(discrete_list[ind - 1] if left_dist < right_dist else discrete_list[ind])
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
    # 配置
    start_time = datetime.datetime(2014, 3, 17)
    house = 'House5'
    week_num = 6
    resolution = 0.5
    magnitude = 10**8

    # 运算
    week_data = []
    for week_num in range(week_num):
        time_span = [start_time, start_time + datetime.timedelta(days=7)]
        week_data.append(read_week_data(
            '数据集/多个家庭/{}.csv_{}_{}_{}_{}.csv_week_usage.csv'.format(house,
                                                                    time_span[0].date(),
                                                                    time_span[1].date(),
                                                                    int(time_span[0].timestamp()),
                                                                    int(time_span[1].timestamp()))))
        start_time += datetime.timedelta(days=7)

    discrete_data = []
    for d in week_data:
        r = discrete(d, resolution, magnitude)
        discrete_data.append(r)

    for i in range(len(discrete_data) - 1):
        u_d1, u_d2 = uniform_scale(discrete_data[i], discrete_data[i + 1], resolution)
        print(hellinger_distance(u_d1, u_d2), end='\t')
