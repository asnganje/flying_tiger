# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from openpyxl import Workbook
from openpyxl import Workbook
from openpyxl.styles import Font


class FlytScraperPipeline:
    def process_item(self, item):
        return item
class ExcelPipeline:

    def open_spider(self, spider):
        self.workbook = Workbook()
        self.sheet = self.workbook.active
        self.sheet.title = "FTigerProducts"

        headers = [
            "Serial No",
            "Name",
            "price",
            "Product code",
            "Image URL",
            "Product URL"
        ]

        self.sheet.append(headers)

        for cell in self.sheet[1]:
            cell.font = Font(bold=True)
        self.serial_number = 1

    def process_item(self, item, spider):
        self.sheet.append([
            self.serial_number,
            item['name'],
            item['price'],
            item['product_code'],
            item['image_url'],
            item['product_url']
        ])

        self.serial_number += 1
        return item
    def close_spider(self, spider):
        self.workbook.save("ftigers.xlsx")




