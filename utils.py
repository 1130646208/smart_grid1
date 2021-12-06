# -- coding: utf-8 --
import datetime
import matplotlib.pyplot as plt


def draw(title, figure, *data):
    ax = figure.add_subplot()
    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel('Power')
    ax.plot(data[0], data[1])

    plt.show()


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


def get_week_data(house, start_time, week_num):
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
    return week_data
