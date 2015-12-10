from django.conf.urls import url
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from . import views
from . import models

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^group/(?P<pk>[0-9]+)/$',
        views.StudentGroupDetailView.as_view(), name='group_detail'),
    url(r'^group/(?P<pk>[0-9]+)/update/$', generic.UpdateView.as_view(
        model=models.Student_Group,
        fields='__all__'), name='group_update'),
    url(r'^group/(?P<pk>[0-9]+)/delete/$', generic.DeleteView.as_view(
        model=models.Student_Group,
        success_url=reverse_lazy('groups:index')), name='group_delete'),
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
    url(r'^debate/(?P<pk>[0-9]+)/delete/$', generic.DeleteView.as_view(
            model=models.Debate_Group,
            success_url=reverse_lazy('groups:debate_index')),
        name='debate_delete'),
    url(r'^create/debate/$', generic.CreateView.as_view(
            model=models.Debate_Group,
            fields='__all__'), name='debate_create'),
    url(r'^student/(?P<pk>[0-9]+)/$',
        generic.DetailView.as_view(model=models.Student,),
        name='student_detail')
]
