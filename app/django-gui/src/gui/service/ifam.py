import os, sys, traceback
import time

from django.conf import settings
from gui.models import Task, Subtask, RawResult
from gui.service.workers import Worker

from dashboard.common import log as logging
from dashboard.common.InternalException import InternalException
from dashboard.common.NotAvailableException import NotAvailableException
from dashboard.service.config.Service import Service

class MyService1(Service):
    """
    Example class definition of a Service object managed by the dashboard service configurator.
    It loads some parameters which should be available via the service configuration file.
    """
    
    """
    Class static logger object.
    """
    _logger = logging.getLogger("dashboard.service.config.ServiceGroupWrapper")

    """
    Default time interval between two runs (in seconds).
    """
    runInterval = 30
    
    def __init__(self, name, configFile):
        """
        Initializer for the object.
        """
        Service.__init__(self, name, configFile)
        
        # Load info from the configuration parameters
        self._param1 = self.param("param1")
        self._param2 = self.param("param2")
        
    def run(self):
        """
        @see L{dashboard.service.config.Service.run()}
        """
        while self.status() == self.ACTIVE:

            # Log the iteration number
            self._logger.info("Loop in the %s service iteration" % (self._name))
            try:
                for subtask in Subtask.objects.filter(rawresult=None).filter(paused=False).exclude(task__tasksettings=None):
                    job = subtask.task.tasksettings.job
                    params = subtask.task.tasksettings.params
                    outFormat = subtask.task.tasksettings.out_format
                    self._logger.info("Performing" + str(job) + " for subtask " + str(subtask.seq_id))
                    worker = Worker(job, outFormat, params)
                    rawResult = RawResult()
                    rawResult.result = worker.execute(subtask.getSeqRecord())
                    rawResult.subtask = subtask
                    rawResult.save()
                    
            except Exception, e:
                self._logger.error(str(e))
        	
            # And put it also in the message area, so that it can be picked by the
            # ServiceMonitor and sent to the configured endpoints
            # The current service state will be also part of the message
            #self.putMessage("Loop %d in the %s service iteration" % (i, self._name))
        	
            # Sleep for the run interval defined
            # This is loaded from the configuration file
            time.sleep(self.runInterval)
