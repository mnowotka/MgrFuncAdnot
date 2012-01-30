from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User)
    task_name = models.CharField(max_length=30)
    seq_file = models.FileField(upload_to='/files/', blank=True, null=True)
    def __str__( self ):
       return self.task_name

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

class RawResult(models.Model):
    subtask = models.OneToOneField(Subtask, primary_key=True)
    result = models.TextField(blank=True, null=True)
    def short_result( self ):
        return (self.result[:20] + "...")

class InferredResult(models.Model):
    subtask = models.OneToOneField(Subtask, primary_key=True)
    result = models.TextField(blank=True, null=True)
    probability = models.FloatField(blank=True, null=True)
    def short_result( self ):
        return (self.result[:20] + "...")
 

