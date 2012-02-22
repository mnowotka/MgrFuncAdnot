
class Parser:
    def __init__(self):
        self.__sequences = []      
    def parse(self, data):
        return self.__sequences
      
class FASTAParser(Parser):

    trailer = '>'
    
    def __parse(self, chunk):    
        if not chunk:
            return
        self.__sequences.append("".join(chunk))

    def parse(self, data):
        chunk = []
        for idx, line in enumerate(data):
          if not line.strip():
              continue
          if not line.startswith(self.trailer):
              chunk.append(line)
          else:
              try:
                self.__parse(chunk)
              except Exception as exc:
                self.__logger.error(str(exc))  
              chunk = []
        self.__parse(chunk)
      
class GenBankParser(Parser):
    pass
    
class SequenceParcingFactory:
    def getParser(self, typ):
        #raise Exception, typ
        if typ == 'fasta':
            #raise Exception, "a"
            return FASTAParser()
        elif typ == 'genbank':
            #raise Exception, "b"
            return GenBankParser()
        else:
            #raise Exception, "c"
            return Parser()                   
