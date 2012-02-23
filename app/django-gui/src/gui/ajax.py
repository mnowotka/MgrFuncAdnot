import os, sys
import logging

from django.utils import simplejson
from django.conf import settings

from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register

from gui.models import Task, Subtask
from gui.sequenceParsers import SequenceParcingFactory

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger = logging.getLogger("dajaxice")
logger.addHandler(ch)

#-------------------------------------------------------------------------------

@dajaxice_register
def dajaxice_example(request):
    return simplejson.dumps({'message':'Hello from Python!'})

#-------------------------------------------------------------------------------

@dajaxice_register
def startTask(request, name):
    try:
    
        task = Task.objects.get(task_name=name)
        if task.paused:
            if task.seq_file and task.subtask_set.count() == 0:
                logger.debug("we have to read from file")
                filename = os.path.join(settings.MEDIA_ROOT ,task.seq_file.name)
                if not os.path.isfile(filename):
                  raise Exception, "file " + filename + " not found."
                fName, fExt= os.path.splitext(filename)
                format = fExt[1:].lower()
                factory = SequenceParcingFactory()
                parser = factory.getParser(format)
                sequences = parser.parse(task.seq_file.read())
                for seq in sequences:
                    subtask = Subtask()
                    subtask.task = task
                    subtask.seq_format = format[0].upper()
                    subtask.sequence = seq
                    subtask.save()
            else:
                paused = task.subtask_set.filter(paused = True)
                for subtask in paused:
                    subtask.paused = False
        
        return simplejson.dumps({'title' : 'Success','type':'info', 'message':'task ' + name + ' started.'})
      
    except Exception, msg:
        return simplejson.dumps({'title' : 'Error', 'type':'error', 'message': msg})      

#-------------------------------------------------------------------------------

@dajaxice_register
def stopTask(request, name):

    try:
      task = Task.objects.get(task_name=name)
      subtasks = task.subtask_set.all()
      for subtask in subtasks:
          if subtask.finished:
              subtask.rawresult.delete()
          subtask.paused = True
      return simplejson.dumps({'title' : 'Success', 'type':'info', 'message':'task ' + name + ' stopped.'})
      
    except Exception, msg:
        return simplejson.dumps({'title' : 'Error', 'type':'error', 'message': msg})          

#-------------------------------------------------------------------------------

@dajaxice_register
def pauseTask(request, name):
    try:
        t = Task.objects.get(task_name=name)
        subtasks = task.subtask_set.all()
        for subtask in subtasks:
            subtask.paused = True
        return simplejson.dumps({'title' : 'Success','type':'info', 'message':'task ' + name + ' paused'})
    except Exception, msg:
        return simplejson.dumps({'title' : 'Error','type':'error', 'message': msg})
        
#-------------------------------------------------------------------------------

@dajaxice_register
def deleteTask(request, name):
    try:
        t = Task.objects.get(task_name=name)
        t.delete()
        return simplejson.dumps({'title' : 'Success', 'type':'info', 'message':'task ' + name + ' deleted.'})
    except Exception, msg:
        return simplejson.dumps({'title' : 'Error', 'type':'error', 'message': msg})
        
#-------------------------------------------------------------------------------

@dajaxice_register
def getTaskProgress(request, name):
    try:
        t = Task.objects.get(task_name=name)
        return simplejson.dumps({'title' : 'Success', 'type':'info', 'message':str(t.progress)})
    except Exception, msg:
        return simplejson.dumps({'title' : 'Error', 'type':'error', 'message': msg})
        
#-------------------------------------------------------------------------------

