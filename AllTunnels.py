import ApplicationProperties
import requests
from Logging import log
import json


class AllTunnels:
    def __init__(self):
        self.secret_key = ApplicationProperties.ngrok_secret

    def url_patch(self, url):
        # Patch: cuttly don't support Long url with subdomain starting with numeric(e.g 0.tcp.ngrok.io). Adding null keyword to fix it
        return 'null' + url.split('//')[-1]

    def tunnels(self):
        url = ApplicationProperties.BASE_TUNNEL_URL  # ngrok tunnel endpoint
        headers = {'ngrok-version': '2',
                   'Authorization': 'Bearer {}'.format(self.secret_key)}
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
        if response != '' and 'tunnels' in response:
            if len(response['tunnels']) > 0 and 'public_url' in response['tunnels'][0]:
                ngrok_public_url = str(response['tunnels'][0]['public_url'])[1]
                # TODO: Look for other option
                # Patch: cuttly don't support Long url with subdomain starting with numeric(e.g 0.tcp.ngrok.io). Adding null keyword to fix it
                url2shorten = self.url_patch(ngrok_public_url)
                # url2shorten = 'null' + ngrok_public_url.split('//')[1]
                print(url2shorten)
                log.info("Url to be shortened: " + url2shorten)
                return (0, url2shorten)
            else:
                log.info("Api invocation was successful, but response didn't return any tunnel session")
                return (-2, None)

# Test
# test = AllTunnels()
# print(test.tunnels())
