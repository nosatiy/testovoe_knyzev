import csv

date = 'APPLICATION_DT'
pos = 'INTERNAL_ORG_ORIGINAL_RK'
amount = 'LOAN_AMOUNT'

def read_csv(file_for_read):
    with open(file_for_read) as f:
        reader = csv.DictReader(f, delimiter=';')
        return list(reader)

def write_csv(data, header):
    with open('data_out.csv', 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(header)
        for record in data:
            writer.writerow(record)

def filling_in_template(data, template):
    for record in data:
        template[record[date]][record[pos]] += float(record[amount])
        template[record[date]]['all_sum'] += float(record[amount])
    row_list = []
    for items in template.items():
        row = [items[0]]
        for val in items[1].keys():
            if val == 'all_sum':
                continue
            row.append(str(template[items[0]][val]))
            row.append("{:.2f}%".format(template[items[0]][val] / template[items[0]]['all_sum'] * 100))
        row_list.append(row)
    return row_list

def creating_tamplte(data):
    lst_with_date, lst_with_pos = set(), set()
    for record in data:
        lst_with_date.add(record[date])
        lst_with_pos.add(record[pos])
    lst_with_date = list(lst_with_date)
    lst_with_pos = list(lst_with_pos)
    lst_with_date.sort()
    lst_with_pos.sort(key= lambda kk:int(kk))
    template = {ss:{pp: 0 for pp in lst_with_pos} for ss in lst_with_date}
    for record in lst_with_date:
        template[record]['all_sum'] = 0
    template = filling_in_template(data, template)
    return template


def header_for_csv(data):
    pos = set()
    header = []
    for record in data:
        pos.add(record['INTERNAL_ORG_ORIGINAL_RK'])
    pos = list(pos)
    pos.sort(key = lambda ss: int(ss))
    for record in pos:
        header.append(record)
        header.append(record + '%')
    header.insert(0, "Date/Pos")
    return header

if __name__ == "__main__":
    try:
        data = read_csv('data.csv')
    except:
        print("Что-то пошло не так")
        exit()
    data_out = creating_tamplte(data)
    header = header_for_csv(data)
    write_csv(data_out, header)
    print("Проверьте файл data_out.csv")

