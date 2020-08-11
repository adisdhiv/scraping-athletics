# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter
from twisted.python.compat import unicode

class AdrianprojectPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['phone']:
            adapter['phone'] = adapter['phone'].replace("Phone: ", "")
        return item

class CsvPipeline(object):
    def __init__(self):
        self.file = open("sports.csv", 'wb')
        self.exporter = CsvItemExporter(self.file, unicode)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)