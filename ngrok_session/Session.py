import time
from ngrok_session.AllTunnels import AllTunnels
from url_conversion.LinkShortner import LinkShortner
from process.Process import Process
from log.Logging import log
from properties import ApplicationProperties
from url_conversion.CheckMapping import CheckMapping


class Session:
    """
    Functionality: \n
    1.To create new Session \n
    2.To Validate if valid session exist between the short link and the long link
    """

    def __init__(self):
        self.process = Process()
        self.link_shortner = LinkShortner()
        self.all_tunnels = AllTunnels()
        self.DEFAULT_SHORT_URL = ApplicationProperties.BASE_DOMAIN() + ApplicationProperties.SSH_CUSTOM_ALIAS()

    def valid_session_check(self):

        tunnel_output = self.all_tunnels.tunnels()
        if tunnel_output[0] == -2:
            # successful tunnel session for device doesn't exist. Possibly the process is orphaned

            log.error("Tunnel session on this device doesn't exist. Possibly the process is orphaned.")
            log.info("Killing the process and spawning the new process.")
            self.process.kill()
            log.info("Spawning new process")
            self.spawn_process()
        elif tunnel_output[0] == 0:
            status = CheckMapping().check_mapping(short_url=self.DEFAULT_SHORT_URL, long_url=tunnel_output[1])
            if status == 0:
                log.info('{} is already mapped to shorted url : {}'.format(self.DEFAULT_SHORT_URL, tunnel_output[1]))
            else:  # correct mapping is not there. So change alias -> set alias to correct long url
                url2shorten = tunnel_output[1]
                link_shortner_output = self.link_shortner.url_shortner(url2shorten)
                if link_shortner_output[0] == 0:
                    log.info('{} is updated for the short url : {} '.format(url2shorten, self.DEFAULT_SHORT_URL))
                else:
                    log.error('Error occurred while updating the mapping: ' + url2shorten)

    def spawn_process(self):
        self.process.start()
        log.debug('Sleeping for 2 seconds before checking if process launch state.')
        time.sleep(2)
        # TODO: checking for retry mechanism if process didn't started successfully.
        if self.process.check()[0] == 0:
            log.info('Process started successfully.')
            tunnel_output = self.all_tunnels.tunnels()
            if tunnel_output[0] == 0:
                url2shorten = tunnel_output[1]
                link_shortner_output = self.link_shortner.url_shortner(url2shorten)
                if link_shortner_output[0] == 0:
                    log.info('{} is mapped to shorted url : {} '.format(url2shorten, self.DEFAULT_SHORT_URL))
                return 0
            else:
                log.error("Error in long URL: " + tunnel_output[1])
                return -1
        else:
            log.error('Process didn\'t started successfully.')
