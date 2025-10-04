BOT_NAME = "news_crawler"

SPIDER_MODULES = ["news_crawler.spiders"]
NEWSPIDER_MODULE = "news_crawler.spiders"

ROBOTSTXT_OBEY = True
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"


MONGO_URI = "mongodb://admin:secret@db:27017"
MONGO_DATABASE = "news"

ITEM_PIPELINES = {
    'news_crawler.pipelines.MongoPipeline': 300,
}
