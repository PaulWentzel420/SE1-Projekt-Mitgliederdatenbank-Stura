from tests.MyTestCase import MyTestCase
from tests.MyFuncLogin import loginAsLukasAdmin
from tests.MyFuncMitglieder import addMitglied


class TestMitgliedEntfernen(MyTestCase):
    """
        Setup and Teardown functions are specified in
        MyTestCase
    """

    # Tests
    def test_1MitgliedEntfernen_AsSuperuser(self):
        """
            This is a "positive" Systemtest as Blackboxtest.
            Here we want to check if you can delete a new Member as Admin and if the
            Member is deleted correctly in the table.

            Steps:

            * login as Admin
            * add a Member
            * delete Member
        """

        # Login as Admin
        loginAsLukasAdmin(self)
        addMitglied(self)

        """
            Löschen eines Mitglieds
        """
        self.browser.find_element_by_xpath(
            "//form[@method='post']/label/span").click()
        self.browser.find_element_by_xpath("//a[@id='delbtnl']").click()
        self.browser.find_element_by_xpath(
            "//a[@id='delmitgliederconfirm']").click()

        """
            Überprüfung ob Mitglied gelöscht
        """
        text = self.browser.find_element_by_xpath("//div[@id='notification']")
        self.assertTrue(text)
        pass
