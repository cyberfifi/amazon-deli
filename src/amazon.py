import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from twilio.rest import Client
from src.utils import get_credentials, get_logger
from selenium.webdriver.chrome.options import Options

LOGGER = get_logger()


class AmazonManger:
    def __init__(self, is_whole_foods):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(
            executable_path='./chromedriver-mac',
            chrome_options=chrome_options)
        self.email = ''
        self.pw = ''
        self.sid = ''
        self.auth_token = ''
        self.phone_number = []
        self.is_whole_foods = is_whole_foods
        self.name = 'Whole Foods' if self.is_whole_foods else 'Amazon Fresh'
        self.set_credentials()

    def sign_in(self):
        self.driver.get("https://www.amazon.com")
        account_list = self.driver.find_element_by_id('nav-link-accountList')
        self.hover(self.driver, account_list)
        time.sleep(1)
        signin_btn = self.driver.find_element_by_xpath('//*[@id="nav-flyout-ya-signin"]/a/span')
        self.hover(self.driver, signin_btn)
        time.sleep(1)
        signin_btn.click()
        email_field = self.driver.find_element_by_xpath('//*[@id="ap_email"]')
        email_field.send_keys(self.email)
        continue_btn = self.driver.find_element_by_xpath('//*[@id="continue"]')
        time.sleep(1)
        continue_btn.click()
        pw_field = self.driver.find_element_by_xpath('//*[@id="ap_password"]')
        pw_field.send_keys(self.pw)
        keep_session_box = self.driver.find_element_by_xpath(
            '//*[@id="authportal-main-section"]/div[2]/div/div/div/form/div/div[2]/div/div/label/div/label/input')
        keep_session_box.click()
        time.sleep(1)
        signin_btn = self.driver.find_element_by_xpath('//*[@id="signInSubmit"]')
        time.sleep(1)
        signin_btn.click()
        time.sleep(1)
        is_two_fa_page = len(self.driver.find_elements_by_xpath(
            "//*[contains(text(), 'Where should we send the communication?')]")) > 0
        if is_two_fa_page:
            radios = self.driver.find_elements_by_xpath('//*[@type="radio"]')
            radios[0].click()
            time.sleep(1)
            continue_btn = self.driver.find_element_by_xpath('//*[@id="continue"]')
            continue_btn.click()
            LOGGER.info('2FA sent')
            time.sleep(60)
        LOGGER.info('sign in completed')

    def start(self):
        self.driver.get("https://www.amazon.com")
        self.access_delivery_page()
        self.check_time_window()

    def set_credentials(self):
        data = get_credentials()
        self.email = data['amazon']['email']
        self.pw = data['amazon']['password']
        self.sid = data['twillio']['sid']
        self.auth_token = data['twillio']['auth_token']
        self.phone_number = data['phone_number']
        LOGGER.info('credential loaded')

    @staticmethod
    def hover(d, el):
        action = ActionChains(d).move_to_element(el)
        action.perform()

    def go_to_home(self):
        self.driver.get("http://www.amazon.com")

    def access_delivery_page(self):
        cart_btn = self.driver.find_element_by_xpath('//*[@id="nav-cart"]')
        cart_btn.click()
        time.sleep(3)
        if self.is_whole_foods:
            check_out_btn = self.driver.find_element_by_xpath(
                "//*[contains(text(), 'Checkout Whole Foods Market Cart')]/../input")
        else:
            check_out_btn = self.driver.find_element_by_xpath(
                "//*[contains(text(), 'Checkout Amazon Fresh Cart')]/../input")
        time.sleep(1)
        check_out_btn.click()
        time.sleep(1)
        continue_btn = self.driver.find_element_by_xpath('//*[@id="a-autoid-0"]/span/a')
        continue_btn.click()
        if self.is_whole_foods:
            time.sleep(1)
            continue_btn = self.driver.find_element_by_xpath('//*[@id="subsContinueButton"]/span/input')
            continue_btn.click()
        time.sleep(1)
        LOGGER.info('accessed {} delivery page'.format(self.name))

    def check_time_window(self):
        date_containers = self.driver.find_elements_by_class_name('ufss-date-select-toggle-container')
        has_window = False
        for date_container in date_containers:
            if len(date_container.find_elements_by_class_name('ufss-unavailable')) == 0:
                LOGGER.info('{} has delivery time window!'.format(self.name))
                self.send_sms('{} has delivery time window!'.format(self.name))
                time.sleep(1)
                # self.place_order(date_container)
                has_window = True
        time.sleep(5)
        if not has_window:
            LOGGER.info('{} No time window, refresh...'.format(self.name))
        self.is_whole_foods = True if self.is_whole_foods is False else False
        self.name = 'Whole Foods' if self.is_whole_foods else 'Amazon Fresh'
        self.go_to_home()
        self.access_delivery_page()

    def send_sms(self, text):
        account_sid = self.sid
        auth_token = self.auth_token
        client = Client(account_sid, auth_token)
        for num in self.phone_number:
            client.messages.create(
                body='{} - {}'.format(text, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                from_='+12062226523',
                to='+1{}'.format(num)
            )
    #
    # def place_order(self, date_container):
    #     date_container.click()
    #     time.sleep(1)
    #     time_container = self.driver.find_element_by_css_selector(
    #         '.ufss-slot-container .ufss-slot.ufss-available')
    #     time_container.click()
    #     time.sleep(1)
    #     continue_btn = self.driver.find_element_by_xpath(
    #         '//*[@id="shipoption-select"]/div/div/div/div/div[2]/div[3]/div/span/span/span/input')
    #     continue_btn.click()
    #     time.sleep(1)
    #     continue_btn = self.driver.find_element_by_xpath('//*[@id="continue-top"]')
    #     continue_btn.click()
    #     time.sleep(1)
    #     place_order_btn = self.driver.find_element_by_xpath('//*[@id="placeYourOrder"]/span/input')
    #     place_order_btn.click()
    #     LOGGER.info('order complete')
