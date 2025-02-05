from datetime import datetime, date
import logging
import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Compose, Join, MapCompose, TakeFirst

logger = logging.getLogger(__name__)


class StripText:
    def __init__(self, chars=' \r\t\n'):
        self.chars = chars

    def __call__(self, value):
        try:
            return value.strip(self.chars)
        except:  # noqa E722
            return value


def simplify_recommended(x):
    return True if x == 'Recommended' else False


def standardize_date(x):
    """
    Convert x from recognized input formats to desired output format,
    or leave unchanged if input format is not recognized.
    """
   
    for fmt in ['%d %b, %Y', '%d %B, %Y', '%b %d, %Y', '%B %d, %Y']:
        try:
            return datetime.strptime(x, fmt).strftime('%d-%m-%Y')
        except ValueError:
            pass

    # Induce year to current year if it is missing.
    for fmt in ['%b %d', '%B %d', '%d %b', '%d %B']:
        try:
            d = datetime.strptime(x, fmt)
            d = d.replace(year=date.today().year)
            return d.strftime('%d-%m-%Y')
        except ValueError:
            pass

    # Format not supported
    logger.debug(f'Could not process date {x}')
    return x


def str_to_float(x):
    x = x.replace(',', '.')
    try:
        return float(x)
    except:  # noqa E722
        return x


def str_to_int(x):
    try:
        return int(str_to_float(x))
    except:  # noqa E722
        return x


class ProductItem(scrapy.Item):
    id = scrapy.Field(
        output_processor=Compose(TakeFirst(), str_to_int)
    )
    title = scrapy.Field()
    genres = scrapy.Field(
        output_processor=Compose(TakeFirst(), lambda x: x.split(','), MapCompose(StripText()))
    )
    developer = scrapy.Field(
        output_processor=Compose(TakeFirst(), lambda x: x.split(", "), MapCompose(StripText()))
    )
    publisher = scrapy.Field(
        output_processor=Compose(TakeFirst(), lambda x: x.split(", "), MapCompose(StripText()))
    )
    release_date = scrapy.Field(
        output_processor=Compose(TakeFirst(), StripText(), standardize_date)
    )
    features = scrapy.Field(
        output_processor=MapCompose(StripText())
    )
    tags = scrapy.Field(
        output_processor=MapCompose(StripText())
    )
    price = scrapy.Field(
        output_processor=Compose(TakeFirst(),
                                 StripText(chars=' €$\n\t\r'),
                                 str_to_float)
    )
    discount_price = scrapy.Field(
        output_processor=Compose(TakeFirst(),
                                 StripText(chars=' €$\n\t\r'),
                                 str_to_float)
    )
    sentiment = scrapy.Field()
    percent_positive = scrapy.Field(
        output_processor=Compose(TakeFirst(), str_to_int)
    )
    n_reviews = scrapy.Field(
        output_processor=Compose(
            MapCompose(StripText(), lambda x: x.replace(',', ''), str_to_int),
            max
        )
    )
    early_access = scrapy.Field()
    description = scrapy.Field()
    franchise = scrapy.Field()
    about = scrapy.Field()


class ReviewItem(scrapy.Item):
    product_id = scrapy.Field(
        output_processor=Compose(TakeFirst(), str_to_int)
    )
    recommended = scrapy.Field(
        output_processor=Compose(TakeFirst(), simplify_recommended),
    )
    date = scrapy.Field(
        output_processor=Compose(TakeFirst(), standardize_date)
    )
    text = scrapy.Field(
        input_processor=MapCompose(StripText()),
        output_processor=Compose(Join('\n'), StripText())
    )
    hours = scrapy.Field(
        output_processor=Compose(TakeFirst(), lambda x: x.replace(',', ''), str_to_float)
    )
    found_helpful = scrapy.Field(
        output_processor=Compose(TakeFirst(), lambda x: x.replace(',', ''), str_to_int)
    )
    found_funny = scrapy.Field(
        output_processor=Compose(TakeFirst(), lambda x: x.replace(',', ''), str_to_int)
    )
    compensation = scrapy.Field()
    username = scrapy.Field()
    products = scrapy.Field(
        output_processor=Compose(TakeFirst(), str_to_int)
    )
    early_access = scrapy.Field()


class ProductItemLoader(ItemLoader):
    default_output_processor = Compose(TakeFirst(), StripText())


class ReviewItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
