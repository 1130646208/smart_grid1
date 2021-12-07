# -- coding: utf-8 --

from hdis import HDIS
from utils import *
from fdi import FDI


def discrete_all(data, resolution):
    week_data = data

    discrete_data = []
    for d in week_data:
        r = HDIS.discrete(d, resolution)
        discrete_data.append(r)
    return discrete_data


def get_all(house, week_num):
    all_data = read_week_data('数据集/多个家庭/{}.csv_n_weeks_raw.csv_week_usage.csv'.format(house))
    week_data = []
    for i in range(week_num):
        week_data.append(all_data[i * 7:i * 7 + 7])
    return week_data


def inject_error(data, inject_week: int):
    injected_data = []
    week_data = data
    for i, d in zip(range(len(week_data)), week_data):
        if i == inject_week:
            r = HDIS.discrete(FDI.inject(d, FDI.fdi1, 0.5), resolution)
        else:
            r = HDIS.discrete(d, resolution)
        injected_data.append(r)
    return injected_data


def detect_error(data, threshold: float):
    """
    检查是否有异常出现
    :param data:
    :param threshold:
    :return: 有异常True
    """
    maxi = max(data)
    if maxi > threshold:
        return True
    return False


def cal_hellinger_distance(discrete_data: list):
    res = []
    for i in range(len(discrete_data) - 1):
        u_d1, u_d2 = HDIS.uniform_scale(discrete_data[i], discrete_data[i + 1], resolution)
        res.append(HDIS.hellinger_distance(u_d1, u_d2))
    return res


if __name__ == '__main__':
    # 配置
    start_time = datetime.datetime(2014, 3, 17)
    houses = [
        # 'House1',
        # 'House2',
        # 'House3',
        # 'House4',
        'House5',
        # 'House6',
        # 'House7',
        # 'House8',
        # 'House9',
        # 'House10',
        # 'House11',
        # 'House12',
        # 'House13',
        # 'House14',
        # 'House15',
        # 'House16',
        # 'House17',
        # 'House18',
        # 'House19',
        # 'House20'
    ]
    week_num = 10
    resolution = 0.6
    err_count = 0
    # 运算
    for house in houses:
        normal = discrete_all(get_all(house, week_num), resolution)
        error = inject_error(get_all(house, week_num), 3)
        normal_h = cal_hellinger_distance(normal)
        error_h = cal_hellinger_distance(error)
        if detect_error(error_h, 0.9):
            err_count += 1
        print(normal)
        print(error)
        print(normal_h)
        print(error_h)
    print(err_count / len(houses))

    # for i in range(len(discrete_data) - 1):
    #     u_d1, u_d2 = HDIS.uniform_scale(discrete_data[i], discrete_data[i + 1], resolution)
    #     print(HDIS.hellinger_distance(u_d1, u_d2), end='\t')
