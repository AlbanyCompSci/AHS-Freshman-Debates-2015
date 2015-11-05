from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^group/(?P<pk>[0-9]+)/$', views.GroupDetailView.as_view(),
        name='group_detail')
]
