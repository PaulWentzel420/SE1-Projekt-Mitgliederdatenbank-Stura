from django.test import TestCase
from aemter.models import *
from mitglieder.models import *
from checklisten.models import *

class TestModels(TestCase):

    def setUp(self):
        self.member1 = Mitglied.objects.create(
            name="Peter",
            vorname="Hans",
            spitzname="Hansi",
            strasse="Straße der Freiheit",
            hausnr="1",
            plz="01642",
            ort="Adelsdorf",
            tel_mobil="0352075199"
        )

        self.referat1 = Organisationseinheit.objects.create(
            bezeichnung="myreferat"
        )

        self.unterbereich1 = Unterbereich.objects.create(
            bezeichnung="myunterbereich",
            organisationseinheit=self.referat1
        )

        self.funktion1 = Funktion.objects.create(
            bezeichnung="myfunktion",
            workload=4,
            max_members=5,
            organisationseinheit=self.referat1,
            unterbereich=self.unterbereich1
        )

        self.mitgliedfunktion1 = MitgliedAmt.objects.create(
            mitglied=self.member1,
            funktion=self.funktion1
        )

        self.checkliste1 = Checkliste.objects.create(
            mitglied=self.member1,
            amt=self.mitgliedfunktion1
        )

        self.aufgabe1 = Aufgabe.objects.create(
            bezeichnung="testtask"
        )

        self.checklisteAufgabe1 = ChecklisteAufgabe.objects.create(
            checkliste=self.checkliste1,
            aufgabe=self.aufgabe1,
            abgehakt=False
        )

        self.recht1 = Recht.objects.create(
            bezeichnung="testrecht"
        )

        self.checklisteRecht1 = ChecklisteRecht.objects.create(
            checkliste=self.checkliste1,
            recht=self.recht1,
            abgehakt=False
        )
        pass

    def test_checkliste_toString(self):
        self.assertEqual(
            self.mitgliedfunktion1.__str__(),
            self.checkliste1.__str__()
        )
        pass

    def test_aufgabe_toString(self):
        self.assertEqual(
            "testtask",
            self.aufgabe1.__str__()
        )
        pass

    def test_checklisteAufgabe_toString(self):
        self.assertEqual(
            self.checkliste1.__str__() + " - " + self.aufgabe1.__str__(),
            self.checklisteAufgabe1.__str__()
        )
        pass

    def test_checklisteRecht_toString(self):
        self.assertEqual(
            self.checkliste1.__str__() + " - " + self.recht1.__str__(),
            self.checklisteRecht1.__str__()
        )
        pass

    pass