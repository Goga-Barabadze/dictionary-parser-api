import logging

logging.basicConfig(format='%(asctime)s %(levelname)s %(thread)d %(lineno)d \t %(message)s')
log = logging.getLogger()
log.setLevel(logging.NOTSET)
