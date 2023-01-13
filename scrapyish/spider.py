class Spider:

    name = None
    start_urls = []

    def start_requests(self):
        pass

    def parse(self, *args, **kwargs):
        pass


class MySpider(Spider):

    name = "example"


    start_urls = ["https://quotes.toscrape.com", "https://quotes.toscrape.com/page/2/"]

    async def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            text = quote.xpath('.//span[@class="text"]/text()').get()
            author = quote.xpath(".//small[@class='author']/text()").get()
            tags = quote.xpath(".//a[@class='tag']/text()").getall()
            yield {"text": text, "author": author, "tags": tags}
