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
    url(r'^Doc/$', views.Doc, name='Doc'),
    url(r'^Marks/$', views.Marks, name='Marks'),
    url(r'^Course/$', views.Course, name='Course'),
    url(r'^Uploadd/$', views.Uploadd, name='Uploadd'),
    url(r'^BulkTG/$', views.BulkTG, name='BulkTG'),
    # url(r'^IndividualTG/$', views.IndividualTG, name='IndividualTG'),
    url(r'^calculateGPA/$', views.calculateGPA, name='calculateGPA'),
    # url(r'^admin2/$', views.admin2, name='admin2'),
    # url(r'^some_view/$', views.some_view, name='some_view'),
    url(r'^pdf_gen/$',views.pdf_gen,name = 'pdf_gen'),
]

