from dotenv import load_dotenv
import os
import scrapy
import json
from urllib.parse import urlencode
import math
from walmartscraper.walmartscraper.items import WalmartproductItem

load_dotenv()


class WalmartspiderSpider(scrapy.Spider):
    name = "walmartspider"
    allowed_domains = ["walmart.com", "scrapeops.io"]
    page = 1

    settings = {
        "SCRAPEOPS_API_KEY": os.environ.get("SECRET_KEY"),
    }

    def __init__(self, keyword=None, *args, **kwargs):
        super(WalmartspiderSpider, self).__init__(*args, **kwargs)
        self.keyword = keyword
        self.start_urls = [f"https://www.walmart.com/search?q={self.keyword}"]

    def parse(self, response):
        script_tag = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
        script_tag_dicts = json.loads(script_tag)
        products = script_tag_dicts["props"]["pageProps"]["initialData"][
            "searchResult"
        ]["itemStacks"][0]["items"]
        total_product_count = script_tag_dicts["props"]["pageProps"]["initialData"][
            "searchResult"
        ]["itemStacks"][0]["count"]
        max_pages = math.ceil(total_product_count / 40)
        if max_pages > 30:
            max_pages = 30

        product_item = WalmartproductItem()
        for product in products:
            if (product["__typename"]) == "Product":
                product_item["name"] = product["name"]
                product_item["description"] = product["shortDescription"]
                product_item["image_url"] = product["image"]
                product_item["product_url"] = product["canonicalUrl"]
                product_item["rating"] = product["rating"]["averageRating"]
                product_item["reviews"] = product["rating"]["numberOfReviews"]
                product_item["list_price"] = product["priceInfo"]["itemPrice"]
                product_item["sell_price"] = product["priceInfo"]["linePrice"]

                yield product_item
            else:
                yield None

        print(f"{self.page} {max_pages}")
        if self.page < max_pages:
            self.page += 1
            payload = {
                "q": self.keyword,
                "sort": "best_seller",
                "page": self.page,
                "affinityOverride": "default",
            }
            next_page_url = f"https://www.walmart.com/search?" + urlencode(payload)
            yield scrapy.Request(url=next_page_url, callback=self.parse)
