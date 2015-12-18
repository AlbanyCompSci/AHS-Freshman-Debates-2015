from django.conf.urls import url
from django.views import generic
from . import views
from . import models

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^group/(?P<pk>[0-9]+)/$',
        views.StudentGroupDetailView.as_view(), name='group_detail'),
    url(r'^student/(?P<pk>[0-9]+)/$',
        views.StudentDetailView.as_view(),
        name='student_detail'),
    url(r'schedule/$', generic.ListView.as_view(
        model=models.Schedule), name='schedule'),
    url(r'schedule/(?P<pk>[0-9]+)/$', views.ScheduleDetailView.as_view(),
        name='schedule_detail')
]
