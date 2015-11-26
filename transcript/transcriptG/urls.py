from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^validate/',views.validate,name='validate'),
    url(r'^register/$',views.register,name='register'),
    url(r'^homevalidate/',views.homevalidate,name='homevalidate'),
    url(r'^list/$', views.list, name='list'),

]

