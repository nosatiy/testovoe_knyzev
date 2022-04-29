import matplotlib.pyplot as plt
import pandas as pd

pos_del = ['-1 - 4914',
        '4915 - 15210',
        '15219 - 19962',
        '20078 - 32857',
        '32858 - 46516',
        '46573 - 49201',
        '49204 - 50319',
        '50321 - 51928',
        '51929 - 57844',
        '57845 - 61904']

def add_str_date(data):
    ret = []
    for ss in data['Date/Pos']:
        ret.append(str(ss).split(' ')[0])
    data.insert(1, 'date', ret)

def calculate_amount(data, len_col, key):
    rows_lst = [[] for ss in range(len_col)]
    range_part = (len(data.columns) - 1) / 2 / 10
    number_part = 0
    part_sum = 0
    stop_for_next_sum = 0
    stop_for_next_lst = 0
    if key == 1:
        type_val = float
    else:
        type_val = str

    for row in data.itertuples(index=False):
        for value in row:
            if type(value) == type_val:
                if type_val == str and '%' in value:
                    value_str = value[:-1]
                    part_sum += float(value_str)
                elif type_val == float:
                    part_sum += float(value)
                else:
                    continue
                stop_for_next_sum += 1
                if stop_for_next_sum >= range_part:
                    rows_lst[number_part].append(part_sum)
                    stop_for_next_sum = 0
                    stop_for_next_lst += 1
                    part_sum = 0
                    if stop_for_next_lst == 10:
                        number_part += 1
                        stop_for_next_lst = 0

    dt = pd.DataFrame(rows_lst, columns=pos_del, index=data.index)
    data = pd.concat([data, dt], axis=1)
    return data

if __name__ == '__main__':
    plt.rcParams['figure.figsize'] = (17,10)
    plt.rcParams["axes.formatter.limits"] = (-3, 10000)
    colors=['#0450B4', '#046DC8', '#1184A7', '#15A2A2', '#6FB1A0', '#FEA802', '#FE7434', '#CC1928', '#D94A8C', '#5D094A']

    try:
        data = pd.read_csv('data_out.csv', delimiter=';')
    except:
        print("Что-то пошло не так")
        exit()
    data['Date/Pos'] = pd.to_datetime(data['Date/Pos'])
    add_str_date(data)
    data.set_index('Date/Pos', inplace=True)

    data_for_abs = calculate_amount(data, len(data.index), 1)
    data_for_per = calculate_amount(data, len(data.index), 2)

    ax = data_for_abs.plot(x='date', y=pos_del, kind='bar', stacked=True, color=colors)
    ax.set_xlabel('Дата')
    ax.set_ylabel('Сумма выдач')
    ax.set_xticklabels(data['date'], rotation=60)
    plt.ylim (0, 70000000)
    plt.savefig('img/absolut.png')
    print('Файл с абсолютными величинами: absolut.png')

    ax = data_for_per.plot(x='date', y=pos_del, kind='bar', stacked=True, color=colors)
    ax.set_facecolor('#000000')
    ax.set_xlabel('Дата')
    ax.set_ylabel('Процент выдач')
    ax.set_xticklabels(data['date'], rotation=60)
    plt.ylim (0, 145)
    plt.savefig('img/percent.png')
    print('Файл с процентным соотношением: percent.png')

