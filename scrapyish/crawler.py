import os
import json
import asyncio
import scrapyish
from playwright.async_api import async_playwright
from scrapyish.http import Response

class Crawler:

    def __init__(self, spiderclass=None, settings=None):
        self.settings = settings
        self.spiderclass = spiderclass
        self.crawling = False
        self.spider = None

    async def crawl(self, spiderclass=None):
        if self.crawling:
            raise RuntimeError("Crawling is already taking place")
        self.crawling = True
        if self.spiderclass is not None:
            self.spider = self.spiderclass(self)
        elif spiderclass is not None:
            self.spider = spiderclass(self)
            self.spiderclass = spiderclass
        self.scheduler = asyncio.Queue(maxsize=self.spiderclass.settings["CONCURRENT_REQUESTS"])
        self.outpath = self.spiderclass.settings["FEEDS_PATH"]
        async with async_playwright() as playwright:
            self.browser = await playwright.chromium.launch()
            await self.run_spider()

    async def run_spider(self):
        tasks = []
        async for request in self.spider.start_requests():
            await self.scheduler.put(request)
            task = asyncio.create_task(self.crawl_request())
            tasks.append(task)


    async def crawl_request(self):
        request = self.scheduler.get()
        page = await self.browser.new_page()
        await page.goto(request.url)
        html = await page.content()
        response = Response(request.url, body=html, encoding='utf8', page=page, browser=self.browser, request=request)
        callback = request._callback
        if request._callback is None:
            callback = self.spider.parse
        async for item in callback(response, **request.cb_kwargs):
            if isinstance(item, dict):
                if os.path.exists(self.outpath):
                    data = json.load(open(self.outpath, 'rt'))
                    data.append(item)
                    json.dump(data, open(self.outpath, 'wt'))
            elif isinstance(item, scrapyish.Request):
                await self.scheduler.put(item)
            
