from sys import exit

from kalib.loggers import Logging

Logging.get(__name__).exception('halt', trace=True, shift=-2, stack=2)
exit(127)
