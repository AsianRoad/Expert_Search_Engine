# coding=utf-8
import csv
import codecs
from gensim import corpora

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
    # with open('ldac/name_id.txt','w') as expertid:
    #     for r in result.keys():
    #         expertid.write(result[r]+'$'+str(r)+'\n')
    return result

def word_id():
    dictionary = corpora.Dictionary.load('ldac/output.dict')
    dictionary_dict = dictionary.token2id
    new_dict = {v:k for k,v in dictionary_dict.items()}
    # wordid = codecs.open('ldac/word_id.txt','w','utf-8')
    # for k ,v in new_dict.items():
    #     con = str(k)+'$'+v+'\n'
    #     wordid.write(con)
    # print 'done'
    return new_dict

def read_phi():
    phi = open('ldac/phi')
    lines = phi.readlines()
    top = []
    word_top = {}
    for i in range(len(lines)):
        top.append(lines[i].split(' '))
    word = word_id()
    for k ,v in word.items():
        w_top = {}
        for i in range(len(top)):
            w_top[i] = float(top[i][k])
        # sort_w = sorted(w_top.items(),key=lambda item:item[1],reverse=True)
        word_top[v] = w_top
    return word_top


def read_theta():
    theta = open('ldac/theta')
    lines = theta.readlines()
    exp_top = {}
    expert = convert_id_name()
    r = []
    for line in lines:
        r.append(line.split(' '))
    for k,v in expert.items():
        e_top = {}
        for i in range(len(r[k])):
            e_top[i] = float(r[k][i].replace('\n',''))
        exp_top[v.decode('utf-8')] = e_top
    return exp_top


def change_ldaword():
    word_topic = {}
    word_change = []
    lda_word = open('ldac/word_topic.txt','r')
    lines = lda_word.readlines()
    for line in lines:
        word = line.split(',')[0].decode('utf-8')
        con = line.split(',')[1:]
        word_con = {}
        for c in con:
            word_con[int(c.split(':')[0])] = float(c.split(':')[1])
        word_topic[word] = word_con
    for i in word_topic:
        for j in word_topic[i]:
            word_change.append(word_topic[i][j])
    dmin = min(word_change)
    dmax = max(word_change)
    for i in word_topic:
        for j in word_topic[i]:
            word_change[i][j] = (word_change[i][j]-dmin)/(dmax-dmin)

if __name__ == '__main__':
    #a = convert_id_name()
    # with codecs.open('ldac/word_topic.txt', 'w', 'utf-8') as index_file:
    #     s = read_phi()
    #     for i in s.keys():
    #         con = i+','
    #         for j in s[i].keys():
    #             con += str(j)+':'+str(s[i][j])
    #             if j !=9:
    #                 con += ','
    #         index_file.write(con+'\n')
    # naid = {}
    # nameid = open('corpus/name_id.txt').readlines()
    # for line in nameid:
    #     name = line.split('$')[0].decode('utf-8')
    #     id = line.split('$')[1].strip()
    #     naid[name] = id
    # with codecs.open('ldac/exp_topic.txt', 'w', 'utf-8') as index_file:
    #     s = read_theta()
    #     m = 1129725
    #     for i in s.keys():
    #         if i in naid.keys():
    #             co = naid[i]
    #         else:
    #             co = m
    #             m += 1
    #         con = str(co) + ','
    #         for j in s[i].keys():
    #             con += str(j)+':'+str(s[i][j])
    #             if j != 9 :
    #                 con += ','
    #         index_file.write(con+'\n')

    change_ldaword()


    name = u'人脸识别'
    print 1