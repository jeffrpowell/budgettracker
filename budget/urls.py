from django.conf.urls import patterns, url

from budget import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^date/(?P<month>\w+)/(?P<year>\d+)/$', views.index, name='index'),
    
    url(r'^alltransactions/$', views.alltransactions, name='alltransactions'),
    url(r'^transaction/(?P<tid>\d+)/(?P<aid>\d+)/$', views.transaction, name='transaction'),
    url(r'^addtransaction/(?P<to_account>\d+)/$', views.addtransaction, name='addtransaction'),
	url(r'^addtransactions/$', views.addtransactions, name='addtransactions'),
    url(r'^banktransaction/$', views.banktransaction, name='banktransaction'),
	url(r'^transaction/delete/(?P<tid>\d+)/$', views.transaction_delete, name='transactiondelete'),
    
    url(r'^account/(?P<aid>\d+)/$', views.account, name='account'),
    url(r'^account/(?P<aid>\d+)/subaccount/$', views.addsubaccount, name='addsubaccount'),
    url(r'^account/(?P<aid>\d+)/date/(?P<month>\w+)/(?P<year>\d+)/$', views.account, name='account'),
    url(r'^account/add/(?P<cid>\d+)/$', views.addaccount, name='addaccount'),
    url(r'^account/edit/(?P<aid>\d+)/$', views.editaccount, name='editaccount'),
    url(r'^account/delete/(?P<aid>\d+)/$', views.deleteaccount, name='deleteaccount'),
    
    url(r'^category/(?P<cid>\d+)/$', views.category, name='category'),
    
    ### AJAX URLS ###
    url(r'^projection/$', views.set_projection, name='set_projection'),
)
