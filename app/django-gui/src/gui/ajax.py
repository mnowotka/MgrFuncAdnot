from django.utils import simplejson

from dajax.core import Dajax
from dajaxice.core import dajaxice_functions

#-------------------------------------------------------------------------------

def dajaxice_example(request):
    return simplejson.dumps({'message':'Hello from Python!'})

#-------------------------------------------------------------------------------

dajaxice_functions.register(dajaxice_example)

