import logging
import re
from w3lib.url import canonicalize_url, url_query_cleaner

from scrapy.http import FormRequest, Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import ProductItem, ProductItemLoader

logger = logging.getLogger(__name__)


def load_product(response):
    """Load a ProductItem from the product page response."""
    loader = ProductItemLoader(item=ProductItem(), response=response)

    url = url_query_cleaner(response.url, ['snr'], remove=True)
    url = canonicalize_url(url)
    # loader.add_value('url', url)

    found_id = re.findall('/app/(.*?)/', response.url)
    if found_id:
        id = found_id[0]
        # reviews_url = f'https://steamcommunity.com/app/{id}/reviews/?browsefilter=mostrecent&p=1'
        # loader.add_value('reviews_url', reviews_url)
        loader.add_value('id', id)

    # Publication details.
    details = response.css('.game_details .details_block').extract_first()
    try:
        details = re.sub('</div>', '</div><br>', details) # Add <br> to the end of each dev_row div
        details = details.split('<br>')

        for line in details:
            line = re.sub('<[^<]+?>', '', line)  # Remove tags.
            line = re.sub('[\r\t\n]', '', line).strip()
            for prop, name in [
                ('Title:', 'title'),
                ('Genre:', 'genres'),
                ('Developer:', 'developer'),
                ('Publisher:', 'publisher'),
                ('Franchise:', 'franchise'),
                ('Release Date:', 'release_date')
            ]:
                if prop in line:
                    item = line.replace(prop, '').strip()
                    loader.add_value(name, item)
    except:  # noqa E722
        pass

    loader.add_css('app_name', '.apphub_AppName ::text')
    loader.add_css('specs', '.game_area_details_specs:not(.learning_about) a ::text')
    loader.add_css('tags', 'a.app_tag::text')
    loader.add_css('description', ".game_description_snippet::text")

    price = response.css('.game_purchase_price ::text').extract_first()
    if not price:
        price = response.css('.discount_original_price ::text').extract_first()
        loader.add_css('discount_price', '.discount_final_price ::text')
    loader.add_value('price', price)

    sentiment = response.css('.summary .game_review_summary').xpath(
        '../*[@itemprop="description"]/text()').extract()
    if sentiment and sentiment[0] and (not sentiment[0][0].isdigit()) and (not (sentiment == 'No user reviews')):
        loader.add_value('sentiment', sentiment)
    loader.add_css('n_reviews', '.summary .responsive_hidden', re='\(([\d,]+)\)')

    # loader.add_xpath(
    #     'metascore',
    #     '//div[@id="game_area_metascore"]/div[contains(@class, "score")]/text()')

    early_access = response.css('.early_access_header')
    if early_access:
        loader.add_value('early_access', True)
    else:
        loader.add_value('early_access', False)

    # About
    about = response.css('#game_area_description').get()
    if about:
        about = re.sub('<h2>About This Game</h2>', '', about) # Remove about header
        about = re.sub('<[^<]+?>|\t|\r|\xa0|\x0d|\x09', '', about) # Remove tags
        loader.add_value('about', about)

    return loader.load_item()


class ProductSpider(CrawlSpider):
    name = 'products'
    start_urls = ['https://store.steampowered.com/search/?category1=998'] # Ordered by relevance, games only category

    allowed_domains = ['steampowered.com']

    rules = [
        Rule(LinkExtractor(
             allow='/app/(.+)/',
             restrict_css='#search_result_container'),
             callback='parse_product'),
        Rule(LinkExtractor(
             allow='page=(\d+)',
             restrict_css='.search_pagination_right'))
    ]

    def __init__(self, steam_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.steam_id = steam_id

    def start_requests(self):
        if self.steam_id:
            yield Request(f'https://store.steampowered.com/app/{self.steam_id}/',
                          callback=self.parse_product,
                          cookies=[{'name': 'wants_mature_content', 'value': '1', 'path': '/', 'expires': 'Thu, 24 Sep 2020 7:16:26 GMT', 'created': 'Wed, 25 Sep 2019 18:33:38 GMT', 'domain': 'store.steampowered.com'},
                                   {'name': 'lastagecheckage', 'value': '1-0-1996', 'path': '/', 'expires': 'Thu, 24 Sep 2020 7:16:26 GMT', 'created': 'Wed, 25 Sep 2019 18:33:38 GMT', 'domain': 'store.steampowered.com'},
                                   {'name': 'birthtime', 'value': '817776001', 'path': '/', 'expires': 'Thu, 24 Sep 2020 7:16:26 GMT', 'created': 'Wed, 25 Sep 2019 18:33:38 GMT', 'domain': 'store.steampowered.com'}])
        else:
            yield from super().start_requests()

    def parse_product(self, response):
        # Circumvent age selection form.
        if not '/agecheck/' in response.url:
            yield load_product(response)
