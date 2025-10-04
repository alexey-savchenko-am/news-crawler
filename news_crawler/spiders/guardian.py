import scrapy
from news_crawler.items import NewsItem
from datetime import datetime

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
    ]

    def parse(self, response):
        for article in response.css("li"):
            link = article.css("a.dcr-2yd10d::attr(href)").get()
            if link:
                yield response.follow(link, callback=self.parse_article)

    def parse_article(self, response):

        title = response.css("h1::text").get() or response.css("h1 span::text").get()

        date_str = response.xpath('//meta[@property="article:published_time"]/@content').get()
        date_obj = datetime.fromisoformat(date_str.replace("Z", "+00:00"))

        yield NewsItem (
            source = "Guardian",
            title = title,
            url= response.url,
            date=date_obj,
            content = " ".join(response.css("div.article-body-commercial-selector p::text").getall()),
            tags = response.css("div.dcr-1ashyvn ul li a::text").getall()
        )
