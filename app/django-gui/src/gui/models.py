import math

from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

#------------------------------------------------------------------------------

class Task(models.Model):
    user = models.ForeignKey(User)
    task_name = models.CharField(max_length=30)
    seq_file = models.FileField(upload_to='files/', blank=True, null=True)
    def getSubtasksCount(self):
       return self.subtask_set.count()
    def getFileName(self):
       return self.seq_file.name
    def getProgress(self):
      al = self.getSubtasksCount()
      completed =  reduce(lambda x,y: x+y, map(lambda x : 1 if x.finished else 0, self.subtask_set.all()))
      return int(math.floor(float(completed)/al * 100)) 
    def __str__( self ):
       return self.task_name
    subtasks = property(getSubtasksCount)
    progress = property(getProgress)
    filename = property(getFileName)   

#------------------------------------------------------------------------------

class TaskForm(ModelForm):
    class Meta:
        model = Task

#------------------------------------------------------------------------------

class Subtask(models.Model):
    FORMAT_CHOICES = (
        (u'F', u'FASTA'),
        (u'G', u'GenBank'),
    )
    task = models.ForeignKey(Task)
    seq_format = models.CharField(max_length=4, choices=FORMAT_CHOICES)
    sequence = models.TextField()
    def short_seq( self ):
        return (self.sequence[:20] + "...")
    def finished( self ):
        try:
            self.rawresult
            return True
        except RawResult.DoesNotExist:
            return False
    finished = property(finished)           

#------------------------------------------------------------------------------

class SubtaskForm(ModelForm):
    class Meta:
        model = Subtask

#------------------------------------------------------------------------------

class RawResult(models.Model):
    subtask = models.OneToOneField(Subtask, primary_key=True)
    result = models.TextField(blank=True, null=True)
    def short_result( self ):
        return (self.result[:20] + "...")

#------------------------------------------------------------------------------

class RawResultForm(ModelForm):
    class Meta:
        model = RawResult

#------------------------------------------------------------------------------

class InferredResult(models.Model):
    subtask = models.OneToOneField(Subtask, primary_key=True)
    result = models.TextField(blank=True, null=True)
    probability = models.FloatField(blank=True, null=True)
    def short_result( self ):
        return (self.result[:20] + "...")

#------------------------------------------------------------------------------
 
class InferredResultForm(ModelForm):
    class Meta:
        model = InferredResult

#------------------------------------------------------------------------------

