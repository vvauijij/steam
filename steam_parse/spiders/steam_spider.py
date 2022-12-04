import scrapy
import requests

from steam_parse.items import SteamGame


class SteamSpider(scrapy.Spider):

    """
    class to parse steam games data from pages (param) in queries (param)
    """

    name = 'steam_spider'
    start_urls = ['https://store.steampowered.com/search/']
    queries = ['moba', 'shooter', 'strategy']
    pages_to_parse = [1, 2, 3, 4]

    def parse(self, response):
        for query in self.queries:
            for page_index in self.pages_to_parse:

                link = f'{self.start_urls[0]}?term={query}&ignore_preferences=1&page={page_index}'
                yield response.follow(link, callback=self.parse_result_page)

    @staticmethod
    def get_urls(response):
        urls = set()

        for url_obj in response.xpath('//*[@id="search_resultsRows"]/a/@href'):
            url_obj = url_obj.get().strip()
            if 'app' in url_obj and 'agecheck' not in url_obj:
                urls.add(url_obj)

        return urls

    def parse_result_page(self, response):
        for url in self.get_urls(response):
            yield response.follow(url, callback=self.parse_game_page)

    def parse_game_page(self, response):
        items = SteamGame()

        try:
            # parse game release date
            items['release_date'] = response.css(
                'div.grid_date::text')[1].get().strip()

            if (int(items['release_date'][-4:]) <= 2000):
                yield

            # parse game name
            items['name'] = response.xpath(
                '//*[@id="appHubAppName_responsive"]/text()').get().strip()

            # parse game category
            categories = list()
            for category in response.css('div.blockbg a::text'):
                category = category.get().strip()
                categories.append(category)

            if len(categories) > 0:
                items['categories'] = ' --> '.join(categories[1:])

            # parse game review amount
            items['review_amount'] = response.css(
                'span.responsive_hidden::text').get().strip()[1:-1]

            # parse game review score
            items['review_score'] = response.css(
                'span.game_review_summary::text').get().strip()

            # parse game developer
            items['developer'] = response.css('div.grid_content a::text')[
                0].get().strip()

            # parse game tags
            tags = list()
            for tag in response.css('div.popular_tags a::text'):
                tags.append(tag.get().strip())
            items['tags'] = tags

            # parse game price
            items['price'] = response.css(
                'div.game_purchase_price::text').get().strip()

            # parse game platforms
            platforms = set()
            for platform in response.css('div').xpath('@data-os'):
                platforms.add(platform.get().strip())
            items['platforms'] = list(platforms)

            yield items

        except:
            yield
