import re
import sys
import random as rndm

import scrapy
from scrapy.http import FormRequest, Request
from w3lib.url import url_query_parameter

from ..items import ReviewItem, ReviewItemLoader, str_to_int


def load_review(review, product_id, page, order):
    """
    Load a ReviewItem from a single review.
    """
    loader = ReviewItemLoader(ReviewItem(), review)

    loader.add_value('product_id', product_id)

    # Review data.
    loader.add_css('recommended', '.title::text')
    loader.add_css('date', '.date_posted::text', re='Posted: (.+)')
    loader.add_css('text', '.apphub_CardTextContent::text')
    loader.add_css('hours', '.hours::text', re='(.+) hrs')
    loader.add_css('compensation', '.received_compensation::text')

    # User/reviewer data.
    loader.add_css('username', '.apphub_CardContentAuthorName a::text')
    loader.add_css('products', '.apphub_CardContentMoreLink ::text', re='([\d,]+) product')

    # Review feedback data.
    feedback = loader.get_css('.found_helpful ::text')
    loader.add_value('found_helpful', feedback, re='([\d,]+).*helpful')
    loader.add_value('found_funny', feedback, re='([\d,]+).*funny')

    early_access = loader.get_css('.early_access_review')
    if early_access:
        loader.add_value('early_access', True)
    else:
        loader.add_value('early_access', False)

    return loader.load_item()


def get_page(response):
    from_page = response.meta.get('from_page', None)

    if from_page:
        page = from_page + 1
    else:
        page = url_query_parameter(response.url, 'p', None)
        if page:
            page = str_to_int(page)

    return page


def get_product_id(response):
    product_id = response.meta.get('product_id', None)

    if not product_id:
        try:
            return re.findall("app/(.+?)/", response.url)[0]
        except:  # noqa E722
            return None
    else:
        return product_id


class ReviewSpider(scrapy.Spider):
    name = 'reviews'

    game_id_to_number_reviews = dict()

    def __init__(self, url_file=None, steam_id=None, games_file=None, limit=sys.maxsize, random=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url_file = url_file
        self.steam_id = steam_id
        self.games_file = games_file
        self.random = random
        self.limit = int(limit)
        if random:
            self.limit_per_game = dict()
            rndm.seed()

    def read_urls(self):
        with open(self.url_file, 'r') as f:
            for url in f:
                url = url.strip()
                if url:
                    id = re.search('/(\d+)/', url).group(1)
                    self.game_id_to_number_reviews[id] = 0
                    yield scrapy.Request(url, callback=self.parse)

    def read_games(self):
        with open(self.games_file, 'r') as f:
            for game in f:
                game_id = re.search('\"id\": (\d+)', game).group(1)
                if game_id:
                    self.game_id_to_number_reviews[game_id] = 0
                    url = f'https://steamcommunity.com/app/{game_id}/reviews/?browsefilter=toprated&p=1'
                    yield scrapy.Request(url, callback=self.parse)
                

    def start_requests(self):
        if self.steam_id:
            # Ordered by most helpful of all time
            url = (
                f'https://steamcommunity.com/app/{self.steam_id}/reviews/?browsefilter=toprated&p=1'
            )
            self.game_id_to_number_reviews[self.steam_id] = 0
            yield Request(url, callback=self.parse)
        elif self.url_file:
            yield from self.read_urls()
        elif self.games_file:
            yield from self.read_games()


    def parse(self, response):
        page = get_page(response)
        product_id = get_product_id(response)

        # Load all reviews on current page.
        reviews = response.css('div .apphub_Card')
        for i, review in enumerate(reviews):
            yield load_review(review, product_id, page, i)
            self.game_id_to_number_reviews[product_id] += 1
            if self.random:
                if not product_id in self.limit_per_game:
                    self.limit_per_game[product_id] = rndm.randint(0, self.limit)
                if self.game_id_to_number_reviews[product_id] >= self.limit_per_game[product_id]:
                    del self.game_id_to_number_reviews[product_id]
                    return
            else:
                if self.game_id_to_number_reviews[product_id] >= self.limit:
                    del self.game_id_to_number_reviews[product_id]
                    return

        # Navigate to next page.
        form = response.xpath('//form[contains(@id, "MoreContentForm")]')
        if form:
            yield self.process_pagination_form(form, page, product_id)

    def process_pagination_form(self, form, page=None, product_id=None):
        action = form.xpath('@action').extract_first()
        names = form.xpath('input/@name').extract()
        values = form.xpath('input/@value').extract()

        formdata = dict(zip(names, values))
        meta = dict(prev_page=page, product_id=product_id)

        return FormRequest(
            url=action,
            method='GET',
            formdata=formdata,
            callback=self.parse,
            meta=meta
        )
