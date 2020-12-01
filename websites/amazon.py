from decouple import config
import time
from selenium.common.exceptions import NoSuchElementException
from .website import WebsiteBuyer

# env variables
amazon_product = config('AMAZON_PRODUCT')
amazon_email = config('AMAZON_EMAIL')
amazon_password = config('AMAZON_PASSWORD')
refresh_seconds = int(config('AMAZON_REFRESH_SECONDS'))


class AmazonBuyer (WebsiteBuyer):
    def __init__(self, driver, check_bought_across_websites):
        super(AmazonBuyer, self).__init__(driver, "amazon", amazon_product, refresh_seconds, check_bought_across_websites)


    def is_signed_in(self):
        account_btn = self.driver.find_element_by_id("nav-link-accountList")
        dnr_attr = account_btn.get_attribute("data-nav-ref")
        if dnr_attr == "nav_ya_signin":
            return False
        elif dnr_attr == "nav_youraccount_btn":
            return True
        else:
            raise Exception("Uncheckable signin status")


    def login(self):
        with self.wait_for_page_load():
            self.driver.find_element_by_id("nav-link-accountList").click()

        with self.wait_for_page_load():
            email = self.driver.find_element_by_id("ap_email")
            email.send_keys(amazon_email)
            # click continue 
            self.driver.find_element_by_id("continue").click()

        with self.wait_for_page_load():
            password = self.driver.find_element_by_id("ap_password")
            password.send_keys(amazon_password)
            # sign in
            self.driver.find_element_by_id("signInSubmit").click()
        

    def try_buy(self):
        try:
            buy_now_btn = self.driver.find_element_by_id("buy-now-button")

            with self.wait_for_page_load():
                buy_now_btn.click()
                print("cliccato il primo")
            
            self.driver.find_element_by_name("placeYourOrder1").click()

        except NoSuchElementException:
            print("failed diok")
            return False
        return True
