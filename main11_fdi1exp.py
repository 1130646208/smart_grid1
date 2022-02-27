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
    all_data = read_week_data('数据集/多个家庭/{}.csv_{}_weeks_raw.csv_week_usage.csv'.format(house, week_num))
    week_data = []
    for i in range(week_num):
        week_data.append(all_data[i * 7:i * 7 + 7])
    return week_data


def inject_error(data, inject_week: int):
    injected_data = []
    week_data = data
    for i, d in zip(range(len(week_data)), week_data):
        if i == inject_week:

            r = HDIS.discrete(FDI.inject(d, FDI.fdi4, 0, 4), resolution)
        else:
            r = HDIS.discrete(d, resolution)
        injected_data.append(r)
    return injected_data


def detect_error_type1(data, threshold: float):
    """
    检查是否有异常出现
    具体是检查是否连续两个相似度超过某阈值
    :param data:
    :param threshold:
    :return: 有异常True
    """
    for week_num in range(len(data) - 1):
        if data[week_num] > threshold and data[week_num + 1] > threshold and abs(
                data[week_num] - data[week_num + 1]) < 0.5:
            return True
    return False


def detect_error_type2(data, week_num, threshold: float):
    if data[week_num-1] > threshold or data[week_num] > threshold:
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
        'House1',
        'House2',
        'House3',
        # 'House4',
        'House5',
        'House6',
        'House7',
        'House8',
        # 'House9',
        'House10',
        # 'House11',
        'House12',
        'House13',
        'House15',
        # 'House16',
        'House17',
        'House18',
        'House19',
        # 'House20',
        'House21'
    ]
    week_num = 20
    resolution = 0.5
    # inject_week = 1
    threshold = 0.8
    # 运算
    ratios = []
    print('')
    for house in houses:
        print('{}\t'.format(house), end='')
    print('')
    for house in houses:
        err_count = 0
        for w in range(1, week_num):
            normal = discrete_all(get_all(house, week_num), resolution)
            error = inject_error(get_all(house, week_num), w)
            normal_h = cal_hellinger_distance(normal)
            error_h = cal_hellinger_distance(error)
            # print('Normal:{}'.format(normal_h))
            # print('Error:{}'.format(error_h))
            # if detect_error_type2(error_h, w, threshold) and not detect_error_type2(normal_h, w, threshold):
            if detect_error_type2(error_h, w, threshold):
                err_count += 1
                # print('**Detected error in {}---week_ind:{}'.format(house, w))
            else:
                # print('##Not detected error in {}---week_ind:{}'.format(house, w))
                pass
            # print(normal)
            # print(error)
            # print('')
        ratio = err_count / (week_num - 1)
        print('%2.2f\t' % (ratio * 100), end='')
        # print('=====================================')
        ratios.append(ratio)
    print('')
    print('【总体 检出率：{}】'.format(sum(ratios) / len(ratios)))
