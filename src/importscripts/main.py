# -*- coding: utf-8 -*-

import os, django, sys
sys.path.append('..')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bin.settings")
django.setup()

from aemter.models import Organisationseinheit, Funktion, Unterbereich
import csv


def importAemter(file):
    """
    Diese Funktion importiert Organisationseinheiten, Unterbereiche und Funktionen aus einer CSV-Datei.
        
        **!ACHTUNG!**
        Diese Funktion leert die folgenden Tabellen in der Datenbank:

        * Organisationseinheit
        * Unterbereich
        * Funktion

    Um diese Funktion zu verwenden, wird eine CSV-Datei mit der folgenden Struktur benötigt:

        * delimiter = ','
        * organisationseinheit,unterbereich,funktion,max_members
        * Die erste Zeile ist eine Kopfzeile und wird nicht importiert


    :param file: Datei mit zu importierendem Inhalt
    :type file: TextIO
    :return: Kein Rückgabewert
    """

    # Delete existing Data
    Organisationseinheit.objects.all().delete()
    Unterbereich.objects.all().delete()
    Funktion.objects.all().delete()

    # read CSV
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        organisationseinheit = row[0]
        unterbereich = row[1]
        funktion = row[2]
        max_members = row[3]

        # Print Current Line for Debug
        # print(organisationseinheit + " | " + unterbereich + " | " + funktion + " | " + max_members)

        if (organisationseinheit == 'Organisationseinheit'):
            continue

        # Erstelle das Organisationseinheit
        if not Organisationseinheit.objects.filter(bezeichnung=organisationseinheit).exists():
            # print(organisationseinheit + " wurde erstellt")
            new_referat = Organisationseinheit(
                bezeichnung = organisationseinheit
            )
            new_referat.save()
        else:
            new_referat = Organisationseinheit.objects.get(bezeichnung=organisationseinheit)

        # Erstelle den Unterbereich
        if not Unterbereich.objects.filter(bezeichnung=unterbereich, organisationseinheit=new_referat).exists():
            new_unterbereich = None
            if (unterbereich != 'None'):
                # print(unterbereich + " wurde erstellt")
                new_unterbereich = Unterbereich(
                    bezeichnung = unterbereich,
                    organisationseinheit = new_referat
                )
                new_unterbereich.save()
        else:
            new_unterbereich = Unterbereich.objects.get(bezeichnung=unterbereich, organisationseinheit=new_referat)

        # Erstelle das Funktion
        # print(funktion + " wurde erstellt")
        new_amt = Funktion(
            bezeichnung = funktion,
            workload = 5,
            max_members = max_members,
            organisationseinheit = new_referat,
            unterbereich = new_unterbereich
        )
        new_amt.save()
    pass

if __name__ == "__main__":
    file = open("ReferateUnterbereicheAemter.csv", encoding="utf-8")
    importAemter(file)
