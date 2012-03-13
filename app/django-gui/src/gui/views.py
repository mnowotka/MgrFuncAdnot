from StringIO import StringIO  
from zipfile import ZipFile
import datetime

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.utils.encoding import smart_unicode, smart_str

from gui.models import Task, Monitor, Subtask

#-------------------------------------------------------------------------------

@login_required(login_url='/accounts/login/')
def index(request):
    return HttpResponse("Hello, world. You're at the app index.")

#-------------------------------------------------------------------------------

@login_required(login_url='/accounts/login/')
def results(request):

#    try:

    in_memory = StringIO()  
    zip = ZipFile(in_memory, "a")
    name = str(request.REQUEST['name'])
    format = Task.objects.get(task_name=name).tasksettings.out_format
    
    for idx, subtask in enumerate(Subtask.objects.filter(task__task_name=name).exclude(rawresult=None)):
      filename = name + "_" + str(idx) + '.' + format
      zip.writestr(filename.encode('utf-8'), subtask.rawresult.result.encode('utf-8'))  
      
    # fix for Linux zip files read in Windows  
    for file in zip.filelist:  
        file.create_system = 0      
          
    zip.close()  

    response = HttpResponse(mimetype="application/zip")  
    response["Content-Disposition"] = "attachment; filename=results.zip"  
      
    in_memory.seek(0)      
    response.write(in_memory.read())
      
#    except Exception, e:
        #self._logger.error(str(e))
#        response  = HttpResponse(str(e))
      
    return response  

#-------------------------------------------------------------------------------

@csrf_exempt
def service_status(request):
    f = open('/home/mnowotka/Dokumenty/MgrFuncAdnot/app/django-gui/request.txt','a')
    f.write("--->" + str(request.REQUEST) + "<----")
    f.close()
    for msg in eval(request.REQUEST[u'message']):
        monit = Monitor()
        monit.when = msg[0]
        monit.status = msg[1]
        if msg[2]:
            monit.who = msg[2][0]         
            monit.what = msg[2][1] 
        monit.save()
    return HttpResponse()

#-------------------------------------------------------------------------------

def monitor(request):
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

