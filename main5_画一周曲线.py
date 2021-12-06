# -- coding: utf-8 --

import datetime
from utils import plt, draw


def read_week_data(file_name):
    x = []
    y = []
    with open(file_name) as f:
        while True:
            line = f.readline()
            if not line:
                break
            else:
                xy = line.strip('\n').split(',')
                x.append(xy[0])
                y.append(float(xy[1]))
    return x, y


if __name__ == '__main__':
    # 参数设定
    house = 'House2'
    base_file_name = '数据集/多个家庭/{}.csv'.format(house)
    start_time = datetime.datetime(2014, 3, 17)
    # 调用计算
    time_span = [start_time, start_time + datetime.timedelta(days=7)]
    start_time = int(time_span[0].timestamp())

    end_time = int(time_span[1].timestamp())
    full_file_name = '{}_{}_{}_{}_{}.csv_week_usage.csv'. \
        format(base_file_name, time_span[0].date(), time_span[1].date(), start_time, end_time)

    fig = plt.figure()
    xy = read_week_data(full_file_name)
    draw('{} {} to {} Power usage'.format(house, time_span[0].date(), time_span[1].date()), fig, *xy)
