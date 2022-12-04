# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
import json


class SteamParsePipeline:
    def open_spider(self, spider) -> None:
        """
        create json file field to write parsed data after opening spider
        """

        self.parsed_games = open('parsed_games.json', 'w')

    def close_spider(self, spider) -> None:
        """
        close json file field after closing spider
        """

        self.parsed_games.close()

    def process_item(self, item, spider):
        """
        write parsed data to json file field
        """

        line = f'{json.dumps(ItemAdapter(item).asdict(), skipkeys=True)}\n'
        self.parsed_games.write(line)

        return item
