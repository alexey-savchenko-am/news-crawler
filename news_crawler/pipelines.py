from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from typing import Any
from scrapy import Item
from .items import NewsItem
from repositories.article_repository import ArticleRepository
from models.article import Article
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from typing import Any
from scrapy import Item
from .items import NewsItem
from repositories.article_repository import ArticleRepository
from models.article import Article
from pydantic import ValidationError

class MongoPipeline:

    def __init__(self):
        self._article_repo = ArticleRepository()

    def process_item(self, item, spider):
        try:
            if not getattr(item, "content", "").strip() or not getattr(item, "tags", []):
                spider.logger.warning(f"Skipped empty item: {getattr(item, 'url', None)}")
                return item

            if self._article_repo.exists(item.url, item.title):
                spider.logger.info(f"Duplicate skipped: {item.url}")
                return item

            if not isinstance(item, dict):
                item = dict(item)

            news_item = NewsItem(**item)

            try:
                article = Article(
                    source=news_item.source,
                    title=news_item.title,
                    url=news_item.url,
                    tags=news_item.tags,
                    content=news_item.content,
                    article_date=news_item.date,
                )
            except ValidationError as e:
                spider.logger.error(f"Validation error: {e.errors()}")
                return item

            self._article_repo.create(article)
            spider.logger.info(f"✅ Saved article: {article.title}")

        except Exception as e:
            spider.logger.error(f"Error processing item: {e}", exc_info=True)

        return item