import re
import csv

for q in range(1,10):
    i = 0
    header = []
    row = []
    file_name = str('logs/') + str(q) + '.log'
    file = open(file_name, 'r')
    file_csv = csv.writer(open('./logs/' + str(q) + '.csv', "w+"))
    for line in file:
        if i == 1:
            while True:
                m = re.search('\|\s*(.+?)\s*\|', line)
                if m is None or not re.search('^\s*$', m.group(1)) is None:
                    file_csv.writerow(header)
                    break
                m = m.group(1)
                line = line.replace(m, '')
                line = line[1:]
                m = re.sub('\|','',m)
                m = re.sub('\s','',m)
                header.append(m)
        elif re.search('^Time:.*sec$', line):
            break
        elif i > 2:
            while True:
                m = re.search('\|\s*(.+?)\s*\|', line)
                if m is None or not re.search('^\s*$', m.group(1)) is None:
                    if len(row) > 0:
                        file_csv.writerow(row)
                    row = []
                    break
                m = m.group(1)
                line = line.replace(m, '')
                line = line[1:]
                m = re.sub('\|','',m)
                m = re.sub('\s','',m)
                m = re.sub('\"','',m)
                m = re.sub('\^\^\<.*\>', '', m)
                row.append(m)

        i += 1
    file.close()
