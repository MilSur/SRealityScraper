import json
import selenium
import re
from database import get_db
from webdriver import get_webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.selector import Selector
 
class SRealityFlatsScraper():
    def __init__(self, limit=500):
        # Connect database and create table:'
        self.connection = get_db()
        self.cursor = self.connection.cursor()
        self.cursor.execute('DROP TABLE IF EXISTS flats;')
        self.cursor.execute('CREATE TABLE flats (data jsonb);')

        # Connect webdriver:
        self.driver = get_webdriver()

        # Number of flats to be scraped
        self.limit = limit

    def __enter__(self):
        return self
 
    def __exit__(self, type, value, traceback):
        self.cursor.close()
        self.connection.close()
        self.driver.quit()
    
    def open_page(self, page_num):
        try:
            self.driver.get("https://www.sreality.cz/hledani/prodej/byty?strana={:}".format(page_num))
        except selenium.common.exceptions.WebDriverException:
            self.open_page(page_num)

    def fetch_single_page(self, page_num):
        self.open_page(page_num)
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.property.ng-scope")))
            page_html = Selector(text=self.driver.page_source)
            flats = page_html.css('div.property.ng-scope')

            for flat in flats:
                flat_json = json.dumps({
                    'title': flat.css('span.name.ng-binding::text').get(),
                    'locality': flat.css('span.locality.ng-binding::text').get(),
                    'price': flat.css('span.norm-price.ng-binding::text').get(),
                    'tags': [re.sub('\s+','',tag) for tag in flat.css('span.label.ng-binding.ng-scope::text').getall()],
                    'images': [im for im in flat.css('img::attr(src)').getall() if not 'camera.svg' in im]
                    }
                )
                insert_query = "INSERT INTO flats (data) VALUES (%s) RETURNING data"
                self.cursor.execute(insert_query, (flat_json,))

                self.cursor.execute('SELECT count(*) FROM flats;')
                listings_num = self.cursor.fetchone()[0]
                print('Flat #{:}/{:} has been logged.'.format(listings_num, self.limit))
                if listings_num >= self.limit:
                    break

            return listings_num < self.limit
    
        except selenium.common.exceptions.TimeoutException:
            return False

    def fetch_all(self):
        page_num = 1
        print('Please wait, {:} flats listing is about to be scraped.'.format(self.limit))
        while self.fetch_single_page(page_num):
            page_num += 1 
        print('Scraping complete!')

         

 