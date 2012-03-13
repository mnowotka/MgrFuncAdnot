import math
import pickle
from cStringIO import StringIO

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

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
    def isPaused(self):
        return (self.subtask_set.count() == 0 or self.subtask_set.filter(paused = True).count() != 0)
    def getProgress(self):
        al = self.getSubtasksCount()
        completed =  reduce(lambda x,y: x+y, map(lambda x : 1 if x.finished else 0, self.subtask_set.all()))
        return int(math.floor(float(completed)/al * 100)) 
    def __str__( self ):
        return self.task_name
    paused = property(isPaused)   
    subtasks = property(getSubtasksCount)
    progress = property(getProgress)
    filename = property(getFileName)   

#------------------------------------------------------------------------------

class TaskForm(ModelForm):
    class Meta:
        model = Task

#------------------------------------------------------------------------------

class TaskSettings(models.Model):
    JOB_CHOICES = (
      (u'N', u'No job'),
      (u'Cmpl', u'Complement'),
      (u'RvCm', u'Reverse Complement'),
      (u'Trb', u'Transcribe'),
      (u'BTrb', u'Back transcribe'),
      (u'Trlt', u'Translate'),
      (u'Blst', u'BLAST'),
    )
    
    FORMAT_CHOICES = (
      (u'fasta', u'fasta'),
      (u'genbank', u'GenBank'),
    )
    
    task = models.OneToOneField(Task, primary_key=True)
    params = models.TextField(blank=True, null=True)
    out_format = models.CharField(max_length=10, choices=FORMAT_CHOICES)
    job = models.CharField(max_length=4, choices=JOB_CHOICES)      

#------------------------------------------------------------------------------

class Subtask(models.Model):
    FORMAT_CHOICES = (
        (u'fasta', u'fasta'),
        (u'genbank', u'GenBank'),
    )
    task = models.ForeignKey(Task)
    seq_format = models.CharField(max_length=10, choices=FORMAT_CHOICES)
    record = models.TextField()
    paused = models.BooleanField(default=True, editable=False)
    def getSeqRecord( self ):
        return SeqIO.read(StringIO(str(self.record)), str(self.seq_format))
    def getSeq( self ):
        return self.seq_record.seq
    def getSeqId( self ):
        return self.seq_record.id
    def getSeqName( self ):
        return self.seq_record.name
    def getSeqDesc( self ):
        return self.seq_record.description
    def getSeqLA( self ):
        return self.seq_record.letter_annotations
    def getSeqAnnots( self ):
        return self.seq_record.annotations
    def getSeqFeat( self ):
        return self.seq_record.features
    def getSeqDBxRefs( self ):
        return self.seq_record.dbxrefs
    def getPickle( self ):
        src = StringIO()
        p = pickle.Pickler(src)
        p.dump(self.seq_record)
        return src.getvalue()                                              
    def short_seq( self ):
        return (self.seq[:20] + "...")
    def finished( self ):
        try:
            self.rawresult
            return True
        except RawResult.DoesNotExist:
            return False
            
    finished = property(finished)
    seq_record = property(getSeqRecord)
    seq = property(getSeq)
    seq_id = property(getSeqId)
    seq_name = property(getSeqName)
    seq_description = property(getSeqDesc)
    seq_letter_annotations = property(getSeqLA)
    seq_annotations = property(getSeqAnnots)
    seq_features = property(getSeqFeat)
    seq_dbxrefs = property(getSeqDBxRefs)
    seq_pickle = property(getPickle)           

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

class Monitor(models.Model):

    JOB_CHOICES = (
      (u'N', u'No job'),
      (u'Cmpl', u'Complement'),
      (u'RvCm', u'Reverse Complement'),
      (u'Trb', u'Transcribe'),
      (u'BTrb', u'Back transcribe'),
      (u'Trlt', u'Translate'),
      (u'Blst', u'BLAST'),
    )
    
    who = models.CharField(max_length=30)
    when = models.DateField(auto_now_add=True, blank=True, null=True)
    what = models.TextField(max_length=4, choices=JOB_CHOICES, blank=True, null=True)
    status = models.CharField(max_length=30)

#------------------------------------------------------------------------------
