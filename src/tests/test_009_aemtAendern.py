from selenium.webdriver.support.ui import Select
from tests.MyTestCase import MyTestCase
from tests.MyFuncLogin import loginAsLukasAdmin
from tests.MyFuncAemter import createAmt, createReferat, createUnterbereich


class TestAemtAendern(MyTestCase):
    """
        Setup and Teardown functions are specified in
        MyTestCase
    """

    def test_1OrganisationseinheitBezeichnungAendern(self):
        """
            This is a "positive" Systemtest as Blackboxtest.
            Here we want to check if you can change information of a "organisationseinheit" as Admin.
            We change the name of the "organisationseinheit" by appending a "_1".
        """
        # Login as Admin
        loginAsLukasAdmin(self)

        # Hinzufügen eines organisationseinheit
        organisationseinheit = "test_referat"
        createReferat(self, organisationseinheit)

        # ändern der Bezeichnung für test_referat
        suffix = "_1"
        self.browser.find_element_by_xpath(
            "//a[contains(text(), '%s')]" % organisationseinheit).click()
        self.browser.find_element_by_xpath(
            "//input[@id='id_bezeichnung']").send_keys(suffix)
        self.browser.find_element_by_xpath("//input[@name='_save']").click()

        # Überprüfen ob alles geklappt hat
        self.assertTrue(self.browser.find_element_by_xpath(
            "//li[@class='success']"))
        self.assertTrue(self.browser.find_element_by_xpath(
            "//a[contains(text(), '%s')]" % (organisationseinheit + suffix)))
        pass

    def test_1UnterbereichBezeichnungAendern(self):
        """
            This is a "positive" Systemtest as Blackboxtest.
            Here we want to check if you can change information of a "unterbereich" as Admin.
            We change the name of the "unterbereich" by appending a "_1".
        """
        # Login as Admin
        loginAsLukasAdmin(self)

        # Hinzufügen eines Unterbereichs
        organisationseinheit = "Referat Finanzen"
        unterbereich = "test_unterbereich"
        createUnterbereich(self, organisationseinheit, unterbereich)

        # ändern der Bezeichnung für test_unterbereich
        suffix = "_1"
        text = unterbereich + " (" + organisationseinheit + ")"
        self.browser.find_element_by_xpath(
            "//a[contains(text(), '%s')]" % text).click()
        self.browser.find_element_by_xpath(
            "//input[@id='id_bezeichnung']").send_keys(suffix)
        self.browser.find_element_by_xpath("//input[@name='_save']").click()

        # Überprüfen ob alles geklappt hat
        text = unterbereich + suffix + " (" + organisationseinheit + ")"
        self.assertTrue(self.browser.find_element_by_xpath(
            "//li[@class='success']"))
        self.assertTrue(self.browser.find_element_by_xpath(
            "//a[contains(text(), '%s')]" % text))
        pass

    def test_1UnterbereichReferatAendern(self):
        """
            This is a "positive" Systemtest as Blackboxtest.
            Here we want to check if you can change the "organisationseinheit" of a "unterbereich" as Admin.
        """
        # Login as Admin
        loginAsLukasAdmin(self)

        # Hinzufügen eines organisationseinheit
        referat2 = "test_referat"
        createReferat(self, referat2)
        self.browser.find_element_by_xpath("//a[@href='/']").click()

        # Hinzufügen eines Unterbereichs
        organisationseinheit = "Referat Finanzen"
        unterbereich = "test_unterbereich"
        createUnterbereich(self, organisationseinheit, unterbereich)

        # ändern des Referates, dem der Bereich zugeordnet wurde
        text = unterbereich + " (" + organisationseinheit + ")"
        self.browser.find_element_by_xpath(
            "//a[contains(text(), '%s')]" % text).click()
        select_referat = Select(
            self.browser.find_element_by_xpath("//select[@id='id_organisationseinheit']"))
        select_referat.select_by_visible_text(referat2)
        self.browser.find_element_by_xpath("//input[@name='_save']").click()

        # Überprüfen ob alles geklappt hat
        text = unterbereich + " (" + referat2 + ")"
        self.assertTrue(self.browser.find_element_by_xpath(
            "//li[@class='success']"))
        self.assertTrue(self.browser.find_element_by_xpath(
            "//a[contains(text(), '%s')]" % text))
        pass

    def test_1AmtBezeichnungAendern(self):
        """
            This is a "positive" Systemtest as Blackboxtest.
            Here we want to check if you can change information of a funktion as Admin.
            We change the name of the funktion by appending a "_1".
        """
        # Login as Admin
        loginAsLukasAdmin(self)

        # Hinzufügen eines Amtes
        funktion = "test_amt"
        organisationseinheit = "Referat Finanzen"
        unterbereich = "Bereich Buchhaltung"
        createAmt(self, organisationseinheit, unterbereich, funktion)

        # ändern des Referates, dem der Bereich zugeordnet wurde
        suffix = "_1"
        text = unterbereich + " (" + organisationseinheit + ")"
        self.browser.find_element_by_xpath(
            "//a[contains(text(), '%s')]" % text).click()
        self.browser.find_element_by_xpath(
            "//tr/td[@class='original']/p[contains(text(), '%s')]/../../td[@class='field-bezeichnung']/input"%(funktion + " " + text)).send_keys(suffix)
        self.browser.find_element_by_xpath("//input[@name='_save']").click()

        """
            Überprüfung ob Funktion hinzugefügt wurde
            TODO: Testen ob das Amt jetzt wirklich existiert
        """
        self.assertTrue(self.browser.find_element_by_xpath(
            "//li[@class='success']/a[contains(text(), '%s')]" % text))
        pass

    def test_1AmtWorkloadAendern(self):
        """
            This is a "positive" Systemtest as Blackboxtest.
            Here we want to check if you can change the workload of a funktion as Admin.
        """
        # Login as Admin
        loginAsLukasAdmin(self)

        # Hinzufügen eines Amtes
        funktion = "test_amt"
        organisationseinheit = "Referat Finanzen"
        unterbereich = "Bereich Buchhaltung"
        createAmt(self, organisationseinheit, unterbereich, funktion)

        # ändern des Referates, dem der Bereich zugeordnet wurde
        workload = "5"
        text = unterbereich + " (" + organisationseinheit + ")"
        self.browser.find_element_by_xpath(
            "//a[contains(text(), '%s')]" % text).click()
        self.browser.find_element_by_xpath(
            "//tr/td[@class='original']/p[contains(text(), '%s')]/../../td[@class='field-workload']/input"%(funktion + " " + text)).send_keys(workload)
        self.browser.find_element_by_xpath("//input[@name='_save']").click()

        # Überprüfen ob alles geklappt hat
        """
            Überprüfung ob Workload geändert wurde
            TODO: Testen ob Workload tatsächlich geändert wurde
        """
        self.assertTrue(self.browser.find_element_by_xpath(
            "//li[@class='success']/a[contains(text(), '%s')]" % text))
        pass

    def test_1AmtReferatAendern(self):
        """
            This is a "positive" Systemtest as Blackboxtest.
            Here we want to check if you can change the "organisationseinheit" of a funktion as Admin.
        """
        # Login as Admin
        loginAsLukasAdmin(self)

        # Hinzufügen eines organisationseinheit
        organisationseinheit = "test_referat"
        createReferat(self, organisationseinheit)
        self.browser.find_element_by_xpath("//a[@href='/']").click()

        # Hinzufügen eines Unterbereichs
        unterbereich = "test_unterbereich"
        createUnterbereich(self, organisationseinheit, unterbereich)
        self.browser.find_element_by_xpath("//a[@href='/']").click()

        # Hinzufügen eines Amtes
        funktion = "test_amt"
        organisationseinheit2 = "Referat Finanzen"
        createAmt(self, organisationseinheit, unterbereich, funktion)

        # ändern des Referates, dem der Bereich zugeordnet wurde
        workload = "5"
        text = unterbereich + " (" + organisationseinheit + ")"
        self.browser.find_element_by_xpath(
            "//a[contains(text(), '%s')]" % text).click()
        select_referat = Select(
            self.browser.find_element_by_xpath("//select[@id='id_organisationseinheit']"))
        select_referat.select_by_visible_text(organisationseinheit2)
        self.browser.find_element_by_xpath("//input[@name='_save']").click()

        # Überprüfen ob alles geklappt hat
        """
            Überprüfung ob Funktion verschoben wurde
            TODO: Testen ob das Amt jetzt wirklich verschoben ist
        """
        self.assertTrue(self.browser.find_element_by_xpath(
            "//li[@class='success']/a[contains(text(), '%s')]" % (unterbereich + " (" + organisationseinheit2 + ")")))
        pass
