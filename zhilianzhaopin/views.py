from django.shortcuts import render
import sqlite3
import pandas as pd
from pyecharts import Pie, Bar,WordCloud
from .models import Jobs
from django.views import View
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
import pymongo
import jieba
import re
# Create your views here.
def zhilianzhaopin_show(req):
    msg = req.POST.get('kw','')
    return render(req,'zhilianzhaopin/index.html',context={'msg':msg})


class JobMesView(View):
    def __init__(self):
        super(JobMesView,self).__init__()
        self.client = pymongo.MongoClient(host='106.12.40.6', port=27017)
        self.db = self.client.zhilianzhaopin
        self.collection = self.db.classify


    def search_city(self,city,jobs):
        if city=='全国':
            jobs = jobs
        else:
            jobs = jobs.filter(
                Q(location__icontains=city)
            )
        return jobs

    def search_wage(self,wage,jobs):
        if wage == '不限':
            jobs = jobs
        elif wage=='7k以下':
            jobs = jobs.filt全国er(
                Q(wage1__lt=7)
            )
        elif wage == '20k以上':

            jobs = jobs.filter(
                Q(wage2__gt=20)
            )
        else:
            wage_low = wage.split('-')[0].strip('k')
            wage_high = wage.split('-')[1].strip('k')
            jobs = jobs.filter((Q(wage1__lt=wage_low)&Q(wage2__gt=wage_low))|(Q(wage1__lt=wage_high)&Q(wage2__gt=wage_high)))
        return jobs

    def search_exp(self,exp,jobs):
        if exp == '工作经验' or exp == '不限':
            jobs = jobs
        else:
            jobs = jobs.filter(Q(work_experience__icontains=exp))
        return jobs

    def search_edu(self,edu,jobs):
        if edu == '学历要求' or edu == '不限':
            jobs = jobs
        else:
            jobs = jobs.filter(Q(education__icontains=edu))
        return jobs

    def search_keywords(self,search_keywords,jobs):
        if search_keywords.strip() == '':
            jobs = jobs
        else:
            jobs = jobs.filter(Q(job_title__icontains=search_keywords)|Q(job_description__icontains=search_keywords))
        return jobs

    def search_category(self,category,jobs):
        print(category)
        if category == '不限':
            return jobs
        k = self.collection.find({'category':category})
        id_list = []
        for i in k:
            id_list.append(i['_id'])
        print(id_list)

        jobs = jobs.filter(Q(id__in = id_list))
        return jobs

    def get(self,request,p=1):
        city = request.GET.get('city','全国').strip()
        wage = request.GET.get('wage','不限').strip()
        edu = request.GET.get('edu','学历要求').strip()
        exp = request.GET.get('years','工作经验').strip()
        category = request.GET.get('category', '不限').strip()
        search_keywords = request.GET.get('kw', '').strip()
        p = request.GET.get('page',1)
        jobs = Jobs.objects.all()
        jobs1 = self.search_city(city,jobs)
        jobs2 = self.search_keywords(search_keywords,jobs1)
        jobs3 = self.search_edu(edu,jobs2)
        jobs4 = self.search_exp(exp,jobs3)
        jobs5 = self.search_wage(wage,jobs4)
        jobs6 = self.search_category(category,jobs5)
        paginator = Paginator(jobs6,10)
        page_jobs = paginator.page(p)
        result_list = []
        for i in page_jobs:
            if i.wage1 == -1:
                wage = '薪资面议'
            else:
                wage = str(i.wage1)+'k-'+str(i.wage2)+'k'
            s = {'id':i.id,'job_title':i.job_title,'location':i.location,'wage':wage,'work_experience':i.work_experience,'education':i.education,'company_name':i.company_name}
            result_list.append(json.dumps(s))
        return JsonResponse({"msg":result_list,'num_page':paginator.num_pages,'page':int(p)})

def location_show(req):
    return render(req,'zhilianzhaopin/city.html')

def work_experience_show(req):
    return render(req, 'zhilianzhaopin/work_experience.html')

def education_show(req):
    return render(req, 'zhilianzhaopin/education.html')

def wordcloud_show(req):
    return render(req,'zhilianzhaopin/wordcloud.html')

def work_detail(req,n):
    job = Jobs.objects.get(id=n)
    if job.wage1 == -1:
        job.wage1 = '薪资面议'
    else:
        job.wage1 = str(job.wage1)+'k-'+str(job.wage2)+'k'
    return render(req,'zhilianzhaopin/work_detail.html',context={'msg':job})

class views(object):
    def __init__(self):
        self.coon = sqlite3.connect('db.sqlite3')
        self.df = pd.read_sql_query('select * from zhilianzhaopin_jobs',self.coon)

    def work_experience(self):
        '''
        生成工作经验图标
        :return:
        '''
        a = list(self.df[self.df['work_experience']!=''].loc[:,['work_experience']].groupby(['work_experience']).size())
        b =  self.df[self.df['work_experience']!=''].loc[:,['work_experience']].groupby(['work_experience']).size().index.values
        pie = Pie("工作经验饼状视图")
        pie.add("工作年限", b,a, is_label_show=True)
        pie.render('templates/zhilianzhaopin/work_experience.html')


    def education(self):
        '''
        生成学历图标
        :return:
        '''
        a = list(
            self.df[self.df['education'] != ''].loc[:, ['education']].groupby(['education']).size())
        b = self.df[self.df['education'] != ''].loc[:, ['education']].groupby(
            ['education']).size().index.values
        pie = Pie("学历要求饼状视图")
        pie.add("学历要求", b, a, is_label_show=True)
        pie.render('templates/zhilianzhaopin/education.html')

    def location(self):
        '''
        生成城市图表
        :return:
        '''
        a = list(self.df[self.df['location']!=''].loc[:,['location']].groupby(['location']).size())
        b =  list(self.df[self.df['location']!=''].loc[:,['location']].groupby(['location']).size().index.values)
        num = len(a)
        for i in range(num):
            if a[num - i - 1] < 20:
                a.pop(num - i -1)
                b.pop(num - i -1)
        bar=Bar('示例')
        bar.add('',b,a,is_label_show=True,is_datazoom_show=True)
        bar.use_theme('dark')
        bar.render(path='templates/zhilianzhaopin/city.html')

