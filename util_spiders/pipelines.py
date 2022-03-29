# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from util_spiders.items import FileItem


class FileItemPipeline:
    def process_item(self, item, spider):
        if isinstance(item, FileItem):
            with open(item['path'], 'wb') as f:
                f.write(item['context'])
        return item
