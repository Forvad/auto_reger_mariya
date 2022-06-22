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
from requests import get
from os import path, getcwd, system
from time import sleep
from loguru import logger
from multiprocessing.dummy import Pool


class AppDynamicsJob(unittest.TestCase):
    def setUp(self):
        # AppDynamics will automatically override this web driver
        # as documented in https://docs.appdynamics.com/display/PRO44/Write+Your+First+Script
        EXTENSION_PATH = 'metamask.crx'
        opt = webdriver.ChromeOptions()
        opt.add_extension(EXTENSION_PATH)
        opt.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        #opt.headless = True
        self.driver = webdriver.Chrome(chrome_options=opt)
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def get_username(self, length):
        usernames = []

        while len(usernames) < length:
            try:
                r = get('https://story-shack-cdn-v2.glitch.me/generators/username-generator')
                usernames.append(loads(r.text)['data']['name'])  # + "".join(
                    #[choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ013456789") for _ in range(5)]))

            except:
                pass

        return (usernames)

    def verf_mail(self, login):
        while True:
            r = get(f'https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain=1secmail.org')
            if len(loads(r.text)) >= 1:
                text = loads(r.text)[0]["id"]
                g = get(
                    f'https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain=1secmail.org&id={text}')
                text = loads(g.text)['textBody'].split(':')
                text = 'https:' + text[2]
                return text
            else:
                sleep(2)


    def test_app_dynamics_job(self):
        mnemonic = Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_12)
        username = self.get_username(4)
        account_password = \
            "".join([choice("abcdefghijklmnopqrstuvwxyz013456789") for _ in range(15)]) \
            + "".join([choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(15)]) + '@'
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

        driver.get("https://myria.com/sigil/?code=6cd9b69a-5782-48c7-861e-708db71e6b9d")
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
        driver.find_element_by_name("firstName").send_keys(username[0])
        driver.find_element_by_name("lastName").click()
        driver.find_element_by_name("lastName").send_keys(username[1])
        driver.find_element_by_name("username").click()
        driver.find_element_by_name("username").send_keys(f'{username[2]}@1')
        driver.find_element_by_name("email").click()
        driver.find_element_by_name("email").send_keys(f'{username[3]}@1secmail.org')
        driver.find_element_by_name("password").click()
        driver.find_element_by_name("password").send_keys(account_password)
        driver.find_element_by_name("confirmPassword").clear()
        driver.find_element_by_name("confirmPassword").send_keys(account_password)
        driver.execute_script("window.scrollTo(0,300);")
        read_mores = driver.find_elements_by_xpath('//*[@id="radix-1"]/div/div[2]/form/button')
        for read_more in read_mores:
            driver.execute_script("arguments[0].scrollIntoView();", read_more)
        print(username[3])
        sleep(1)
        driver.find_element_by_xpath('//*[@id="radix-1"]/div/div[2]/form/button').click()
        with open('email.txt', 'a', encoding='utf-8') as file:
            login = username[3]
            file.write(f'{login}\n')
            logger.success('The work has been successfully completed')
        driver.get(self.verf_mail(username[3]))
        sleep(2)
        with open('email.txt', 'a', encoding='utf-8') as file:
            login = username[3]
            file.write(f'{login}  ++\n')
            logger.success('The work has been successfully completed')



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