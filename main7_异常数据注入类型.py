# -- coding: utf-8 --
import random

def fdi1(origin_data, factor):
    """
    总体成比例减小
    :param origin_data:
    :param factor:
    :return:
    """
    assert 0 < factor < 1
    return [i * factor for i in origin_data]


def fdi2(origin_data, cutoff_point):
    """
    削峰
    :param origin_data:
    :param cutoff_point:
    :return:
    """
    return [cutoff_point if i > cutoff_point else i for i in origin_data]


def fdi3(origin_data, sub_value):
    """
    总体减小sub_value
    :param origin_data:
    :param sub_value:
    :return:
    """
    return [i - sub_value if i - sub_value > 0 else 0 for i in origin_data]


def fdi4(origin_data, l_bound, r_bound):
    """
    将某段时间直接抹零
    :param origin_data:
    :param l_bound:
    :param r_bound:
    :return:
    """
    return [0 if l_bound <= i <= r_bound else origin_data[i] for i in range(len(origin_data))]


def fdi6(origin_data, range_factor_l, range_factor_r):
    assert 0 <= range_factor_l < range_factor_r <= 1
    rand_list = []
    rand = random.random()
    while True:
        if range_factor_l <= rand <= range_factor_r:
            rand_list.append(rand)
            rand = random.random()
            if len(rand_list) == len(origin_data):
                break
        else:
            rand = random.random()
    ave = sum(origin_data) / len(origin_data)
    return [ave * rand_list[i] for i in range(len(origin_data))]


if __name__ == '__main__':
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(fdi1(data, 0.6))
    print(fdi2(data, 6))
    print(fdi3(data, 5))
    print(fdi4(data, 0, 3))
    print(fdi6(data, 0.4, 0.6))
