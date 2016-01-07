from django.conf.urls import url
from django.contrib.auth.views import login, logout
from . import views

app_name = 'polls'
urlpatterns = [
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    url(r'upload', views.upload_file, name='upload'),
    # ex: /polls/5/
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^registration/',  views.register),
    url(r'^accounts/login/$',  login),
    url(r'^accounts/logout/$', logout)
]
