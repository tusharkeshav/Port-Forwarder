import logging

FORMAT = "[%(asctime)s %(filename)s->%(funcName)s():%(lineno)s]%(levelname)s: %(message)s"
logging.basicConfig(filename='log/Application.log', format=FORMAT,  encoding='utf-8')

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# #Setup logger
# logger = logging.getLogger(__name__)
# FORMAT = "[%(asctime)s %(filename)s->%(funcName)s():%(lineno)s]%(levelname)s: %(message)s"
# logging.basicConfig(format=FORMAT, level=logging.INFO)
# #Log to file
# logging_filename = 'main.log'
# handler = RotatingFileHandler(logging_filename, maxBytes=1000000, backupCount=10) #10 files of 1MB each
# handler.setFormatter(logging.Formatter(FORMAT))
# logger.addHandler(handler)
