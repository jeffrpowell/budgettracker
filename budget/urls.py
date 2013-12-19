from django.conf.urls import patterns, url

from budget import views

urlpatterns = patterns('',
    # ex: /budget/
    url(r'^$', views.index, name='index'),
    # ex: /budget/5/
    url(r'^(?P<tid>\d+)/$', views.detail, name='detail'),
    # ex: /budget/5/results/
    url(r'^(?P<tid>\d+)/results/$', views.results, name='results'),
    # ex: /budget/addtransaction/
    url(r'^addtransaction/$', views.addtransaction, name='addtransaction'),
)
