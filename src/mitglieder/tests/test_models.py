from django.test import TestCase
from mitglieder.models import *
from aemter.models import *

class TestModels(TestCase):

    def setUp(self):
        self.mitglied1 = Mitglied.objects.create(
            name = "Peter",
            vorname = "Hans",
            spitzname = "Hansi",
            tel_mobil = "0352075199"
        )

        self.referat1 = Organisationseinheit.objects.create(
            bezeichnung = "myreferat"
        )

        self.unterbereich1 = Unterbereich.objects.create(
            bezeichnung = "myunterbereich",
            organisationseinheit = self.referat1
        )

        self.funktion1 = Funktion.objects.create(
            bezeichnung = "myamt",
            workload = 4,
            max_members = 5,
            organisationseinheit = self.referat1,
            unterbereich = self.unterbereich1
        )

        self.mitgliedfunktion1 = MitgliedAmt.objects.create(
            mitglied = self.mitglied1,
            funktion = self.funktion1
        )

        self.mitgliedmail1 = MitgliedMail.objects.create(
            mitglied = self.mitglied1,
            email = "sxxxxx@htw-dresden.de"
        )

    def test_mitglied_toString(self):
        self.assertEqual(
            self.mitglied1.__str__(),
            "Hans Peter")

    def test_mitgliedAmt_toString(self):
        self.assertEqual(
            self.mitgliedfunktion1.__str__(),
            "Hans Peter, myamt myunterbereich (myreferat)")

    def test_mitgliedMail_toString(self):
        self.assertEqual(
            self.mitgliedmail1.__str__(),
            "sxxxxx@htw-dresden.de Hans Peter")
