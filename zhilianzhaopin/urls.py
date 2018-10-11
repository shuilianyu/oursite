from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.zhilianzhaopin_show, name='zhilianzhaopin_show'),
    url(r'^jobs/(?P<p>[0-9]+)/$',views.JobMesView.as_view(),name='jobs'),
    url(r'^location_show/$',views.location_show,name='location_show'),
    url(r'^work_experience_show/$',views.work_experience_show,name='work_experience_show'),
    url(r'^education_show/$',views.education_show,name='education_show'),
    url(r'^wordcloud_show/$',views.wordcloud_show,name='wordcloud_show'),
    url(r'^work_detail/(?P<n>[0-9]+)/$',views.work_detail,name='work_detail'),
]
