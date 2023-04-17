"""
    TODO: under Construction
"""


"""
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
import time
"""
"""
    Mit Namespace auf den link
    "{% url 'mitglieder:mitglieder_loeschen' %}"
"""
"""
class TestMultiuser(StaticLiveServerTestCase):

    # befor every test funktion
    def setUp(self):
        self.browsers = list()
        for i in range(0, 1):

                #hier muss der richtige Webtreiber ausgewählt werden
                #1. Edge - Windows
                #2. Firefox - Windows
                #3. Firefox - Linux

            #browser = webdriver.Edge('tests\\edgedriver_win64\\msedgedriver.exe')
            browser = webdriver.Firefox(executable_path='tests\\firefoxdriver-win64\\geckodriver.exe')
            #browser = webdriver.Firefox(executable_path='tests\\firefoxdriver-linux64\\geckodriver')
            self.browsers.append(browser)
            pass
        pass

    # after every test funktion
    def tearDown(self):
        try:
            for browser in self.browsers:
                browser.close()
        except:
            print('Error while closing')
        pass

    # Tests
    def test_foo(self):
        for browser in self.browsers:
            try:
                browser.get(self.live_server_url)
            except:
                print('Error in opening login page')
            pass
        pass
"""
