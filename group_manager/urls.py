from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^group/(?P<pk>[0-9]+)/$',
        views.StudentGroupDetailView.as_view(), name='group_detail'),
    url(r'^student/(?P<pk>[0-9]+)/$',
        views.StudentDetailView.as_view(),
        name='student_detail'),
    url(r'schedule/$', views.ScheduleListView.as_view(), name='schedule'),
    url(r'schedule/(?P<pk>[0-9]+)/$', views.ScheduleDetailView.as_view(),
        name='schedule_detail'),
    url(r'azlist/(?P<date>[0-9-]+)/$', views.AZList.as_view(),
        name='azlist')
]
