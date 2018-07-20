# coding=utf-8
from __future__ import division

import codecs
import json

import jieba



class BuildIndex:

    def __init__(self,files):
        self.result = {}
        self.filenames = files
        self.termlist = self.process_files()
        self.indices = self.regIndex()
        # self.full_index = self.fulIndex()
        # self.collection_index = self.colIndex()
        self.merge_index = self.merIndex()

    def process_files(self):
        expert_file = open(self.filenames,'r')
        file_to_terms = {}
        lines = expert_file.readlines()
        count = 0
        for line in lines:
            # file_to_terms[file] = open(file, 'r').read()
            name = line.split('$')[0].decode('utf-8')
            count += 1
            info = line.split('$')[1]
            stopwords = open('corpus/chinese_stopword.txt').read()
            file_to_terms[name] = " ".join(jieba.cut_for_search(info))
            # file_to_terms[file] = " ".join(jieba.cut_for_search(file_to_terms[file]))
            file_to_terms[name] = file_to_terms[name].split()
            file_to_terms[name] = [w for w in file_to_terms[name] if w >= u'\u4e00' and w <=u'\u9fa5' and w.encode('utf-8') not in stopwords ]
            print count
        return file_to_terms

    def index_one_expert(self,wordlist):
        file_index = {}
        for word in wordlist:
            if word in file_index.keys():
                file_index[word] += 1
            else:
                file_index[word] = 1
        return file_index


    def make_indices(self,termlist):
        total = {}
        count = 0
        for expertname in termlist.keys():
            count += 1
            print expertname,count
            total[expertname] = self.index_one_expert(termlist[expertname])


        return total

    def regIndex(self):
        return self.make_indices(self.termlist)


    def fulIndex(self):
        return self.full_frequency_index(self.indices)

    def colIndex(self):
        return self.collection_frequency_index(self.indices)

    def merIndex(self):
        return self.merge_index(self.indices)


    # def full_index(termlist):
    #     total_index = {}
    #     for expert_name in termlist:
    #         expert_word = termlist[expert_name]
    #         for term in expert_word.keys():
    #             if term in total_index.keys():
    #                 total_index[term][expert_name] = expert_word[term]
    #             else:
    #                 total_index[term] = {expert_name:expert_word[term]}
    #
    #     return total_index

    # 计算语言模型的词频索引
    def full_frequency_index(self,termlist):
        total_index = {}
        for expert_name in termlist:
            expert_word = termlist[expert_name]
            word_len = len(expert_word)
            if word_len != 0:
                for term in expert_word.keys():
                    if term in total_index.keys():
                        total_index[term][expert_name] = expert_word[term]/word_len
                    else:
                        total_index[term] = {expert_name:expert_word[term]/word_len}
        return total_index


    # 平滑索引,词在所有专家下的出现概率
    def collection_frequency_index(self,termlist):
        collection_index = {}
        term_record = {}
        collection_len = 0
        # 记录词在所有专家下出现的次数
        for expert_name in termlist:
            expert_word = termlist[expert_name]
            collection_len += len(expert_word)
            for term in expert_word.keys():
                if term in term_record.keys():
                    term_record[term] += expert_word[term]
                else:
                    term_record[term] = expert_word[term]
        for expert_name in termlist:
            expert_word = termlist[expert_name]
            for term in expert_word.keys():
                collection_index[term] = term_record[term]/collection_len
        return collection_index

    # 两个索引放一块
    def merge_index(self,termlist):
        merge_index = {}
        term_record = {}
        collection_len = 0
        count1,count2 = 0,0
        for expert_name in termlist:
            count2 += 1
            print expert_name,count2
            expert_word = termlist[expert_name]
            collection_len += len(expert_word)
            for term in expert_word.keys():
                if term in term_record.keys():
                    term_record[term] += expert_word[term]
                else:
                    term_record[term] = expert_word[term]
        for expert_name in termlist:
            count1 += 1
            print count1
            expert_word = termlist[expert_name]
            word_len = len(expert_word)
            if word_len != 0:
                for term in expert_word.keys():
                    if term in merge_index.keys():
                        merge_index[term][expert_name] = expert_word[term]/word_len
                    else:
                        merge_index[term] = {'col_fre':term_record[term] / collection_len,expert_name:expert_word[term]/word_len}
        return merge_index

    # 平滑语言模型的计算方法
    # def calculate(self,word,expert):
    #     expert_len = len(self.indices[expert])
    #     miu = 80
    #     term_frequency,collection_frequency = 0,0
    #     if word in self.full_index.keys():
    #         if expert in self.full_index[word].keys():
    #             term_frequency = self.full_index[word][expert]
    #     if word in self.collection_index.keys():
    #         collection_frequency = self.collection_index[word]
    #
    #     cal = expert_len/(expert_len+miu)
    #     probability = cal*term_frequency+(1-cal)*collection_frequency
    #     return probability

    # def language_model(self,word):
    #     result = {}
    #     for expert in self.indices.keys():
    #         result[expert] = self.calculate(word,expert)
    #     result = sorted(result.iteritems(),key=lambda item:item[1],reverse=True)
    #     return result



if __name__ == '__main__':
    # termlist = process_files('corpus/test_100.txt')
    # indices = make_indices(termlist)
    # print 1
    ma = u'马维娅'
    word = u'脑血管'
    i = BuildIndex('corpus/result.txt')
    a = i.merge_index
    print 1
    with codecs.open('corpus/lm_index.txt','w','utf-8') as index_file:
        for i in a.keys():
            st = i+','
            for s in a[i].keys():
                st += s +':'+ str(a[i][s])+','
            index_file.write(st+'\n')
            st = ''
    index_file.close()