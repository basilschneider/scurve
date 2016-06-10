#!/usr/bin/env/python2

""" Logger to be imported by other modules. """

import logging

# Set up logger
# DEBUG (10), INFO (20), WARNING(30), ERROR(40), CRITICAL(50)
logging.basicConfig(format='%(levelname)-8s - %(message)s',
                    level=logging.INFO)
LGR = logging.getLogger(__name__)
