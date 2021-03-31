# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
import os


class StocktickerPipeline:

    def open_spider(self, spider):
        self.exchange = 'NYSE'
        #connect to database
        self.conn = psycopg2.connect(
                host= os.getenv('postgreshost'),
                database="postgres",
                user="postgres",
                password=os.getenv('postgrespassword'))
        self.conn.autocommit=True
        self.curr = self.conn.cursor()
        self.create_ticker_table()
    
    def process_item(self, item, spider):
        company_name = item['company_name']
        ticker = item['ticker']

        high = float(item['high'].replace(",",""))
        low = float(item['low'].replace(",",""))
        close = float(item['close'].replace(",",""))
        volume = float(item['volume'].replace(",",""))
       
        self.save_to_db(ticker=item['ticker'],
                     company_name=item['company_name'],
                     high= high,
                     low=low,
                     close=close,
                     volume=volume
                     )
        return item

    def save_to_db(self,
                ticker,
                company_name,
                high,
                low,
                close,
                volume):
        self.curr.execute("""SELECT * FROM nysetickers
                        WHERE ticker=(%s)""", (ticker,))
        post_qury = self.curr.fetchone()
        if post_qury == None: # create one if one is not found
            print('ticker not found in DB adding')
            self.curr.execute("""INSERT INTO nysetickers
                        (ticker,
                        company_name,
                        high,
                        low,
                        close,
                        volume,
                        exchange)
                        VALUES (%s ,%s, %s, %s, %s, %s, %s)
                        """,
                (ticker,
                company_name,
                high,
                low,
                close,
                volume,
                self.exchange))
     

    def create_ticker_table(self):
        self.curr.execute("""CREATE TABLE IF NOT EXISTS nysetickers (
        id serial,
        ticker varchar(15) NOT NULL,
        company_name varchar(100) NOT NULL,
        high float NOT NULL,
        low float NOT NULL,
        close float NOT NULL,
        volume float NOT NULL,
        exchange varchar(50) NOT NULL
        );""")

    def close_spider(self, spider):
        self.conn.close()
        self.curr.close()