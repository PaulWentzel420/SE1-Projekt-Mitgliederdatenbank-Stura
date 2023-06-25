from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

def test():
    driver = webdriver.Chrome()

    try:
        # Rufe unsere Testinstanz auf
        driver.get("http://84.146.24.124:21037/")
        sleep(2)

        username = 'testbenutzer'
        password = 'AequuxungishahT2oo'

        username_field = driver.find_element(By.NAME, 'username')
        password_field = driver.find_element(By.NAME, 'password')

        username_field.send_keys(username)
        password_field.send_keys(password)

        login_button = driver.find_element(By.ID, 'btn-login')
        login_button.click()

        sleep(2)

        driver.get("http://84.146.24.124:21037/mitglieder/erstellen")

        # Vorname
        vorname_input = driver.find_element(By.NAME, 'vorname')
        vorname_input.clear()
        vorname_input.send_keys("Max")

        # Nachname
        nachname_input = driver.find_element(By.NAME, 'nachname')
        nachname_input.clear()
        nachname_input.send_keys("Mustermann")

        # Org.einheit
        driver.find_element(By.XPATH, '//input[@class="select-dropdown dropdown-trigger"]').click()
        driver.find_element(By.XPATH, '//ul[@class="dropdown-content select-dropdown"]/li[2]').click()
        sleep(0.25)

        # Bereich
        driver.find_element(By.XPATH, '//div[@id="div_selectbereich1"]/div/div/input[@class="select-dropdown dropdown-trigger"]').click()
        driver.find_element(By.XPATH, '//div[@id="div_selectbereich1"]/div/div/ul[@class="dropdown-content select-dropdown"]/li[2]').click()
        sleep(0.25)

        # Funktion
        driver.find_element(By.XPATH, '//div[@id="div_selectamt1"]/div/div/input[@class="select-dropdown dropdown-trigger"]').click()
        driver.find_element(By.XPATH, '//div[@id="div_selectamt1"]/div/div/ul[@class="dropdown-content select-dropdown"]/li[2]').click()

        # Absenden des Formulars
        submit_button = driver.find_element(By.ID, 'save_button')
        submit_button.click()


        # Wir überprüfen ob das Ergebnis unsere Erwartungen erfüllt
        # ... ToDo

    finally:
        sleep(3000)
        driver.quit()

test()
