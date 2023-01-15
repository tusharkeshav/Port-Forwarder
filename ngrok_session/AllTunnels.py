from properties import ApplicationProperties
import requests
from log.Logging import log
import json
from process.Process import Process
import time


class AllTunnels:
    def __init__(self):
        self.secret_key = ApplicationProperties.NGROK_SECRET()

    def url_patch(self, url):
        # Patch: cuttly don't support Long url with subdomain starting with numeric(e.g 0.tcp.ngrok.io). Adding null keyword to fix it
        log.info('Patching the long URL to add null to long url: {}'.format(url))
        return 'null' + url.split('//')[-1]

    def tunnels(self):
        url = ApplicationProperties.BASE_TUNNEL_URL()  # ngrok tunnel endpoint
        headers = {'ngrok-version': '2',
                   'Authorization': 'Bearer {}'.format(self.secret_key)}

        log.info('Checking process before Ngrok Api call {} '.format(Process().check()))
        log.info('Invoking ngrok API to get tunnel sessions: {} and headers: {}'.format(url, headers))

        # Patch: Encountered a bug where NGROK API wasn't returning correct response even after successfull correct ngrok process execution.
        # Patch: So delay is added so that there ngrok session would update in ngrok servers and API return correct response.
        log.info('Sleeping for 5 seconds before making API call')
        time.sleep(5)
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            response = response.text
        elif 500 > response.status_code >= 400:
            log.error("Authorization issue. Possibly due to api access token. status code received: {}".format(
                response.status_code))
            return (-1, "Authorization issue, status code received: {}".format(response.status_code))
        elif 600 > response.status_code >= 500:
            log.error("Server Issue, status code received: {}".format(response.status_code))
            return (-1, "Server Issue, status code received: {}".format(response.status_code))

        # Check for output
        response = json.loads(response)
        log.info('Ngrok Api response: {}'.format(response))

        if response != '' and 'tunnels' in response:
            if len(response['tunnels']) > 0 and 'public_url' in response['tunnels'][0]:
                ngrok_public_url = str(response['tunnels'][0]['public_url'])
                # TODO: Look for other option
                # Patch: cuttly don't support Long url with subdomain starting with numeric(e.g 0.tcp.ngrok.io). Adding null keyword to fix it
                url2shorten = ngrok_public_url
                if ApplicationProperties.PORT()[0].lower() == 'tcp':
                    url2shorten = self.url_patch(ngrok_public_url)
                log.info("Url to be shortened: " + url2shorten)
                return (0, url2shorten)
            else:
                log.info("Api invocation was successful, but response didn't return any tunnel session")
                return (-2, None)

# Test
# test = AllTunnels()
# print(test.tunnels())
