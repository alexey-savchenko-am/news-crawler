import scrapy
from news_crawler.items import NewsItem
from datetime import datetime, timezone
from news_crawler.utils import DateExtractor

class GuardianSpider(scrapy.Spider):
    name = "guardian"
    allowed_domains = ["theguardian.com"]
    start_urls = [
        "https://www.theguardian.com/world",
        "https://www.theguardian.com/world/europe-news",
        "https://www.theguardian.com/us-news",
        "https://www.theguardian.com/world/americas",
        "https://www.theguardian.com/world/asia",
        "https://www.theguardian.com/australia-news",
        "https://www.theguardian.com/world/middleeast",
        "https://www.theguardian.com/world/africa",
        "https://www.theguardian.com/inequality",
        "https://www.theguardian.com/global-development",
        "https://www.theguardian.com/football",
        "https://www.theguardian.com/sport/cricket",
        "https://www.theguardian.com/sport/golf",
        "https://www.theguardian.com/sport/us-sport",
        "https://www.theguardian.com/sport/all?utm_source=chatgpt.com",
    ]

    def parse(self, response):
        for article in response.css("li"):
            link = article.css("a.dcr-2yd10d::attr(href)").get()
            if link:
                yield response.follow(link, callback=self.parse_article)

    def parse_article(self, response):

        title = response.css("h1::text").get() or response.css("h1 span::text").get()
        content = " ".join(response.css("div.article-body-commercial-selector p::text").getall())
        tags = [tag.strip().lower() for tag in response.css("div.dcr-1ashyvn ul li a::text").getall()] 
        date = DateExtractor.extract_iso_date(response) or datetime.now(timezone.utc)

        yield NewsItem (
            source = "Guardian",
            title = title,
            url= response.url,
            date=date,
            content = content,
            tags = tags
        )
