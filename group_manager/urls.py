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
    url(r'azlist/date/$', views.AZListDate.as_view(),
        name='azlist'),
    url(r'azlist/(?P<date>[0-9-]+)/$', views.AZListGroup.as_view(),
        name='azlist_group'),
    url(r'azlist/csv/date/$', views.AzCsvDateView.as_view(), name='csv_date'),
    url(r'azlist/csv/(?P<date>[0-9-]+)/$', views.AzCsvGroupView.as_view(),
        name='csv_group')
]
