# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from openpyxl import Workbook
from openpyxl import Workbook
from openpyxl.styles import Font
import gspread
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import  os


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

class GoogleSheetsPipeline:
    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    CLIENT_SECRET_FILE = "client_secret.json"
    TOKEN_FILE = "token.json"

    def open_spider(self, spider):

        credentials = None
        if os.path.exists(self.TOKEN_FILE):
            credentials = Credentials.from_authorized_user_file(self.TOKEN_FILE, self.SCOPES, )
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.CLIENT_SECRET_FILE, self.SCOPES, )
                credentials = flow.run_local_server(port=0)
            with open(self.TOKEN_FILE, "w") as token:
                token.write(credentials.to_json())
        self.client = gspread.authorize(credentials)
        self.spreadsheet = self.client.create("Flying Tiger Products")
        self.sheet = self.spreadsheet.sheet1

        self.headers = [
            "Serial No",
            "Name",
            "Price",
            "Product Code",
            "Image URL",
            "Product URL"
        ]
        self.sheet.append_row(self.headers)

        self.sheet.format(
            "A1:F1",
            {
                "textFormat":{
                    "bold": True
                }
            }
        )
        self.serial_number = 1
        self.spreadsheet.share(
            None,
            perm_type="anyone",
            role="reader"
        )

    def process_item(self, item, spider):
        row = [
            self.serial_number,
            item['name'],
            item['price'],
            item['product_code'],
            item['image_url'],
            item['product_url']
        ]

        self.sheet.append_row(row)
        self.serial_number += 1
        return  item







