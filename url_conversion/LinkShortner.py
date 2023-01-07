import json
import requests
import uuid
from properties import ApplicationProperties
from urllib import parse
from log.Logging import log


class LinkShortner:
    """
    Functionality: \n
    1. Shorten the specified long url
    2. Change alias of given shortened url
    3. Set Custom alias of url
    """

    def __init__(self):
        self.secret = ApplicationProperties.CUTTLY_SECRET()
        self.SSH_alias = ApplicationProperties.SSH_CUSTOM_ALIAS()
        # self.urlToShorten = url

    def url_shortner(self, url):
        output = self.change_alias()
        if output[0] == 3:
            log.info('The Default short url is new and not register for any shortner. \n Registering url: {} with for shortening the url.'.format(url))
        elif output[0] == 2:
            log.error('Can\'t change the alias, '+ output[1])
        return self.set_alias(url)

    # Invoke cuttly api to get the output
    def cuttly_api(self, parameters: dict) -> (dict, int):
        BASE_API_URL = ApplicationProperties.BASE_API_URL()
        parameters['key'] = self.secret
        print(parameters)
        response = requests.get(url=BASE_API_URL, params=parameters)
        return json.loads(response.text), response.status_code

    # This will free the alias from the
    def change_alias(self):
        random_alias = 'test' + str(uuid.uuid4())[:5]
        short_url = parse.quote(ApplicationProperties.BASE_DOMAIN() + self.SSH_alias)
        parameters = {
            'edit': short_url,
            'name': random_alias
        }
        output = {}
        log.info('Changing alias with parameter: '+ str(parameters))
        output, status = self.cuttly_api(parameters)
        print('Changing alias API output: {} Status: {}'.format(output, status))
        if output != '' and "status" in output:
            if output['status'] == 3:
                return (3, "message: The default doesn't linked to the system.")
            elif output['status'] == 2:
                return (2, 'message: Cuttly api return error. Error: Couldn\'t save in db')
            elif output['status'] == 1:
                return (0, 'message: Long url(ngrok url) success changed to default shortened url')
        pass

    # Set the the SSH_alias to the new generated Ngrok-url (e.g tcp://0.tcp.ngrok.io:somePort )
    '''
    pamaters = {short: , name: }
    Short: Which URL to shortern
    name: Custom alias if required
    '''

    def set_alias(self, url):
        PORT_FORWARDED_URL = url
        parameters = {
            'short': PORT_FORWARDED_URL,
            'name': ApplicationProperties.SSH_CUSTOM_ALIAS()
        }
        output = {}
        log.info('Setting the new long url to short url: ' + PORT_FORWARDED_URL + ApplicationProperties.SSH_CUSTOM_ALIAS())
        output, status = self.cuttly_api(parameters)
        log.info(str(self.set_alias.__name__) + ' Output: '+ str(output) + ' Status: '+ str(status))
        if output != '' and 'url' in output:
            if output['url']['status'] == 2:
                return (0, 'error: Probably error in Long url(Ngrok)')
            elif output['url']['status'] == 3:
                return (3,'error: Alias is already taken. Possibly bug in code')
            elif output['url']['status'] == 4:
                return (4, 'errorCuttly Access key in invalid.')
            elif output['url']['status'] == 6:
                return (6, 'error Long url belongs to blocked domain.')
            elif output['url']['status'] == 7:
                return (0, 'message Link is shortened.')
        pass

# #TEST
# S = LinkShortner()
# S.change_alias()
# S.set_alias('http://xyz.com')
