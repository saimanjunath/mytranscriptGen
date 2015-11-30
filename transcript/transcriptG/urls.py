from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^validate/',views.validate,name='validate'),
    url(r'^register/$',views.register,name='register'),
    url(r'^homevalidate/',views.homevalidate,name='homevalidate'),
    url(r'^courseList/$', views.courseList, name='courseList'),
    url(r'^studentMarkslist/$', views.studentMarkslist, name='studentMarkslist'),
    url(r'^list/$', views.list, name='list'),
    url(r'Doc/$', views.Doc, name='Doc'),
    url(r'Marks/$', views.Marks, name='Marks'),
    url(r'Course/$', views.Course, name='Course'),
    url(r'upload/$', views.upload, name='upload'),
]

