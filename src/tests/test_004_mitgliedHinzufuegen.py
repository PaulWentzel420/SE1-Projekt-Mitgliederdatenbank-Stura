import time
from selenium import webdriver
from django.urls import reverse

from tests.MyTestCase import MyTestCase
from tests.MyFuncLogin import loginAsLukasAdmin, loginAsLukasUser
from tests.MyFuncMitglieder import *
from tests.MyFuncAemter import createAmt


class TestMitgliedHinzufuegen(MyTestCase):
    """
        Setup and Teardown functions are specified in
        MyTestCase
    """

    # Tests
    def test_1MitgliedHinzufügen_AsSuperuser(self):
        """
            This is a "positive" Systemtest as Blackboxtest.
            Here we want to check if you can add a new Member as Admin and if the
            Member is displayed correctly in the table.

            Steps:

            * login as Admin
            * add a Member
        """

        # Login as Admin
        loginAsLukasAdmin(self)
        addMitglied(self)
        pass

    def test_50MitgliederHinzufügen_AsSuperuser_lookAsUser(self):
        """
            This is a complex "positive" Systemtest as Blackboxtest.
            Here we want to check if you can add a multiple new Members (50) as Admin and if the
            Member is displayed correctly in the table.
            We also want to check if the Pagination is working correctly.

            Steps:

            * login as Admin
            * add a Member (as loop)
            * check Pagination
        """

        # Login as Admin
        loginAsLukasAdmin(self)

        # Hinzufügen eines Amtes
        funktion = "test_amt"
        organisationseinheit = "Referat Finanzen"
        unterbereich = "Bereich Buchhaltung"
        createAmt(self, organisationseinheit, unterbereich, funktion)
        self.browser.find_element_by_xpath("//a[@href='/']").click()

        for value in range(50):
            # print(f"Mitglied {value} wird hinzugefügt")
            try:
                addMitgliedWithParameters(self,
                    f"Max_{value}", "Mustermann", "Musti")
                self.browser.find_element_by_xpath("//ul[@class='pagination']/li/a[contains(text(), '1')]").click()
            except:
                self.assertTrue(False, msg=f"Mitglied {value} wurde übersprungen")
                pass
            pass

        # Test Mitglieder Pagination Seiten
        self.assertTrue(self.browser.find_element_by_xpath("//ul[@class='pagination']/li/a[contains(text(), '1')]"))
        self.assertTrue(self.browser.find_element_by_xpath("//ul[@class='pagination']/li/a[contains(text(), '2')]"))
        self.assertTrue(self.browser.find_element_by_xpath("//ul[@class='pagination']/li/a[contains(text(), '3')]"))
        self.assertTrue(self.browser.find_element_by_xpath("//ul[@class='pagination']/li/a[contains(text(), '4')]"))

        """
            Logout and login as User
        """
        self.browser.find_element_by_xpath("//li/a[@href='/logout']").click()
        loginAsLukasUser(self)

        # Test Mitglieder Pagination Seiten
        self.assertTrue(self.browser.find_element_by_xpath("//ul[@class='pagination']/li/a[contains(text(), '1')]"))
        self.assertTrue(self.browser.find_element_by_xpath("//ul[@class='pagination']/li/a[contains(text(), '2')]"))
        self.assertTrue(self.browser.find_element_by_xpath("//ul[@class='pagination']/li/a[contains(text(), '3')]"))
        self.assertTrue(self.browser.find_element_by_xpath("//ul[@class='pagination']/li/a[contains(text(), '4')]"))
        pass
