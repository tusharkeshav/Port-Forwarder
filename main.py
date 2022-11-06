from AllTunnels import AllTunnels
from LinkShortner import LinkShortner
from Process import Process
from Logging import log
import ApplicationProperties
from LinkLonger import LinkLonger

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


def check_mapping(short_url, long_url):
    short_url_2_long_url = LinkLonger.url_short_reverse(short_url)
    short_url_2_long_url = short_url_2_long_url.split('null')[-1]
    long_url_clean = long_url.split('/')[-1].split('null')[-1]
    log.info('Checking mapping of short url: {} and Long url: {}'.format(short_url_2_long_url, long_url_clean))
    if short_url_2_long_url == long_url_clean:   # mapping is correct
        return 0
    else:
        return -1


def start_tunneling():
    output = process.check()
    if output[0] == -1:
        log.info('No Process found, starting new process')
        spawn_process()

    elif output[0] == 0:
        # There is a case, where ssh session might be disconnected
        tunnel_output = all_tunnels.tunnels()
        if tunnel_output[0] == -2:  # successful tunnel session for device doesn't exist. Possibly the process is orphaned
            log.error("Tunnel session on this device doesn't exist. Possibly the process is orphaned.")
            log.info("Killing the process and spawning the new process.")
            process.kill()
            log.info("Spawning new process")
            spawn_process()
        elif tunnel_output[0] == 0:
            status = check_mapping(short_url=DEFAULT_SHORT_URL, long_url=tunnel_output[1])
            if status == 0:
                log.info('{} is already mapped to shorted url : {}'.format(DEFAULT_SHORT_URL, tunnel_output[1]))
            else:   # correct mapping is not there. So change alias -> set alias to correct long url
                url2shorten = tunnel_output[1]
                link_shortner_output = link_shortner.url_shortner(url2shorten)
                if link_shortner_output[0] == 0:
                    log.info('{} is updated for the short url : {} '.format(url2shorten, DEFAULT_SHORT_URL))
                else:
                    log.error('Error occured while updating the mapping: '+ url2shorten)


if __name__ == '__main__':
    process = Process()
    link_shortner = LinkShortner()
    all_tunnels = AllTunnels()
    try:
        start_tunneling()
    except Exception as error:
        log.exception('An exception occured: {}'.format(error))
        log.info('Gracefull cleaning up. Checking if process exist and killing it')
        process.kill()
