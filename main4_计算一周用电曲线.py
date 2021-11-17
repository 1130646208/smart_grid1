# -- coding: utf-8 --
# 计算一周的用电量
import scipy
from scipy.integrate import simps
import datetime


def cal_integral(x, y):
    """
    定义计算离散点积分的函数
    :param x:
    :param y:
    :return:
    """
    if not x or not y:
        return 0
    return scipy.integrate.trapz(y, x)


def my_cal_integral(x, y):
    assert len(x) == len(y)
    if not x or not y:
        return 0
    res = 0
    for i in range(1, len(x)):
        res += (x[i] - x[i-1]) * y[i]
    return res


def cal_week_usage(week_file_name: str):
    """
    计算一周的用电曲线
    :return:
    """
    week_usage = []
    with open(week_file_name) as f:
        first_line = f.readline()
        start_timestamp = int(first_line.split(',')[0])
        start_date = datetime.datetime.fromtimestamp(start_timestamp)
        week_days_date = [start_date + datetime.timedelta(days=d) for d in range(0, 8)]
        week_days_timestamp = [t.timestamp() for t in week_days_date]
        x = []
        y = []
        f.seek(0)
        while True:
            line = f.readline()
            # 最后一次计算积分，读取到文件末尾触发
            if not line:
                week_usage.append(cal_integral(x, y))
                x.clear()
                y.clear()
                break
            time_usage = line.split(',')
            x_time = int(time_usage[0])
            y_usage = int(time_usage[1])
            # logic
            # 如果正在计算最后一天的，那么week_days_timestamp是空的
            if x_time >= week_days_timestamp[0]:
                week_days_timestamp.pop(0)
                week_usage.append(cal_integral(x, y))
                x.clear()
                y.clear()
            else:
                x.append(x_time)
                y.append(y_usage)
        if len(week_days_timestamp) > 1:
            print('Some days lost: {}. Try another dataset...'.
                  format([datetime.datetime.fromtimestamp(t) for t in week_days_timestamp]))
        with open(week_file_name + '_week_usage' + '.csv', 'w') as f1:
            for i in range(7):
                f1.write('{},{}\n'.format(week_days_date[i].date(), week_usage[i+1]))
            print('Generated file' + week_file_name + '_week_usage' + '.csv')


if __name__ == '__main__':
    start_time = datetime.datetime(2014, 3, 17)
    house = 'House12'

    for week_num in range(6):
        time_span = [start_time, start_time + datetime.timedelta(days=7)]
        cal_week_usage('数据集/多个家庭/{}.csv_{}_{}_{}_{}.csv'.format(house, time_span[0].date(), time_span[1].date(), int(time_span[0].timestamp()), int(time_span[1].timestamp())))
        start_time += datetime.timedelta(days=7)

    # x = [1, 2, 3, 4]
    # y = [11, 11, 11, 22]
    # print(my_cal_integral(x, y))
