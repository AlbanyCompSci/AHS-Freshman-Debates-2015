from django.conf.urls import url
from django.views import generic
from . import views
from . import models

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^group/(?P<pk>[0-9]+)/$',
        generic.DetailView.as_view(model=models.Student_Group),
        name='group_detail'),
    url(r'^student/(?P<pk>[0-9]+)/$',
        generic.DetailView.as_view(model=models.Student),
        name='student_detail'),
    url(r'^create/(?P<teacher>[0-9]+)/group/$',
        views.StudentGroupPeriodSelect, name='student_group_period_select'),
    url(r'^create/(?P<teacher>[0-9]+)/(?P<periods>[1-7]+)/group/$',
        views.StudentGroupCreate.as_view(), name='student_group_form'),
    url(r'^debate/(?P<pk>[0-9]+)/$',
        generic.DetailView.as_view(model=models.Debate_Group),
        name='debate_detail'),
    url(r'^create/debate/$', generic.CreateView.as_view(
            model=models.Debate_Group,
            fields='__all__'), name='debate_create'),
    url(r'^debate/$', generic.ListView.as_view(model=models.Debate_Group),
        name='debate_index')
]
