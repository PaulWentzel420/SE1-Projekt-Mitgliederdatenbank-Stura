from tests.MyTestCase import MyTestCase
from tests.MyFuncLogin import loginAsLukasAdmin
from tests.MyFuncAemter import createAmt, createReferat, createUnterbereich


class TestAemtEntfernen(MyTestCase):
    """
        Setup and Teardown functions are specified in
        MyTestCase
    """

    def test_1ReferatEntfernen_AsSuperuser(self):
        """
            This is a "positive" Systemtest as Blackboxtest.
            Here we want to check if you can delete a "Organisationseinheit" as Admin.

            Steps:

            * login as Admin
            * add a "Organisationseinheit"
            * delete the "Organisationseinheit"
        """

        # Login as Admin
        loginAsLukasAdmin(self)

        # Hinzufügen eines organisationseinheit
        organisationseinheit = "test_referat"
        createReferat(self, organisationseinheit)

        # Entfernen eines organisationseinheit
        self.browser.find_element_by_xpath(
            "//a[contains(text(), '%s')]" % organisationseinheit).click()
        self.browser.find_element_by_xpath("//a[@class='deletelink']").click()
        self.browser.find_element_by_xpath(
            "//div/input[@type='submit']").click()

        # Überprüfen ob alles geklappt hat
        self.assertTrue(self.browser.find_element_by_xpath(
            "//li[@class='success']"))
        tmpbool = True
        try:
            self.browser.find_element_by_xpath(
                "//a[contains(text(), '%s')]" % organisationseinheit)
        except BaseException:
            tmpbool = False
        self.assertFalse(tmpbool)
        pass

    def test_1UnterbereichEntfernen_AsSuperuser(self):
        """
            This is a "positive" Systemtest as Blackboxtest.
            Here we want to check if you can delete a "unterbereich" as Admin.

            Steps:

            * login as Admin
            * add a "unterbereich"
            * delete the "unterbereich"
        """

        # Login as Admin
        loginAsLukasAdmin(self)

        # Hinzufügen eines Unterbereichs
        organisationseinheit = "Referat Finanzen"
        unterbereich = "test_unterbereich"
        createUnterbereich(self, organisationseinheit, unterbereich)

        # Entfernen eines unterbereiches
        self.browser.find_element_by_xpath(
            "//a[contains(text(), '%s')]" % unterbereich).click()
        self.browser.find_element_by_xpath("//a[@class='deletelink']").click()
        self.browser.find_element_by_xpath(
            "//div/input[@type='submit']").click()

        # Überprüfen ob alles geklappt hat
        self.assertTrue(self.browser.find_element_by_xpath(
            "//li[@class='success']"))
        tmpbool = True
        try:
            self.browser.find_element_by_xpath(
                "//a[contains(text(), '%s')]" % unterbereich)
        except BaseException:
            tmpbool = False
        self.assertFalse(tmpbool)
        pass

    def test_1AemtEntfernen_AsSuperuser(self):
        """
            This is a "positive" Systemtest as Blackboxtest.
            Here we want to check if you can delete a funktion as Admin.

            Steps:

            * login as Admin
            * add a funktion
            * delete the funktion
        """

        # Login as Admin
        loginAsLukasAdmin(self)

        # Hinzufügen eines Amtes
        funktion = "test_amt"
        organisationseinheit = "Referat Finanzen"
        unterbereich = "Bereich Buchhaltung"
        createAmt(self, organisationseinheit, unterbereich, funktion)

        # Entfernen eines Amts
        unterbereich = unterbereich + " (" + organisationseinheit + ")"
        self.browser.find_element_by_xpath(
            "//a[contains(text(), '%s')]" % unterbereich).click()
        self.browser.find_element_by_xpath(
            "//tr/td[@class='original']/p[contains(text(), '%s')]/../../td[@class='delete']/input"%(funktion + " " + unterbereich)).click()
        self.browser.find_element_by_xpath("//input[@name='_save']").click()

        """
            Überprüfung ob Funktion entfernt wurde
            TODO: Testen ob das Amt jetzt wirklich nicht mehr da ist
        """
        self.assertTrue(self.browser.find_element_by_xpath(
            "//li[@class='success']/a[contains(text(), '%s')]" % unterbereich))
        pass
