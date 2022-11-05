import requests
from Logging import log


class LinkLonger:

    @staticmethod
    def url_short_reverse(url):
        long_url = ''
        try:
            log.info('Iterating redirects to get final url.')
            while True:
                long_url = requests.head(url).headers['location']
                url = long_url
                log.debug(long_url)
        except:
            print(long_url)
        return long_url

# #Test
# t = LinkLonger()
# print(t.url_short_reverse('http://cutt.ly/zNYsUQm'))
