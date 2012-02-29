from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from gui.models import Task

#-------------------------------------------------------------------------------

@login_required(login_url='/accounts/login/')
def index(request):
    return HttpResponse("Hello, world. You're at the app index.")

#-------------------------------------------------------------------------------

def service_status(request):
    return HttpResponse()

#-------------------------------------------------------------------------------

class UserTaskListView(ListView):

    context_object_name = "task_list"
    template_name = "tasks_by_user.html"

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserTaskListView, self).dispatch(*args, **kwargs)

#-------------------------------------------------------------------------------

