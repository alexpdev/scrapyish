import asyncio
import sys
import argparse
from scrapyish import spider
from scrapyish.spider import Spider
from scrapyish.crawler import Crawler



def get_spider_classes():
    yield from filter(
        lambda x: hasattr(x, 'name'),
        map(lambda x: spider.__dict__[x],
        dir(spider)))



def start_spider(args):
    for spiderclass in get_spider_classes():
        if spiderclass.name == args.spidername:
            crawler = Crawler(spiderclass)
            asyncio.run(crawler.crawl())
