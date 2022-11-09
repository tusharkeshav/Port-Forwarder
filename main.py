import ApplicationProperties
from AllTunnels import AllTunnels
from LinkShortner import LinkShortner
from Process import Process
from Logging import log
from Session import Session
import RecoveryCheck

DEFAULT_SHORT_URL = ApplicationProperties.BASE_DOMAIN + ApplicationProperties.SSH_custom_alias


def spawn_process():
    process.start()
    # TODO: checking for retry mechanism if process didn't started successfully.
    if process.check()[0] == 0:
        log.info('Process started successfully.')
        tunnel_output = all_tunnels.tunnels()
        if tunnel_output[0] == 0:
            url2shorten = tunnel_output[1]
            link_shortner_output = link_shortner.url_shortner(url2shorten)
            if link_shortner_output[0] == 0:
                log.info('{} is mapped to shorted url : {} '.format(url2shorten, DEFAULT_SHORT_URL))
            return 0
        else:
            log.error("Error in long URL: " + tunnel_output[1])
            return -1


def start_tunneling():
    output = process.check()
    if output[0] == -1:
        log.info('No Process found, starting new process')
        session.spawn_process()

    elif output[0] == 0:
        # There is a case, where ssh session might be disconnected
        session.valid_session_check()


if __name__ == '__main__':
    log.info('\n\n\n##################### Initialization Process #####################')
    process = Process()
    link_shortner = LinkShortner()
    all_tunnels = AllTunnels()
    session = Session()
    try:
        # start_tunneling()
        RecoveryCheck.check()
    except Exception as error:
        log.exception('An exception occurred: {}'.format(error))
        log.info('Gracefully cleaning up. Checking if process exist and killing it')
        process.kill()
