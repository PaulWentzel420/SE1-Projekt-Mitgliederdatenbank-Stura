from tests.MyTestCase import MyTestCase
from tests.MyFuncLogin import loginAsLukasAdmin
from tests.MyFuncMitglieder import addMitglied


class TestMitgliedAendern(MyTestCase):
    """
        Setup and Teardown functions are specified in
        MyTestCase
    """

    # Tests
    def test_1MitgliedAendern_AsSuperuser(self):
        """
            This is a "positive" Systemtest as Blackboxtest.
            Here we want to check if you can change information of a Member as Admin and if the
            Member is changed correctly in the table.

            Steps:

            * login as Admin
            * add a Member
            * change Member Data
            * check if everything is correct displayed
        """
        # Login as Admin
        loginAsLukasAdmin(self)
        addMitglied(self)

        """
            Auswählen eines Mitglieds (Stift)
        """
        self.browser.find_element_by_xpath("//tbody/tr/td/a").click()

        """
            Verändern von Feldern
        """
        self.browser.find_element_by_xpath(
            "//input[@id='vorname']").send_keys('_1')
        self.browser.find_element_by_xpath(
            "//input[@id='nachname']").send_keys('_1')
        self.browser.find_element_by_xpath("//a[@id='save_button']").click()

        self.assertEqual(
            self.browser.find_element_by_xpath("//tr[@class='mitglied']/td[contains(text(), 'Hans_1 Peter_1')]").text,
            "Hans_1 Peter_1",
            msg="Hans Peter wurde nicht geändert")
        pass
