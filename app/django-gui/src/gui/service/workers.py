from Bio.SeqRecord import SeqRecord

#-------------------------------------------------------------------------------

class Worker:
    def __init__(self, job, outFormat = 'fasta', params=None):
        self.params = params
        self.outFormat = outFormat
        self.job = JobFactory().getJob(job, params)
    def execute(self, seqRecord):
        return self.job.execute(seqRecord, self.outFormat)
        
#-------------------------------------------------------------------------------

class JobFactory:

    def getJob(self, job, params):
        if job == u'Cmpl':
            return ComplementJob(params)
        elif job == u'RvCm':
            return ReverseComplementJob(params)
        elif job == u'Trb':
            return TranscribeJob(params)
        elif job == u'BTrb':
            return BackTranscribeJob(params)
        elif job == u'Trlt':
            return TranslateJob(params)
        elif job == u'Blst':
            return BLASTJob(params)    
            
#-------------------------------------------------------------------------------

class Job:
    def __init__(self, params):
        self.params = params
    def execute(self, seqRecord, outFormat):
      raise NotImplementedError

#-------------------------------------------------------------------------------

class ComplementJob(Job):
    def execute(self, seqRecord, outFormat):
        return SeqRecord(seqRecord.seq.complement()).format(outFormat)
    
#-------------------------------------------------------------------------------

class ReverseComplementJob(Job):
    def execute(self, seqRecord, outFormat):    
        return SeqRecord(seqRecord.seq.reverse_complement()).format(outFormat)
    
#-------------------------------------------------------------------------------

class TranscribeJob(Job):
    def execute(self, seqRecord, outFormat):
        return SeqRecord(seqRecord.seq.transcribe()).format(outFormat)
    
#-------------------------------------------------------------------------------

class BackTranscribeJob(Job):
    def execute(self, seqRecord, outFormat):
        return SeqRecord(seqRecord.seq.back_transcribe()).format(outFormat)
    
#-------------------------------------------------------------------------------

class TranslateJob(Job):
    def execute(self, seqRecord, outFormat):
        return SeqRecord(seqRecord.seq.translate()).format(outFormat)
    
#-------------------------------------------------------------------------------

class BLASTJob(Job):
    def execute(self, seqRecord, outFormat):
        from Bio.Blast import NCBIWWW
        from Bio.Blast import NCBIXML
        ret = []
        rekord = seqRecord.format("fasta")
        for db in self.params["db"]:
          ret.append(NCBIWWW.qblast(self.params['blast'], db, rekord, expect=float(self.params['cutoff']), filter=self.params['filter'], hitlist_size=int(self.params['nhits']), matrix_name=self.params['matrix'], alignments=int(self.params['nalign']), descriptions=int(self.params['ndesc']), megablast=self.params['megablast']).read())
        return ret
    
#-------------------------------------------------------------------------------
                            
