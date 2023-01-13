import asyncio
from playwright.async_api import async_playwright

class TextResponse:
    pass




class Crawler:

    def __init__(self, spiderclass):
        self.spider = spiderclass()

    async def crawl(self):
        async with async_playwright() as playwright:
            self.browser = await playwright.chromium.launch()
            L = await asyncio.gather(
                *[self.crawl_url(url) for url in self.spider.start_urls])
            print("L")


    async def crawl_url(self, url):
        page = await self.browser.new_page()
        await page.goto(url)
        html = await page.content()
        print(html)
        response = TextResponse(url, body=html, encoding='utf8')
        async for i in self.spider.parse(response):
            print(i)
