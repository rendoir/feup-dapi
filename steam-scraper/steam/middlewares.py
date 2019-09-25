import logging
import os
import re
from w3lib.url import url_query_cleaner

from scrapy import Request
from scrapy.downloadermiddlewares.redirect import RedirectMiddleware
from scrapy.dupefilters import RFPDupeFilter
from scrapy.extensions.httpcache import FilesystemCacheStorage
from scrapy.utils.request import request_fingerprint

logger = logging.getLogger(__name__)


def strip_snr(request):
    """Remove snr query query from request.url and return the modified request."""
    url = url_query_cleaner(request.url, ['snr'], remove=True)
    return request.replace(url=url)


class SteamCacheStorage(FilesystemCacheStorage):
    def _get_request_path(self, spider, request):
        request = strip_snr(request)
        key = request_fingerprint(request)
        return os.path.join(self.cachedir, spider.name, key[0:2], key)


class SteamDupeFilter(RFPDupeFilter):
    def request_fingerprint(self, request):
        request = strip_snr(request)
        return super().request_fingerprint(request)


class CircumventAgeCheckMiddleware(RedirectMiddleware):
    def _redirect(self, redirected, request, spider, reason):
        # Only overrule the default redirect behavior
        # in the case of mature content checkpoints.
        if not '/agecheck/' in redirected.url:
            return super()._redirect(redirected, request, spider, reason)

        logger.debug(f'Button-type age check triggered for {request.url}.')

        return Request(url=request.url,
                       cookies=[{'name': 'wants_mature_content', 'value': '1', 'path': '/', 'expires': 'Thu, 24 Sep 2020 7:16:26 GMT', 'created': 'Wed, 25 Sep 2019 18:33:38 GMT', 'domain': 'store.steampowered.com'},
                                   {'name': 'lastagecheckage', 'value': '1-0-1996', 'path': '/', 'expires': 'Thu, 24 Sep 2020 7:16:26 GMT', 'created': 'Wed, 25 Sep 2019 18:33:38 GMT', 'domain': 'store.steampowered.com'},
                                   {'name': 'birthtime', 'value': '849398401', 'path': '/', 'expires': 'Thu, 24 Sep 2020 7:16:26 GMT', 'created': 'Wed, 25 Sep 2019 18:33:38 GMT', 'domain': 'store.steampowered.com'}],
                       meta={'dont_cache': True},
                       callback=spider.parse_product)
