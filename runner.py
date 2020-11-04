from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from labirintparser import settings
from labirintparser.spiders.labirint import LabirintSpiders

if __name__ =="__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LabirintSpiders)

    process.start()

