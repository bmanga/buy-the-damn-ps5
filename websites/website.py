from contextlib import contextmanager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import \
  staleness_of
import time
import os
from pathlib import Path

class WebsiteBuyer:
    def __init__(self, driver, website_name, product_url, refresh_seconds, check_bought_across_websites):
        self.product_url = product_url
        self.driver = driver
        self.website_name = website_name
        self.refresh_seconds = refresh_seconds
        self.check_bought_across_websites = check_bought_across_websites

    def is_signed_in(self):
        raise NotImplementedError

    def login(self):
        raise NotImplementedError
        

    def try_buy(self):
        raise NotImplementedError

    def mark_bought(self):
        Path(self.website_name + ".lock").touch()
        Path("global.lock").touch()

    def notify_bought(self):
        print(self.website_name, ": Item bought")

    def check_already_bought(self):
        bought = os.path.exists(self.website_name + ".lock")
        if self.check_bought_across_websites:
            bought = bought or os.path.exists("global.lock")
        return bought

    @contextmanager
    def wait_for_page_load(self, timeout=10):
        old_page = self.driver.find_element_by_tag_name('html')
        yield
        WebDriverWait(self.driver, timeout).until(
            staleness_of(old_page)
        )

    def run(self):
        while True:
            start = time.time()
            if self.check_already_bought():
                print(self.website_name, "loop terminated: Item already bought")
                return
            
            self.driver.get(self.product_url)

            if not self.is_signed_in():
                self.login()
                # Ensure we are back at the correct page
                if self.driver.current_url != self.product_url:
                    self.driver.get(self.product_url)

            if self.try_buy():
                self.mark_bought()
                self.notify_bought()
                return

            end = time.time()
            time.sleep(self.refresh_seconds - (end - start))
