# coding=utf-8
import pickle

import jieba
from gensim import corpora

from gensim.models import AuthorTopicModel
from gensim.corpora import Dictionary
import csv

def read_data():
    stopwords = open('corpus/chinese_stopword.txt').read()
    author2doc1= dict()
    author2doc2= dict()
    docs1 = []
    docs2 = []
    pid = 0
    with open('corpus/all.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:

            try:
                author = row['author'].decode('gbk').split(',')
                keyword =  row['key_word'].decode('gbk').encode('utf-8')+','
                abstract = row['abstract'].decode('gbk').encode('utf-8')
                title = row['title'].decode('gbk').encode('utf-8')
                paper_data = keyword+abstract+title
                #print title
                if pid <= 18000:
                    for i in author:
                        if i != '':
                            if author2doc1.get(i):
                                author2doc1[i].append(pid)
                            else:
                                author2doc1[i] = [pid]
                else:
                    for i in author:
                        if author2doc2.get(i):
                            author2doc2[i].append(pid)
                        else:
                            author2doc2[i] = [pid]
                if pid <= 18000:
                    clean = " ".join(jieba.cut(paper_data, cut_all=False))
                    clean = clean.split()
                    clean =  [w for w in clean if w >= u'\u4e00' and w <=u'\u9fa5' and w.encode('utf-8') not in stopwords]
                    docs1.append(clean)
                else:
                    clean = " ".join(jieba.cut(paper_data, cut_all=False))
                    clean = clean.split()
                    clean =  [w for w in clean if w >= u'\u4e00' and w <=u'\u9fa5' and w.encode('utf-8') not in stopwords]
                    docs2.append(clean)
                pid += 1
            except:
                print 'illegal multibyte sequence'
    return author2doc1,docs1,author2doc2,docs2



def creat_model(author2doc1,docs1,author2doc2,docs2):
    docs = docs1+docs2
    dictionary = Dictionary(docs)
    max_freq = 0.3
    min_wordcount = 2
    dictionary.filter_extremes(no_below=min_wordcount,no_above=max_freq)


    _ = dictionary[0]
    dictionary.save('model/atdc.dict')
    corpus1 = [dictionary.doc2bow(doc) for doc in docs1]
    corpus2 = [dictionary.doc2bow(doc) for doc in docs2]

    print('Number of authors1: %d' % len(author2doc1))
    print('Number of authors2: %d' % len(author2doc2))
    print('Number of unique tokens: %d' % len(dictionary))
    print('Number of documents1: %d' % len(corpus1))
    print('Number of documents2: %d' % len(corpus2))

    return corpus1,corpus2,dictionary


def run_model(corpus1,corpus2,dictionary,author2doc1,author2doc2):

    model = AuthorTopicModel(corpus=corpus1,num_topics=10,id2word=dictionary.id2token,
                             author2doc=author2doc1,chunksize=2000, passes=1, eval_every=0,serialized=True,
                             iterations=1, random_state=1,serialization_path='tmp/corpus1.mm')
    model.update(corpus=corpus2,author2doc=author2doc2)
    model.save('model/at_all.atmodel')

def show():
    model = AuthorTopicModel.load('model/at_all.atmodel')

    author_list = model.id2author.values()
    t_res=[[]for i in range(10)]

    for a in author_list:
        res = model.get_author_topics(a,minimum_probability=0.0)
        for i in range(10):
            t_res[i].append((a,res[i][1]))

    res = []
    for i in range(10):
        res.append(sorted(t_res[i], key=lambda item: item[1], reverse=True)[:6])
    # for topic in model.show_topics(num_topics=10):
    #     print('Label: ')
    #     words = ''
    #     for word, prob in model.show_topic(topic[0]):
    #         words += word + ' '
    #     print('Words: ' + words)
    for i in range(len(res)):
        print 'topic'+str(i)
        for j in res[i]:
            print j[0],"%.6f" %(j[1]/2974)


def ver():
    # 每词单词边界指标
    model = AuthorTopicModel.load('model/at_all.atmodel')
    dictionary = Dictionary.load('model/atdc.dict')
    from gensim.models.coherencemodel import CoherenceModel

    atcm = CoherenceModel(model,corpus=model.corpus,dictionary=dictionary,coherence='u_mass')
    print atcm.get_coherence()


    # Compute the per-word bound.
    # Number of words in corpus.
    # corpus_words = sum(cnt for document in model.corpus for _, cnt in document)
    #
    # # Compute bound and divide by number of words.
    # perwordbound = model.bound(model.corpus, author2doc=model.author2doc,
    #                            doc2author=model.doc2author) / corpus_words
    # print(perwordbound)

    # 话题一致性指标计算



if __name__ == "__main__":
    #author2doc1,docs1,author2doc2,docs2 = read_data()
    #pickle.dump(author2doc,open('corpus/author2doc.dic','w'))
    #corpus1,corpus2,dictionary = creat_model(author2doc1,docs1,author2doc2,docs2)
    # model = run_model(corpus1,corpus2,dictionary,author2doc1,author2doc2)
    ver()