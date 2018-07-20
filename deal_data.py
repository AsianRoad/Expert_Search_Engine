import csv
import codecs

data_ini = []
temp_data = {}

with open('corpus/all.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            author = row['author'].decode('gbk').encode('utf-8').split(',')
            keyword =  row['key_word'].decode('gbk').encode('utf-8')+','
            abstract = row['abstract'].decode('gbk').encode('utf-8')
            title = row['title'].decode('gbk').encode('utf-8')
            paper_data = keyword+abstract+title
            print title


            for i in author:
                if i != '':
                    if i in temp_data.keys():
                        temp_data[i].append(paper_data)
                    else:
                        temp_data[i] = [paper_data]
        # temp_data['key_word'] = row['key_word']
        # temp_data['abstract'] = row['abstract']
        # temp_data['title'] = row['title']
        # data_ini.append(temp_data)
        except:
            print 'illegal multibyte sequence'


with open('corpus/result.txt','w') as tfile:
    for i in temp_data.keys():
        wdata = ''
        for j in temp_data[i]:
            wdata += j
        tfile.write(i+'$'+wdata+'\n')

tfile.close()