from LinkLonger import LinkLonger
from Logging import log


class CheckMapping:

    def check_mapping(self, short_url, long_url):
        short_url_2_long_url = LinkLonger.url_short_reverse(short_url)
        short_url_2_long_url = short_url_2_long_url.split('null')[-1]
        long_url_clean = long_url.split('/')[-1].split('null')[-1]
        log.info('Checking mapping of short url: {} and Long url: {}'.format(short_url_2_long_url, long_url_clean))
        if short_url_2_long_url == long_url_clean:  # mapping is correct
            return 0
        else:
            return -1
