from dotenv import load_dotenv
import os
import scrapy
import json
from walmartscraper.walmartscraper.items import WalmartproductItem

load_dotenv()

class WalmartspiderSpider(scrapy.Spider):
    name = "walmartspider"
    allowed_domains = ["walmart.com", "scrapeops.io"]
    # start_urls = [
    #     "https://proxy.scrapeops.io/v1/?api_key=********************&url=https://www.walmart.com/search?q=iphones"
    # ]
    scrapy_url = f"https://proxy.scrapeops.io/v1/?api_key={os.environ.get("SECRET_KEY")}&url="

    def __init__(self, keyword=None, *args, **kwargs):
        super(WalmartspiderSpider, self).__init__(*args, **kwargs)
        self.start_urls = [
            f"{self.scrapy_url}https://www.walmart.com/search?q={keyword}"
        ]

    def parse(self, response):
        print(response.xpath("//html"))
        script_tag = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
        script_tag_dicts = json.loads(script_tag)
        # print(script_tag_dicts)
        products = script_tag_dicts["props"]["pageProps"]["initialData"][
            "searchResult"
        ]["itemStacks"][0]["items"]

        product_item = WalmartproductItem()
        for product in products:
            product_item["name"] = product["name"]
            product_item["description"] = product["shortDescription"]
            product_item["image_url"] = product["image"]
            product_item["product_url"] = product["canonicalUrl"]
            product_item["rating"] = product["rating"]["averageRating"]
            product_item["reviews"] = product["rating"]["numberOfReviews"]
            product_item["list_price"] = product["priceInfo"]["itemPrice"]
            product_item["sell_price"] = product["priceInfo"]["linePrice"]

            yield product_item
