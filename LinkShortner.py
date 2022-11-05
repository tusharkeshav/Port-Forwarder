import json
import requests
import uuid
import ApplicationProperties
from urllib import parse


class LinkShortner:

    def __init__(self):
        self.secret = ApplicationProperties.cutt_ly_secret
        self.SSH_alias = ApplicationProperties.SSH_custom_alias
        # self.urlToShorten = url

    def url_shortner(self, url):
        return self.set_alias(url)

    # Invoke cuttly api to get the output
    def cuttly_api(self, parameters: dict) -> (dict, int):
        BASE_API_URL = ApplicationProperties.BASE_API_URL
        parameters['key'] = self.secret
        print(parameters)
        response = requests.get(url=BASE_API_URL, params=parameters)
        return json.loads(response.text), response.status_code

    # This will free the alias from the
    def change_alias(self):
        random_alias = 'test' + str(uuid.uuid4())[:5]
        short_url = parse.quote(ApplicationProperties.BASE_DOMAIN + self.SSH_alias)
        parameters = {
            'edit': short_url,
            'name': random_alias
        }
        output = {}
        print(self.change_alias.__name__, parameters)
        output, status = self.cuttly_api(parameters)
        print(self.change_alias.__name__, output, status)
        if output != '' and "status" in output:
            if output['status'] == 3:
                return {"message": "The default doesn't linked to the system."}
            elif output['status'] == 2:
                return {'message': 'Cuttly api return error. Error: Couldn\'t save in db'}
            elif output['status'] == 1:
                return {'message': 'Long url(ngrok url) success changed to default shortened url'}
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
            'name': ApplicationProperties.SSH_custom_alias
        }
        output = {}
        print(self.set_alias.__name__, parameters)
        output, status = self.cuttly_api(parameters)
        print(self.set_alias.__name__, output, status)
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
