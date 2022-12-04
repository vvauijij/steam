# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


import scrapy


class SteamGame(scrapy.Item):

    """
    steam game class
    """

    name = scrapy.Field()
    categories = scrapy.Field()
    review_amount = scrapy.Field()
    review_score = scrapy.Field()
    release_date = scrapy.Field()
    developer = scrapy.Field()
    tags = scrapy.Field()
    price = scrapy.Field()
    platforms = scrapy.Field()
