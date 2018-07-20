# coding=utf-8
from __future__ import division
import jieba

class Query:

    def __init__(self,filename):
        self.filename = filename
        self.lmindex = self.read_lmindex()
        self.lmne = len(self.lmindex)

    def read_lmindex(self):
        lmindex_file = open(self.filename, 'r')
        lines = lmindex_file.readlines()
        lm_index ={}
        for line in lines:
            word_con = {}
            word = line.split(',')[0].decode('utf-8')
            con = line.split(',')[1:-1]
            for i in con:
                word_con[i.split(':')[0]] = float(i.split(':')[1])

            lm_index[word] = word_con
        return lm_index

    def cal_one_word(self,word):
        lm = self.lmindex.get(word)
        res = {}
        miu = 80
        cal = self.lmne / (self.lmne + miu)     # 引入平滑系数
        if lm != None:
            for l in lm.keys():
                if l != 'col_fre':
                    res[l] = cal*lm[l]+(1-cal)*lm['col_fre']
            res['col'] = lm['col_fre']
        return res

    def cal_rank(self,res):
        exp_list = []
        rank = {}
        for wd in res.keys():
            for r in res[wd]:
                if r not in exp_list:
                    exp_list.append(r)
        exp_list.remove('col')
        for r in exp_list:
            rank[r] = 1
            for wd in res.keys():
                if len(res[wd]) != 0 :
                 if r in res[wd]:
                    rank[r] *= res[wd][r]
                 else:
                    rank[r] *= res[wd]['col']

        return rank


    def do_query(self,text):
        temp_res = {}
        words = ' '.join(jieba.cut(text,cut_all=False)).split()
        for word in words:
            temp_res[word] = self.cal_one_word(word)
        rank = self.cal_rank(temp_res)
        return rank


if __name__ == '__main__':
    a = Query('corpus/lm_compress_index.txt')
    # test = a.cal_one_word(u'铅锡')
    text = '车用动力锂离子电池,马尔可夫决策过程,加入适量钛酸'
    # test1 = ' '.join(jieba.cut(text,cut_all=False)).split()
    # test2 = ' '.join(jieba.cut_for_search(text)).split()
    s = a.do_query(text)
    print 1


