from selenium.webdriver.support.ui import Select


def createReferat(self, organisationseinheit):
    """
        Erstellen eines Referates über die GUI, benötigt ist ein login als AdminPanel
        Ausgang ist, dass der User Angemeldet ist und sich in der Mitglieder sicht
        befindet.

        :param self:
        :type self:
        :param organisationseinheit: Name, wie das neue Organisationseinheit heißen soll
        :type organisationseinheit: string
        :return: No return Value
    """

    # Navigieren zum Admin Pannel
    self.browser.find_element_by_xpath("//a[@href='/admin']").click()

    # Navigieren zu Organisationseinheit Hinzufügen
    self.browser.find_element_by_xpath(
        "//a[@href='/admin/aemter/organisationseinheit/add/']").click()

    # fill inputs
    self.browser.find_element_by_xpath(
        "//input[@id='id_bezeichnung']").send_keys(organisationseinheit)

    # summit form
    self.browser.find_element_by_xpath("//input[@name='_save']").click()

    """
        Überprüfung ob Organisationseinheit hinzugefügt wurde
    """
    self.assertTrue(self.browser.find_element_by_xpath(
        "//a[contains(text(), '%s')]" % organisationseinheit))
    pass


def createUnterbereich(self, organisationseinheit, unterbereich):
    """
        Erstellen eines Unterbereiches über die GUI, benötigt ist ein login als AdminPanel
        Ausgang ist, dass der User Angemeldet ist und sich in der Mitglieder sicht
        befindet.

        :param self:
        :type self:
        :param organisationseinheit: Organisationseinheit, dem der Unterbereich zugeordnet werden soll
        :type organisationseinheit: string
        :param unterbereich: Name des Unterbereichs
        :type unterbereich: string
        :return: No return Value
    """

    # Navigieren zum Admin Pannel
    self.browser.find_element_by_xpath("//a[@href='/admin']").click()

    # Navigieren zu Organisationseinheit Hinzufügen
    self.browser.find_element_by_xpath(
        "//a[@href='/admin/aemter/unterbereich/add/']").click()

    # fill inputs
    self.browser.find_element_by_xpath(
        "//input[@id='id_bezeichnung']").send_keys(unterbereich)

    # fill selects
    select_referat = Select(
        self.browser.find_element_by_xpath("//select[@id='id_organisationseinheit']"))
    select_referat.select_by_visible_text(organisationseinheit)

    # summit form
    self.browser.find_element_by_xpath("//input[@name='_save']").click()

    """
        Überprüfung ob Unterbereichs hinzugefügt wurde
    """
    created_unterbereich = unterbereich + " (" + organisationseinheit + ")"
    self.assertTrue(self.browser.find_element_by_xpath(
        "//a[contains(text(), '%s')]" % created_unterbereich))
    pass


def createAmt(self, organisationseinheit, unterbereich, funktion):
    """
        Erstellen eines Amtes über die GUI, benötigt ist ein login als AdminPanel
        Ausgang ist, dass der User Angemeldet ist und sich in der Mitglieder sicht
        befindet.

        :param self:
        :type self:
        :param organisationseinheit: Organisationseinheit, dem das Funktion zugeordnet werden soll
        :type organisationseinheit: string
        :param unterbereich: Unterbereich des Referats
        :type unterbereich: string
        :param funktion: Angabe des Namens, der das neue Funktion erhalten soll
        :type funktion: string
        :return: No return Value
    """
    workload = "5"
    max_members = "60"
    unterbereich = unterbereich + " (" + organisationseinheit + ")"

    # Navigieren zum Admin Pannel
    self.browser.find_element_by_xpath("//a[@href='/admin']").click()

    # Navigieren zu Funktion Hinzufügen
    self.browser.find_element_by_xpath(
        "//a[@href='/admin/aemter/unterbereich/']").click()

    # schauen ob Unterbereich auf anderer seite liegt
    i = 1
    while (True):
        try:
            # print(f"Durchsucht wird Seite {i}")
            self.browser.find_element_by_xpath(
                "//a[contains(text(), '%s')]" % unterbereich).click()
        except:
            try:
                i = i + 1
                self.browser.find_element_by_xpath("//a[contains(text(), '%d')]" % i).click()
            except:
                # print("Etwas ist schief gegangen\n")
                pass
            continue
        break

    self.browser.find_element_by_xpath(
        "//a[contains(text(), 'Funktion hinzufügen')]").click()

    # fill inputs
    num = len(self.browser.find_elements_by_xpath("//tbody/tr"))
    num = num - 2
    self.browser.find_element_by_xpath(
        "//tbody/tr[%d]/td[@class='field-bezeichnung']/input" % num).send_keys(funktion)
    self.browser.find_element_by_xpath(
        "//tbody/tr[%d]/td[@class='field-workload']/input" % num).send_keys(workload)
    self.browser.find_element_by_xpath(
        "//tbody/tr[%d]/td[@class='field-max_members']/input" % num).send_keys(max_members)

    # summit form
    self.browser.find_element_by_xpath("//input[@name='_save']").click()

    """
        Überprüfung ob Funktion hinzugefügt wurde
        TODO: Testen ob das Amt jetzt wirklich existiert
    """
    self.assertTrue(self.browser.find_element_by_xpath(
        "//li[@class='success']/a[contains(text(), '%s')]" % unterbereich))
    pass
