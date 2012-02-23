import logging

#-------------------------------------------------------------------------------

class Parser:
    def __init__(self):
        self.sequences = []
        self.logger = logging.getLogger("dajaxice")      
    def parse(self, data):
        return self.sequences

#-------------------------------------------------------------------------------
      
class FASTAParser(Parser):

    trailer = '>'
    
    def __parse(self, chunk):    
        if not chunk:
            return    
        self.sequences.append("".join(chunk[1:]))

    def parse(self, data):
        chunk = []
        for idx, line in enumerate(data.replace('\r\n','\n').split('\n')):
          if not line.strip():
              continue
          if not line.startswith(self.trailer): 
              chunk.append(line)
          else:
              try:
                self.__parse(chunk)
              except Exception as exc:
                self.logger.error(str(exc))  
              chunk = []
        self.__parse(chunk)
        return self.sequences

#-------------------------------------------------------------------------------
      
class GenBankParser(Parser):
    pass

#-------------------------------------------------------------------------------
    
class SequenceParcingFactory:
    def getParser(self, typ):
        if typ == 'fasta':
            return FASTAParser()
        elif typ == 'genbank':
            return GenBankParser()
        else:
            return Parser()

#-------------------------------------------------------------------------------                               
