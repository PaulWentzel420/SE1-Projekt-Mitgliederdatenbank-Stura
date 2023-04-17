from django.urls import reverse


def loginAsLukasAdmin(self):
    """
        Opens a Browser instance and login as admin with the account testlukasadmin.

        :param self:
        :type self:
        :return: No return Value
    """

    # Öffnen eines Browsers
    try:
        self.browser.get(self.live_server_url)
    except BaseException:
        print('Error in opening login page')

    # Suche aller Objekte der Seite
    try:
        entUsername = self.browser.find_element_by_id('id_username')
        entPassword = self.browser.find_element_by_id('id_password')
        btnLogin = self.browser.find_element_by_id('btn-login')
    except BaseException:
        print("Es wurden nicht alle Objekte auf der Seite gefunden")

    # Eingabe der Login-Daten
    entUsername.send_keys('testlukasadmin')
    entPassword.send_keys('0123456789test')
    btnLogin.click()

    # Check Login Success
    self.assertEqual(
        self.browser.current_url,
        self.live_server_url +
        reverse('mitglieder:homepage'),
        msg="Konnte nicht angemeldet werden bzw. Weiterleitung nicht erfolgt")
    pass


def loginAsLukasUser(self):
    """
        Opens a Browser instance and login as user with the account testlukas.

        :param self:
        :type self:
        :return: No return Value
    """

    # Öffnen eines Browsers
    try:
        self.browser.get(self.live_server_url)
    except BaseException:
        print('Error in opening login page')

    # Suche aller Objekte der Seite
    try:
        entUsername = self.browser.find_element_by_id('id_username')
        entPassword = self.browser.find_element_by_id('id_password')
        btnLogin = self.browser.find_element_by_id('btn-login')
    except BaseException:
        print("Es wurden nicht alle Objekte auf der Seite gefunden")

    # Eingabe der Login-Daten
    entUsername.send_keys('testlukas')
    entPassword.send_keys('0123456789test')
    btnLogin.click()

    # Check Login Success
    self.assertEqual(
        self.browser.current_url,
        self.live_server_url +
        reverse('mitglieder:homepage'),
        msg="Konnte nicht angemeldet werden bzw. Weiterleitung nicht erfolgt")
    pass
