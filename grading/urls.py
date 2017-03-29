from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^grading/score_table/$',
        views.ScoreingSheetsView.as_view(),
        name='score_table')
]
