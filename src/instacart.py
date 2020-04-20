import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from twilio.rest import Client
from datetime import datetime
from src.utils import get_credentials, get_logger
from selenium.webdriver.firefox.options import Options


LOGGER = get_logger()


class InstaCartManger:
    def __init__(self):
        options = Options()
        # options.headless = True
        self.driver = webdriver.Firefox(options=options, executable_path='./firefoxdriver-mac')
        self.email = ''
        self.pw = ''
        self.sid = ''
        self.auth_token = ''

    def start(self):
        self.set_credentials()
        self.driver.get("http://www.instacart.com")
        self.sign_in()
        self.access_delivery_page()
        while True:
            self.check_time_window()

    def set_credentials(self):
        data = get_credentials()
        self.email = data['insta_cart']['email']
        self.pw = data['insta_cart']['password']
        self.sid = data['twillio']['sid']
        self.auth_token = data['twillio']['auth_token']
        LOGGER.info('credential loaded')

    @staticmethod
    def hover(d, el):
        action = ActionChains(d).move_to_element(el)
        action.perform()

    def sign_in(self):
        time.sleep(1)
        signin_btn = self.driver.find_element_by_xpath('//*[@id="root"]/div/div/header/div/div[2]/div/button')
        self.hover(self.driver, signin_btn)
        time.sleep(1)
        signin_btn.click()
        email_field = self.driver.find_element_by_xpath('//*[@id="nextgen-authenticate.all.log_in_email"]')
        email_field.send_keys(self.email)
        pw_field = self.driver.find_element_by_xpath('//*[@id="nextgen-authenticate.all.log_in_password"]')
        pw_field.send_keys(self.pw)
        signin_btn = self.driver.find_element_by_xpath('//*[@id="main-content"]/div[2]/form/div[3]/button')
        time.sleep(1)
        signin_btn.click()
        time.sleep(5)
        LOGGER.info('sign in completed')

    def access_delivery_page(self):
        self.driver.get("http://www.instacart.com/store/checkout_v3")
        time.sleep(1)
        LOGGER.info('delivery page accessed')

    def check_time_window(self):
        time.sleep(5)
        sorry_els = self.driver.find_elements_by_xpath(
            "//*[contains(text(), 'all shoppers are busy')]")
        if len(sorry_els) > 0:
            LOGGER.info('No time window, refresh...')
            time.sleep(5)
            self.driver.refresh()
        else:
            LOGGER.info('Time window found')
            self.send_sms('InstaCart has delivery time window!')
            time.sleep(600)

    def send_sms(self, text):
        account_sid = self.sid
        auth_token = self.auth_token
        client = Client(account_sid, auth_token)
        client.messages.create(
            body='{} - {}'.format(text, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            from_='+12062226523',
            to='+12019686330'
        )
