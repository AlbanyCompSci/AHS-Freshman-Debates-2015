from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views import generic
from .models import *
from .forms import *

# Create your views here.


class LoginRequiredMixin (object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class IndexView (LoginRequiredMixin, generic.ListView):
    template_name = 'group_manager/index.html'
    context_object_name = 'groups'

    def get_queryset(self):
        """Returns all groups belonging to user"""
        return Student_Group.objects.filter(teacher=self.request.user)


class GroupDetailView (generic.DetailView):
    model = Student_Group


class StudentDetailView (generic.DetailView):
    model = Student
