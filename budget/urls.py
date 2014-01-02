from django.conf.urls import patterns, url

from budget import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^transaction/(?P<tid>\d+)/$', views.transaction, name='transaction'),
    url(r'^account/(?P<aid>\d+)/$', views.account, name='account'),
    url(r'^addtransaction/$', views.addtransaction, name='addtransaction'),
    url(r'^addtransaction/(?P<to_account>\d+)/$', views.addtransaction, name='addtransaction'),
    url(r'^category/(?P<cid>\d+)/$', views.category, name='category'),
    
    ### AJAX URL ###
    url(r'^projection/$', views.set_projection, name='set_projection'),
)
