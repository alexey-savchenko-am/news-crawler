import scrapy
from scrapy.http import HtmlResponse, Response, Request
from news_crawler.items import NewsItem
from datetime import datetime, timezone
from news_crawler.utils import TagExtractor, DateExtractor

class CnnSpider(scrapy.Spider):
    name = "cnn"
    allowed_domains = ["edition.cnn.com"]
    start_urls = [
        "https://edition.cnn.com/",
        "https://edition.cnn.com/world",
        "https://edition.cnn.com/business",
        "https://edition.cnn.com/tech",
        "https://edition.cnn.com/us",
        "https://edition.cnn.com/asia",
        "https://edition.cnn.com/australia",
        "https://edition.cnn.com/china",
        "https://edition.cnn.com/europe",
        "https://edition.cnn.com/india",
    ]

    def parse(self, response: HtmlResponse):
        for link in response.css("li.card a::attr(href)").getall():
            url: str = response.urljoin(link)
            yield response.follow(url, callback=self.parse_article)

    def parse_article(self, response: HtmlResponse):
        title = response.css("h1::text").get(default="").strip()
        paragraphs = response.css("div.article__content p::text").getall()
        content = " ".join(p.strip() for p in paragraphs if p.strip())
        date=DateExtractor.extract_iso_date(response) or datetime.now(timezone.utc)
        tags = TagExtractor.extract_tags(title)

        yield NewsItem (
            source = "CNN",
            title = title,
            url= response.url,
            date=date,
            content = content,
            tags = tags
        )
