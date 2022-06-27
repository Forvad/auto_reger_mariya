# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
from bip_utils import Bip39WordsNum, Bip39MnemonicGenerator
from random import choice
from json import loads
from requests import get, Session
from os import path, getcwd, system
from time import sleep
from loguru import logger
from pyuseragents import random as random_useragent
import cloudscraper


class AppDynamicsJob(unittest.TestCase):
    def setUp(self):
        EXTENSION_PATH = 'metamask.crx'
        opt = webdriver.ChromeOptions()
        opt.add_extension(EXTENSION_PATH)
        opt.add_argument('--disable-infobars')
        opt.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        opt.add_argument("--mute-audio")
        self.driver = webdriver.Chrome(chrome_options=opt)
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def creat_mail(self):
        session = Session()
        session.headers.update({'user-agent': random_useragent(), 'Accept': 'application/json, text/plain, */*',
                                'Referer': 'https://temprmail.com/'})
        r = session.post('https://api.temprmail.com/v1/emails')
        email = loads(r.text)['email']
        checkmailsurl = loads(r.text)['emails_json_url']
        return email, checkmailsurl

    def check_mail(self, check):
        session = Session()
        session.headers.update({'user-agent': random_useragent(), 'Accept': 'application/json, text/plain, */*',
                                'Referer': 'https://temprmail.com/'})
        scraper = cloudscraper.create_scraper()
        scraper.headers.update({'Content-Type': 'application/json', 'cf-visitor': 'https',
                                'User-Agent': 'Legion/5.2 CFNetwork/1209 Darwin/20.2.0', 'Connection': 'keep-alive',
                                'Accept': 'application/json, text/plain, */*', 'Accept-Language': 'ru',
                                'x-forwarded-proto': 'https', 'Accept-Encoding': 'gzip, deflate, br'})
        for i in range(15):
            r = scraper.get(check)
            if 'Email Verification' in r.text:
                msgid = loads(r.text)[0]['hash_id']
                break
            else:
                if i == 14:
                    return 'https://myria.com'
                else:
                    sleep(3)
        r = session.get(f'https://tempremail-assets.s3.us-east-1.amazonaws.com/emails/{msgid}.json')
        text = loads(r.text)['message'].split('<a href="')[1]
        num = text.find('"')
        url = text[0:num]
        return url

    def test_app_dynamics_job(self):
        referal = 'https://myria.com/sigil/?code=b41b6bb8-87cb-4ff6-9ed7-97a7b16245cb'
        mnemonic = Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_12)

        username1 = 'F' + "".join([choice("abcdefghijklmnopqrstuvwxyz") for _ in range(7)])
        username2 = 'E' + "".join([choice("abcdefghijklmnopqrstuvwxyz") for _ in range(7)])
        username3 = 'C' + "".join([choice("abcdefghijklmnopqrstuvwxyz") for _ in range(7)])

        mail, chekmail = self.creat_mail()
        account_password = \
            "".join([choice("abcdefghijklmnopqrstuvwxyz") for _ in range(5)]) \
            + "".join([choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(5)]) + '@' \
            + "".join([choice('0123456789') for _ in range(3)])
        driver = self.driver

        driver.switch_to.window(driver.window_handles[1])

        # Register Metamask

        driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#initialize/welcome')
        driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div/div/button').click()
        driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div/div[2]/div/div[2]/div[1]/button').click()
        driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div/div/div[5]/div[1]/footer/button[1]').click()
        for i in range(1, 13):
            driver.find_element_by_xpath(f'/html/body/div[1]/div/div[2]/div/div/div[2]/form/div[1]/div[3]/div[{i}]/div[1]/div/input').send_keys(str(mnemonic).split(' ')[i - 1])
        driver.find_element_by_xpath('// *[ @ id = "password"]').click()
        driver.find_element_by_xpath('// *[ @ id = "password"]').send_keys('12345678')
        driver.find_element_by_xpath('//*[@id="confirm-password"]').click()
        driver.find_element_by_xpath('//*[@id="confirm-password"]').send_keys('12345678')
        driver.find_element_by_xpath('// *[ @ id = "create-new-vault__terms-checkbox"]').click()
        driver.find_element_by_xpath('// *[ @ id = "app-content"]/div/div[2]/div/div/div[2]/form/button').click()
        driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div/button').click()
        sleep(1)

        # Register myria.com

        driver.get(referal)
        driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div/div/div[2]/div[2]/div/div[1]/div/div/button').click()
        driver.execute_script("window.open('about:blank', 'secondtab');")
        driver.switch_to.window("secondtab")
        driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#initialize/welcome')
        sleep(1)
        driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div[3]/div[2]/button[2]').click()
        driver.find_element_by_xpath(
            '//*[@id="app-content"]/div/div[2]/div/div[2]/div[2]/div[2]/footer/button[2]').click()
        driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div[3]/button[2]').click()
        driver.close()
        driver.switch_to.window(driver.window_handles[1])
        sleep(1)
        driver.find_element_by_xpath('// *[ @ id = "__next"] / div[2] / div / div / div[2] / div[2] / div /'
                                     ' div[1] / div / div / div / div[1] / div[2] / div / div[4] / div[1] / span / img').click()
        sleep(1)
        driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div/div/div[2]/div[2]/div/div[1]/div/div/div/div[1]/div[2]/div/div[5]/button').click()
        driver.find_element_by_xpath('// *[ @ id = "radix-30"] / div / div / div / div / div[1] / button').click()
        driver.find_element_by_xpath('// *[ @ id = "__next"] / div[2] / div / div / div[2] / div[2] / div / div / div / div / div[2] / div[2] / div / \
                                 div[2] / div / div[1] / div[2] / div / div[2] / a / div / div')
        driver.find_element_by_xpath(
            "//div[@id='__next']/div[2]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div/div[2]/"
            "div/div/div[2]/div/div[2]/a/div/div").click()
        driver.find_element_by_name("firstName").click()
        driver.find_element_by_name("firstName").send_keys(username1)
        driver.find_element_by_name("lastName").click()
        driver.find_element_by_name("lastName").send_keys(username2)
        driver.find_element_by_name("username").click()
        driver.find_element_by_name("username").send_keys(username3)
        driver.find_element_by_name("email").click()
        driver.find_element_by_name("email").send_keys(mail)
        driver.find_element_by_name("password").click()
        driver.find_element_by_name("password").send_keys(account_password)
        driver.find_element_by_name("confirmPassword").clear()
        driver.find_element_by_name("confirmPassword").send_keys(account_password)
        driver.execute_script("window.scrollTo(0,300);")
        read_mores = driver.find_elements_by_xpath('//*[@id="radix-1"]/div/div[2]/form/button')
        for read_more in read_mores:
            driver.execute_script("arguments[0].scrollIntoView();", read_more)
        sleep(1)
        driver.find_element_by_xpath('//*[@id="radix-1"]/div/div[2]/form/button').click()
        driver.get(self.check_mail(chekmail))
        if len(self.check_mail(chekmail)) > 17:
            with open('s4et.txt', 'r') as a:
                f_contents = a.read()
            s = int(f_contents) + 20
            s = str(s)
            with open('s4et.txt', 'w') as f:
                f.write(s)
        sleep(2)




    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
