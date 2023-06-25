from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

class Daten:
    def __init__(self, position, rechte, org_value=None, bereich_value=None, funktion_value=None, vorname=None, nachname=None, voller_name=None):
        self.position = position
        self.rechte = []

        self.org_value = org_value
        self.bereich_value = bereich_value
        self.funktion_value = funktion_value
        self.vorname = vorname
        self.nachname = nachname

        self.voller_name = voller_name if voller_name is not None else f'{vorname} {nachname}'
        
        if rechte:
            self.rechte.extend(rechte)

        def __str__(self):
            return f'{self.voller_name}\n{self.position}\n{self.rechte}'

def einloggen(driver):
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

def test(daten, driver):
    driver.get("http://84.146.24.124:21037/mitglieder/erstellen")

    # Vorname
    vorname_input = driver.find_element(By.NAME, 'vorname')
    vorname_input.clear()
    vorname_input.send_keys(daten.vorname)

    # Nachname
    nachname_input = driver.find_element(By.NAME, 'nachname')
    nachname_input.clear()
    nachname_input.send_keys(daten.nachname)

    # Org.einheit
    driver.find_element(By.XPATH, '//input[@class="select-dropdown dropdown-trigger"]').click()
    driver.find_element(By.XPATH, f'//ul[@class="dropdown-content select-dropdown"]/li[{daten.org_value}]').click()
    sleep(0.25)

    # Bereich
    driver.find_element(By.XPATH, '//div[@id="div_selectbereich1"]/div/div/input[@class="select-dropdown dropdown-trigger"]').click()
    driver.find_element(By.XPATH, f'//div[@id="div_selectbereich1"]/div/div/ul[@class="dropdown-content select-dropdown"]/li[{daten.bereich_value}]').click()
        
    sleep(0.25)

    # Funktion
    driver.find_element(By.XPATH, '//div[@id="div_selectamt1"]/div/div/input[@class="select-dropdown dropdown-trigger"]').click()
    driver.find_element(By.XPATH, f'//div[@id="div_selectamt1"]/div/div/ul[@class="dropdown-content select-dropdown"]/li[{daten.funktion_value}]').click()


    # E-Mail
    email_input = driver.find_element(By.NAME, 'email1')
    email_input.clear()
    email_input.send_keys(f'{daten.vorname}.{daten.nachname}@htw-dresden.de')

    # Absenden des Formulars
    submit_button = driver.find_element(By.ID, 'save_button')
    submit_button.click()

    sleep(1)
    # Wir überprüfen ob das Ergebnis unsere Erwartungen erfüllt
    # Überprüfung der Ergebnisse über die Checkliste (bekommt jeder die "richtigen" Rechte (z.B. Schlüssel)?)
    driver.get("http://84.146.24.124:21037/checklisten")
    sleep(2)
    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')
    cards = soup.find_all('div', {'class': 'col l4 m6 s12'})
    
    for card in cards:
        name = card.find('span', {'class': 'card-title truncate'}).text.strip()
        position = card.find('p').text.strip()

        # Die richtige Checkliste des hinzugefügten Mitglieds auswählen
        if f'{daten.vorname} {daten.nachname}' == name:
            print('Name: ', name)
            print('Position: ', position)

            zugang_elemente = card.find_all('span', string='Zugang: Schleuse')
            recht_elemente = card.find_all('span', string=lambda string: string and string.startswith('Schlüssel'))

            if not zugang_elemente and not recht_elemente:
                print('Berechtigungen: Keine')
            
            rechte = []

            if zugang_elemente:
                for zugang_element in zugang_elemente:
                    berechtigung = zugang_element.text.strip()
                    rechte.append(berechtigung)
            
            recht_elemente = card.find_all('span', string=lambda string: string and string.startswith('Schlüssel'))


            if recht_elemente:
                for recht_element in recht_elemente:
                    recht = recht_element.text.strip()
                    rechte.append(recht)

            for i, recht in enumerate(rechte, start=1):
                print(f'Berechtigung{i}: {recht}')
            ergebnis = Daten(position, rechte, voller_name=name)
            
            # Wir vergleichen das Ergebnis mit unseren Erwartungen (Beispieldaten)
            if ergebnis.voller_name == daten.voller_name and ergebnis.position ==  daten.position and sorted(ergebnis.rechte) == sorted(daten.rechte):
                print(f'\nTest für {name} erfolgreich')
                return True
            else:
                print(f'\nTest für {name} NICHT erfolgreich\n')

                # Wenn der Test fehlschlägt geben wir alle relevanten Daten aus um manuell zu check was schiefgelaufen ist
                print(f'Daten:\n{daten}')
                print(f'Ergebnis:\n{ergebnis}')
                return False



def main():
    driver = webdriver.Chrome()
    num_tests = 0
    num_successful = 0

    try:
        einloggen(driver)
        # Die Daten für die Dropdowns (Org.Einheit, Bereich sowie Funktion) müssen leider als Zahlen übergeben werden,
        # ich fand jedenfalls keine Möglichkeit im Dropdown nach Strings auszuwählen.
        beispieldaten = [
            Daten('Service/Buchhaltung (Angestellte)', ['Zugang: Schleuse', 'Schlüssel4'], 2, 2, 2, 'Paul', 'Wentzel'),        
            Daten('Mitglied Ausschuss Finanzielles (Ausschüsse des StuRa)', ['Zugang: Schleuse', 'Schlüssel5', 'Schlüssel6'], 3, 2, 2, 'Georg', 'Schicker'),
            Daten('Leitung Beauftragung Datenschutz (Beauftragte des StuRa)', ['Zugang: Schleuse', 'Schlüssel8'], 4, 2, 2, 'Collin', 'Neumann'),
            Daten('studentische Vertretung (Beitrag Projekt eCampus)', ['Zugang: Schleuse'], 5, 2, 2, 'Nathalie', 'Kaestner'),
            Daten('SprecherIn Sprecherinnen und Sprecher (Fachausschuss Bauingenieurswesen/Architektur)', ['Zugang: Schleuse'], 6, 2, 2, 'Lennart', 'Bronke'),
            Daten('SprecherIn Sprecherinnen und Sprecher (Fachausschuss Design)', ['Zugang: Schleuse'], 7, 2, 2, 'Collina', 'Neumannski')
        ]
        for daten in beispieldaten:
            num_tests += 1
            if test(daten, driver):
                num_successful += 1
            print('#############################################')
            
    finally:
        driver.quit()

    print(f'Durchgeführte Tests: {num_tests}')
    print(f'Erfolgreiche Tests: {num_successful}')
    print(f'Fehlgeschlagene Tests: {num_tests - num_successful}')

main()