from selenium import webdriver
import chromedriver_binary
from websites.amazon import AmazonBuyer


driver = webdriver.Chrome()

amazon = AmazonBuyer(driver, False)

amazon.run()


