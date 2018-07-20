# coding=utf-8
import csv

def convert_id_name():
    """将作者名字与作者id映射起来"""
    csvFile = open('ldac/test2.csv','r')
    idFile = open('ldac/author_id.id','r')
    idreader = idFile.readlines()
    reader = csv.reader(csvFile)
    result = {}
    name = []
    id = []
    for item in reader:
        if reader.line_num == 1:
            continue
        name.append(item[0].split(','))
    csvFile.close()
    for item in idreader:
        id.append(item.replace(',\n','').split(','))
    for i in range(len(id)):
        for j in range(len(id[i])):
            if id[i][j] not in result.keys():
                result[int(id[i][j])] = name[i][j]

    return result

if __name__ == '__main__':
    a = convert_id_name()
    print 1