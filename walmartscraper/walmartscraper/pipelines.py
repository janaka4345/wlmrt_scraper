# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class WalmartscraperPipeline:
    def process_item(self, item, spider):
        return item


class WalmartscraperCleanupPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get("description"):
            description = adapter["description"]
            new_description = (
                description.replace("<li>", "")
                .replace("</li>", "")
                .replace("<strong>", "")
                .replace("</strong>", "")
            )
            adapter["description"] = new_description

        if adapter.get("list_price"):
            float_list_price = float(adapter["list_price"].replace("$", ""))
            adapter["list_price"] = float_list_price

        if adapter.get("sell_price"):
            float_sell_price = float(adapter["sell_price"].replace("$", ""))
            adapter["sell_price"] = float_sell_price

        return item
