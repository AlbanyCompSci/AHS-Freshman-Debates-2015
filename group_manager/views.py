from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import generic
from .models import *

# Create your views here.


"""@login_required
def index(request):
    my_groups = Student_Group.objects.filter(teacher=request.user)
    return render(request, 'group_manager/index.html', {'groups': my_groups})"""

@login_required
class IndexView (generic.ListView):
    template_name = 'group_manager/index.html'
    context_object_name = 'my_groups'

    def get_queryset (self):
        """Returns all groups belonging to user"""
        return Student_Group.objects.filter(teacher=self.request.user)
