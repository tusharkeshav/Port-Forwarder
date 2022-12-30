from log.Logging import log
from process.Process import Process
from ngrok_session.Session import Session
import time


def check():
    log.info('Recovery: Monitoring the process.')
    session = Session()
    while True:
        time.sleep(500)
        status, out = Process().check()
        if status != 0:
            # issue with process, process doesn't exist, call recover process again
            log.error('Recovery: Process doesn\'t exist, Trying to recover')
            session.spawn_process()
            pass

        # check for Valid session
        log.info('Recovery: Checking for Valid session')
        session.valid_session_check()
