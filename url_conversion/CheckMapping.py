from url_conversion.LinkLonger import LinkLonger
from log.Logging import log
from properties.ApplicationProperties import PORT

class CheckMapping:

    def check_mapping(self, short_url, long_url):
        short_url_2_long_url = LinkLonger.url_short_reverse(short_url)
        long_url_clean = ''
        if str(PORT()[0]).lower() == 'tcp':
            short_url_2_long_url = short_url_2_long_url.split('null')[-1]
            long_url_clean = long_url.split('/')[-1].split('null')[-1]
        elif str(PORT()[0]).lower() == 'http':
            short_url_2_long_url = short_url_2_long_url.split('https')[-1].split('/')[-1]
            long_url_clean = long_url.split('/')[-1].split('http')[-1]
        else:
            raise Exception("Invalid supported Protocol: {}".format(PORT()[0]))
        log.info('Checking mapping of short url: {} and Long url: {}'.format(short_url_2_long_url, long_url_clean))
        if short_url_2_long_url == long_url_clean:  # mapping is correct
            return 0
        else:
            return -1
