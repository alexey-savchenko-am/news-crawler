# pipelines.py
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from typing import Any
from scrapy import Item
from .items import NewsItem

class MongoPipeline:
    collection_name = "articles"

    def __init__(self, mongo_uri: str, mongo_db: str):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client: MongoClient | None = None
        self.db: Any = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings["MONGO_URI"],
            mongo_db=crawler.settings["MONGO_DATABASE"]
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        if self.client:
            self.client.close()

    def process_item(self, item: NewsItem | Item, spider):
       
        # content is empty
        if not item.content.strip():
            return
        
        # checking for duplicates by article url
        existing =  self.db[self.collection_name].find_one({"url": item.url})
        if existing:
            return

        if not isinstance(item, dict):
            item = dict(item)
       
        news_item = NewsItem(**item)

        try:
            self.db[self.collection_name].insert_one(news_item.model_dump())
        except DuplicateKeyError:
            spider.logger.info(f"Duplicate skipped: {item.url}")

        return news_item
