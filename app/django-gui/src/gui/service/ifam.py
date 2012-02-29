import os, sys
import time

from django.conf import settings

from dashboard.common import log as logging
from dashboard.common.InternalException import InternalException
from dashboard.common.NotAvailableException import NotAvailableException
from dashboard.common.url.URLClient import URLClient
from dashboard.service.config.Service import Service

class MyService1(Service):
    """
    Example class definition of a Service object managed by the dashboard service configurator.
    It loads some parameters which should be available via the service configuration file.
    """
    
    """
    Class static logger object.
    """
    _logger = logging.getLogger("dashboard.service.config.test.MyService1")

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
            self._logger.info("Loop %d in the %s service iteration" % (i, self._name))
        	
            # And put it also in the message area, so that it can be picked by the
            # ServiceMonitor and sent to the configured endpoints
            # The current service state will be also part of the message
            #self.putMessage("Loop %d in the %s service iteration" % (i, self._name))
        	
            # Sleep for the run interval defined
            # This is loaded from the configuration file
            time.sleep(self.runInterval)
