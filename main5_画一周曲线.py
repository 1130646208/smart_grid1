# -- coding: utf-8 --

import matplotlib.pyplot as plt
import datetime


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


def draw(title, figure, *data):
    # ax = figure.add_axes([0.1, 0.1, 0.8, 0.8])
    ax = figure.add_subplot()
    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel('Power')
    ax.plot(data[0], data[1])

    plt.show()


if __name__ == '__main__':
    # 参数设定
    house = 'House12'
    base_file_name = '数据集/多个家庭/{}.csv'.format(house)
    start_time = datetime.datetime(2014, 4, 21)
    # 调用计算
    time_span = [start_time, start_time + datetime.timedelta(days=7)]
    start_time = int(time_span[0].timestamp())

    end_time = int(time_span[1].timestamp())
    full_file_name = '{}_{}_{}_{}_{}.csv_week_usage.csv'.\
        format(base_file_name, time_span[0].date(), time_span[1].date(), start_time, end_time)

    fig = plt.figure()
    xy = read_week_data(full_file_name)
    draw('{} {} to {} Power usage'.format(house, time_span[0].date(), time_span[1].date()), fig, *xy)
