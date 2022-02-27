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

    with open('{}_{}_weeks_raw.csv'.format(file_name, week_num), 'a') as f1:
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
    print('Append to file: {}'.format(f1.name))
    if write_count < 100:
        print('!!!!!!!!!!!!!!!But data poor!!!!!!!!!!!!')
        raise ValueError('Poor data Error.')
    else:
        print('Lines: {}'.format(write_count))


if __name__ == '__main__':
    # 配置
    houses = [
        # 'House1',
        # 'House2',
        # 'House3',
        # 'House4',
        # 'House5',
        # 'House6',
        # 'House7',
        # 'House8',
        # 'House9',
        # 'House10',
        # 'House11',
        # 'House12',
        # 'House13',
        # 'House15',
        # 'House16',
        # 'House17',
        # 'House18',
        # 'House19',
        # 'House20',
        # 'House21'
    ]
    week_num = 20

    # 运算
    for house in houses:
        file_name = '数据集/多个家庭/{}.csv'.format(house)
        start_time = datetime.datetime(2014, 3, 17)

        if os.path.exists('{}_{}_weeks_raw.csv'.format(file_name, week_num)):
            raise OSError("文件已存在...")
        for i in range(week_num):
            time_span = [start_time, start_time + datetime.timedelta(days=7)]
            try:
                gen_segment_for_time_span(time_span, file_name)
            except ValueError:
                os.remove('{}_{}_weeks_raw.csv'.format(file_name, week_num))
                print('file removed')
                break
            start_time += datetime.timedelta(days=7)
