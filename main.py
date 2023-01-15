from properties import ApplicationProperties, setup
from ngrok_session.AllTunnels import AllTunnels
from url_conversion.LinkShortner import LinkShortner
from process.Process import Process
from log.Logging import log
from ngrok_session.Session import Session
import RecoveryCheck
import argparse

DEFAULT_SHORT_URL = ApplicationProperties.BASE_DOMAIN() + ApplicationProperties.SSH_CUSTOM_ALIAS()


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


def arguments():
    options = argparse.ArgumentParser()
    options.add_argument('-k', '--ngrok_api_secret', help='Add Ngrok api secret')
    options.add_argument('-a', '--ngrok_auth_token', help='Add Ngrok auth token to the ~/.ngrok/ngrok.yml path')
    options.add_argument('-s', '--cuttly_secret', help='Add cuttly api secret')
    options.add_argument('--alias', help='Start ngrok with custom alias. Note: this will overide config.ini alias')
    options.add_argument('-p', '--port', help='Forward the specified port')
    options.add_argument('-r', '--protocol', help='Forward the port with specified protocol')

    args = options.parse_args()
    if not any(vars(args).values()):
        return
    if args.ngrok_api_secret:
        secret = args.ngrok_api_secret
        setup.set_ngrok_secret(secret=secret)
    if args.ngrok_auth_token:
        auth_token = args.ngrok_auth_token
        setup.set_ngrok_auth_token(auth_token=auth_token)
    if args.cuttly_secret:
        cuttly_secret = args.cuttly_secret
        setup.set_cutt_ly_secret(secret=cuttly_secret)
    if args.alias:
        setup.set_alias(alias=args.alias)
    if args.port:
        if args.protocol:
            setup.set_port_protocol(args.port, args.protocol)
        else:
            log.error('Please pass both protocol and port.')
            raise Exception('Protocol and port need to be passed together.')


if __name__ == '__main__':
    log.info('\n\n\n##################### Initialization Process #####################')
    arguments()
    process = Process()
    link_shortner = LinkShortner()
    all_tunnels = AllTunnels()
    session = Session()
    while True:
        try:
            start_tunneling()
            RecoveryCheck.check()
        except KeyboardInterrupt:
            log.info('Keyboard interruption. Gracefully shutting down the process')
            process.kill()
            exit(0)
        except Exception as error:
            log.exception('An exception occurred: {}'.format(error))
            # log.info('Gracefully cleaning up. Checking if process exist and killing it')
            log.info('Trying to recover. Rerunning the program again')
            continue
        log.info('Error occurred, trying to recover.')
