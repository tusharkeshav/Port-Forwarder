import requests
from log.Logging import log


class LinkLonger:
    """
    Functionality: \n
    1. Able to convert short url to Long url or say, it basically reverses the url shortening process.
    """

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
