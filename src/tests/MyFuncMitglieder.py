from selenium import webdriver
from django.urls import reverse


def addMitglied(self):
    """
        Add a member with default parameters over the "mitglieder/erstellen" view.
        You need to be on the "mitglieder/" site to call this function.

        :param self:
        :type self:
        :return: No return Value
    """
    # Suchen des Hinzufügen Buttons
    try:
        btnAddMitglied = self.browser.find_element_by_xpath(
            "//a[@href='/mitglieder/erstellen']")
        #btnAddMitglied = self.browser.find_element_by_id('btn-mitadd')
    except BaseException:
        print("Es wurden nicht alle Objekte auf der Seite gefunden")

    # Klicken des Buttons
    btnAddMitglied.click()

    # Suchen aller relevanten Objekte zum hinzufügen eines Mitglieds
    try:
        # Entrys
        entVorname = self.browser.find_element_by_name('vorname')
        entNachname = self.browser.find_element_by_name('nachname')
        entSpitzname = self.browser.find_element_by_name('spitzname')

        entStrasse = self.browser.find_element_by_name('strasse')
        entHausnr = self.browser.find_element_by_name('hausnr')
        entPlz = self.browser.find_element_by_name('plz')
        entOrt = self.browser.find_element_by_name('ort')
        entTelefon_mobil = self.browser.find_element_by_name('telefon_mobil')

        # Buttons
        btnAddEmail = self.browser.find_element_by_id('addEmailBtn')
        btnSave = self.browser.find_element_by_id('save_button')
    except BaseException:
        print("Es wurden nicht alle Objekte auf der Seite gefunden")

    # Einfügen der Form
    entVorname.send_keys('Hans')
    entNachname.send_keys('Peter')
    entSpitzname.send_keys('Hansi')

    # Organisationseinheit auswählen
    self.browser.find_element_by_xpath(
        "//input[@class='select-dropdown dropdown-trigger']").click()
    self.browser.find_element_by_xpath(
        "//ul[@class='dropdown-content select-dropdown']/li[19]").click()

    # Bereich auswählen
    self.browser.find_element_by_xpath(
        "//div[@id='div_selectbereich1']/div/div/input[@class='select-dropdown dropdown-trigger']").click()
    self.browser.find_element_by_xpath(
        "//div[@id='div_selectbereich1']/div/div/ul[@class='dropdown-content select-dropdown']/li[2]").click()

    # Funktion auswählen
    self.browser.find_element_by_xpath(
        "//div[@id='div_selectamt1']/div/div/input[@class='select-dropdown dropdown-trigger']").click()
    self.browser.find_element_by_xpath(
        "//div[@id='div_selectamt1']/div/div/ul[@class='dropdown-content select-dropdown']/li[2]").click()

    btnAddEmail.click()
    # Finden der Email Felder
    try:
        entEmail1 = self.browser.find_element_by_name('email1')
        entEmail2 = self.browser.find_element_by_name('email2')
    except BaseException:
        print("Es wurden nicht alle Objekte auf der Seite gefunden")

    # Eingabe der Emails
    entEmail1.send_keys('sxxxxx@htw-dresden.de')
    entEmail2.send_keys('Hans.Peter@web.de')

    # Einfügen der restlichen Daten der Form
    entStrasse.send_keys('Straße der Freiheit')
    entHausnr.send_keys('24')
    entPlz.send_keys('01561')
    entOrt.send_keys('Ebersbach')
    entTelefon_mobil.send_keys('0362594833')

    # Speichern der Daten
    btnSave.click()

    # überprüfen ob alles geklapt hat
    self.assertEqual(self.browser.current_url,
                     self.live_server_url + reverse('mitglieder:homepage'),
                     msg="Weiterleitung nicht erfolgt")
    self.assertEqual(
        self.browser.find_element_by_xpath("//tr[@class='mitglied']/td[contains(text(), 'Hans Peter')]").text,
        "Hans Peter",
        msg="Hans Peter wurde nicht angelegt")
    pass

def addMitgliedWithParameters(self,
                                vorname,
                                nachname,
                                spitzname,
                                ):
    """
        Add a member with default parameters over the "mitglieder/erstellen" view.
        You can change firstname, lastname and username.
        You need to be on the "mitglieder/" site to call this function.

        :param self:
        :type self:
        :param vorname: Firstname of the Member, that you want to create.
        :type vorname: string
        :param nachname: Lastname of the Member, that you want to create.
        :type nachname: string
        :param spitzname: Username of the Member, that you want to create.
        :type spitzname: string
        :return: No return Value
    """
    # Suchen des Hinzufügen Buttons
    try:
        self.browser.find_element_by_xpath("//a[@href='/mitglieder/erstellen']").click()
    except:
        try:
            self.browser.refresh()
            self.browser.find_element_by_xpath("//a[@href='/mitglieder/erstellen']").click()
        except:
            print("Es wurden nicht alle Objekte auf der Seite gefunden")

    # Suchen aller relevanten Objekte zum hinzufügen eines Mitglieds
    try:
        # Entrys
        # Einfügen der Form
        self.browser.find_element_by_name('vorname').send_keys(vorname)
        self.browser.find_element_by_name('nachname').send_keys(nachname)
        self.browser.find_element_by_name('spitzname').send_keys(spitzname)

        entStrasse = self.browser.find_element_by_name('strasse')
        entHausnr = self.browser.find_element_by_name('hausnr')
        entPlz = self.browser.find_element_by_name('plz')
        entOrt = self.browser.find_element_by_name('ort')
        entTelefon_mobil = self.browser.find_element_by_name('telefon_mobil')

        # Buttons
        btnAddEmail = self.browser.find_element_by_id('addEmailBtn')
        btnSave = self.browser.find_element_by_id('save_button')
    except:
        print("Es wurden nicht alle Objekte auf der Seite gefunden")

    # Organisationseinheit auswählen
    self.browser.find_element_by_xpath(
        "//input[@class='select-dropdown dropdown-trigger']").click()
    self.browser.find_element_by_xpath(
        "//ul[@class='dropdown-content select-dropdown']/li[19]").click()

    # Bereich auswählen
    self.browser.find_element_by_xpath(
        "//div[@id='div_selectbereich1']/div/div/input[@class='select-dropdown dropdown-trigger']").click()
    self.browser.find_element_by_xpath(
        "//div[@id='div_selectbereich1']/div/div/ul[@class='dropdown-content select-dropdown']/li[3]").click()

    # Funktion auswählen
    self.browser.find_element_by_xpath(
        "//div[@id='div_selectamt1']/div/div/input[@class='select-dropdown dropdown-trigger']").click()
    self.browser.find_element_by_xpath(
        "//div[@id='div_selectamt1']/div/div/ul[@class='dropdown-content select-dropdown']/li[3]").click()

    btnAddEmail.click()
    # Finden der Email Felder
    try:
        entEmail1 = self.browser.find_element_by_name('email1')
        entEmail2 = self.browser.find_element_by_name('email2')
    except BaseException:
        print("Es wurden nicht alle Objekte auf der Seite gefunden")

    # Eingabe der Emails
    entEmail1.send_keys('sxxxxx@htw-dresden.de')
    entEmail2.send_keys(vorname + "." + nachname + "@web.de")

    # Einfügen der restlichen Daten der Form
    entStrasse.send_keys('Straße der Freiheit')
    entHausnr.send_keys('24')
    entPlz.send_keys('01561')
    entOrt.send_keys('Ebersbach')
    entTelefon_mobil.send_keys('0362594833')

    # Speichern der Daten
    btnSave.click()

    # überprüfen ob alles geklapt hat
    self.assertEqual(self.browser.current_url,
                     self.live_server_url + reverse('mitglieder:homepage'),
                     msg="Weiterleitung nicht erfolgt")

    i = 1
    while (True):
        try:
            # print(f"Durchsucht wird Seite {i}")
            webelement = self.browser.find_element_by_xpath("//tr[@class='mitglied']/td[contains(text(), '%s')]"%(vorname + " " + nachname))
        except:
            try:
                i = i + 1
                self.browser.find_element_by_xpath("//ul[@class='pagination']/li/a[contains(text(), '%d')]"%i).click()
            except:
                # print("Etwas ist schief gegangen\n")
                pass
            continue
        break

    self.assertEqual(
        webelement.text,
        vorname + " " + nachname,
        msg="%s wurde nicht angelegt"%(vorname + " " + nachname))
    pass
