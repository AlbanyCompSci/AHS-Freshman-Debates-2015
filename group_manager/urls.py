from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^group/(?P<pk>[0-9]+)/$', views.GroupDetailView.as_view(),
        name='group_detail'),
    url(r'^student/(?P<pk>[0-9]+)/$', views.StudentDetailView.as_view(),
        name='student_detail'),
    url(r'^create/(?P<teacher>[0-9]+)/group/$',
        views.StudentGroupPeriodSelect, name='student_group_period_select'),
    url(r'^create/(?P<teacher>[0-9]+)/(?P<periods>[1-7]+)/group/$',
        views.StudentGroupCreate.as_view(), name='student_group_form')
]
