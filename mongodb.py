from pyecharts import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
import jieba
import pymongo
#连接数据库
import sqlite3
import re

class ZhilianTfidf(object):

    def __init__(self):

        self.coon = sqlite3.connect("db.sqlite3")
        self.cursor = self.coon.cursor()
        self.targetname_path = './targetname'
        self.df = pd.read_sql_query('select * from zhilianzhaopin_jobs where id <={}'.format(len(self.targetname_list(self.targetname_path))), self.coon)
        self.df_test = pd.read_sql_query('select * from zhilianzhaopin_jobs where id > {}'.format(len(self.targetname_list(self.targetname_path))), self.coon)
        self.client = pymongo.MongoClient(host='localhost', port=27017)
        self.db = self.client.zhilianzhaopin
        self.collection = self.db.classify
    def get_data(self,df):
        data_list=[]
        for df_one in df.loc[:,'job_description']:
            data_list.append(df_one)
        return data_list

    def get_id(self,df):
        id_list = []
        for df_one in df.loc[:,'id']:
            id_list.append(df_one)
        return id_list


    def cutword(self,data_list):
        rusult_list = []
        for i in data_list:
            rusult_list.append(" ".join(list(jieba.cut(i))))
        return rusult_list

    def targetname_list(self,filepath):
        targetname_list = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
        return targetname_list

    def tfifvec(self):
        '''
        中文特征值化
        #TF(词频) :在一篇文章中出现该词与文章中总词数的比值 出现次数/文章总词数
        #IDF逆向词频 log(文章的总数/该词出现的文章数)
        :return: None
        '''
        for doc, category in zip([i+1 for i in range(len(self.targetname_list(self.targetname_path)))], self.targetname_list(self.targetname_path)):
            self.collection.update({"_id": doc}, {"$set": {"_id": doc,'category':category}}, upsert=True)
        tfidf_tranformer = TfidfVectorizer()
        X_train_tfidf = tfidf_tranformer.fit_transform(self.cutword(self.get_data(self.df)))
        clf = MultinomialNB(alpha=1.0).fit(X_train_tfidf, self.targetname_list(self.targetname_path))
        docs_new = self.cutword(self.get_data(self.df_test))
        X_new_tfidf = tfidf_tranformer.transform(docs_new)
        predicted = clf.predict(X_new_tfidf)
        id_list = self.get_id(self.df_test)

        for doc, category in zip(id_list, predicted):
            self.collection.update({"_id": doc}, {"$set": {"_id": doc, 'category': category}}, upsert=True)
    def mongo_find(self):
        k = self.collection.find({'category':'前端开发'})
        for i in k:
            print(i['_id'])
    def mongo_drop(self):
        self.collection.drop()







def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords

class wordcould(object):
    '''
    生成词云
    '''
    def __init__(self):
        self.coon = sqlite3.connect('db.sqlite3')
        self.df = pd.read_sql_query('select * from zhilianzhaopin_jobs', self.coon)
        self.client = pymongo.MongoClient(host='localhost', port=27017)
        self.db = self.client.zhilianzhaopin
        self.collection = self.db.jobs


    def make_wordcould(self):
        a = self.collection.find()
        key_list = []
        count_list = []
        for i in a:
            if i['_id'] not in stopwordslist('zhilianzhaopin/stopwords_two'):
                key_list.append(i['_id'])
                count_list.append(i['count'])
        wd = WordCloud(width=1300, height=620)

        wd.add('', key_list, count_list, word_size_range=(20, 100))
        wd.render('templates/zhilianzhaopin/wordcloud.html')

    def cut_word(self):
        for df_one in self.df['job_description']:
            for i in jieba.cut(df_one):
                if i not in stopwordslist('./stopwords') and i.strip() and not re.search(r'([0-9]+|[a-z]+|[A-Z]+)+', i):
                    result_find = self.collection.find_one({"_id": i})
                    if result_find:
                        count = result_find['count'] + 1
                        data_update = {"_id": i, 'count': count}
                        self.collection.update({"_id": i}, {"$set": data_update}, upsert=True)
                    else:
                        data = {"_id": i, 'count': 1}
                        self.collection.insert(data)


z = ZhilianTfidf()
z.tfifvec()

w = wordcould()
w.cut_word()