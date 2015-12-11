from django.conf.urls import url
from django.views import generic
from . import views
from . import models

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^group/(?P<pk>[0-9]+)/$',
        views.StudentGroupDetailView.as_view(), name='group_detail'),
    url(r'^group/(?P<pk>[0-9]+)/delete/$',
        views.StudentGroupDelete.as_view(), name='group_delete'),
    url(r'^create/(?P<teacher>[0-9]+)/group/$',
        views.StudentGroupPeriodSelect.as_view(),
        name='student_group_period_select'),
    url(r'^create/(?P<teacher>[0-9]+)/(?P<periods>[1-7]+)/group/$',
        views.StudentGroupCreate.as_view(), name='student_group_form'),
    url(r'^debate/$', generic.ListView.as_view(model=models.Debate_Group),
        name='debate_index'),
    url(r'^debate/(?P<pk>[0-9]+)/$',
        generic.DetailView.as_view(model=models.Debate_Group),
        name='debate_detail'),
    url(r'^debate/(?P<pk>[0-9]+)/delete/$',
        views.DebateGroupDelete.as_view(), name='debate_delete'),
    url(r'^create/debate/$',
        views.DebateGroupCreate.as_view(), name='debate_create'),
    url(r'^student/(?P<pk>[0-9]+)/$',
        generic.DetailView.as_view(model=models.Student,),
        name='student_detail')
]
