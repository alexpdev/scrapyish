import atexit
import os
import shutil

import pytest

from scrapyish import Request, Spider
from scrapyish.crawler import Crawler
from scrapyish.http import Response, Selector
from tests import html_sample, json_sample

TESTDIR = "./tests/TESTDIR"


@pytest.fixture
def outfile():
    if os.path.exists(TESTDIR):
        shutil.rmtree(TESTDIR)  # pragma: nocover
    os.mkdir(TESTDIR)
    ofile = os.path.join(TESTDIR, "items.json")
    return ofile


@pytest.fixture
def sample_html():
    return html_sample


@pytest.fixture
def sample_json():
    return json_sample


@pytest.fixture
def sample_request():
    url = "https://fakeurl.com/"
    request = Request(url)
    return request


@pytest.fixture
def sample_response(sample_html, sample_request):
    url = sample_request.url
    response = Response(url, body=sample_html, request=sample_request)
    return response


def test_spider_crawler(outfile):
    class TSpider(Spider):
        name = "testing"
        settings = {"FEEDS_PATH": outfile}

        async def start_requests(self):
            yield Request("https://quotes.toscrape.com")
            for i in range(3):
                yield Request(f"https://quotes.toscrape.com/page/{i}")

        async def parse(self, response):
            for quote in response.css("div.quote"):
                text = quote.xpath(".//text()").getall()
                yield {"text": text}

    crawler = Crawler()
    crawler.crawl(TSpider)
    assert os.path.exists(TSpider.settings["FEEDS_PATH"])


def test_response_raw(sample_response):
    assert len(sample_response.raw) > 0


def test_response_urljoin(sample_response):
    links = sample_response.xpath("//a/@href").getall()
    sample_response._set_url("https://quotes.toscrape.com/")
    for link in links:
        url = sample_response.urljoin(link)
        assert len(url) > 0


def test_text_response_xpath(sample_response):
    selector_list = sample_response.xpath("//text()")
    assert len(selector_list) > 0


def test_json_response(sample_json, sample_request):
    url = sample_request.url
    response = Response(url, body=sample_json, request=sample_request)
    assert isinstance(response.json(), dict)


def test_request_object(sample_html):
    url = "https://fakeurl.com/fake"
    request = Request(url)
    response = Response(request.url, body=sample_html, request=request)
    print(response, response.request, response.url)
    assert not response.json()


def test_selector(sample_html):
    try:
        selector = Selector()
    except ValueError:
        selector = Selector(text=sample_html)
    assert len(selector.css("div")) > 0


@atexit.register
def cleanup():  # pragma: nocover
    if os.path.exists(TESTDIR):
        shutil.rmtree(TESTDIR)
