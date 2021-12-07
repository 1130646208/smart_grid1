# -- coding: utf-8 --

# -- coding: utf-8 --
import datetime
import os


# 数据清洗，筛选出一周的数据


def gen_segment_for_time_span(time_span: list, file_name: str):
    """
    针对给定的文件，给定的时间范围生成小文件
    :return:
    """

    start_time = int(time_span[0].timestamp())
    end_time = int(time_span[1].timestamp())
    write_count = 0

    with open('{}_n_weeks_raw.csv'.format(file_name), 'a') as f1:
        with open(file_name) as f:
            while True:
                line = f.readline()
                data = line.split(',')
                if line and int(data[0]) < start_time:
                    continue
                if line and int(data[0]) > end_time:
                    break
                if not line:
                    break
                f1.write(','.join([data[0], data[1]]) + '\n')
                write_count += 1
    print('generated file: {}'.format(f1.name))
    if write_count < 100:
        print('but data poor')
    else:
        print('lines: {}'.format(write_count))


if __name__ == '__main__':
    # 配置
    start_time = datetime.datetime(2014, 3, 17)
    house = 'House5'
    week_num = 10

    # 运算
    file_name = '数据集/多个家庭/{}.csv'.format(house)
    if os.path.exists('{}_n_weeks_raw.csv'.format(file_name)):
        raise OSError("文件已存在...")
    for week_num in range(week_num):
        time_span = [start_time, start_time + datetime.timedelta(days=7)]
        gen_segment_for_time_span(time_span, file_name)
        start_time += datetime.timedelta(days=7)
