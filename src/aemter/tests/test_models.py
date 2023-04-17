from django.test import TestCase
from mitglieder.models import *
from aemter.models import *

class TestModels(TestCase):

    def setUp(self):
        self.referat1 = Organisationseinheit.objects.create(
            bezeichnung = "myreferat"
        )

        self.unterbereich1 = Unterbereich.objects.create(
            bezeichnung = "myunterbereich",
            organisationseinheit = self.referat1
        )

        self.funktion1 = Funktion.objects.create(
            bezeichnung = "myfunktion1",
            workload = 4,
            max_members = 5,
            organisationseinheit = self.referat1,
            unterbereich = self.unterbereich1
        )

        self.funktion2 = Funktion.objects.create(
            bezeichnung = "myfunktion2",
            workload = 4,
            max_members = 5,
            organisationseinheit = self.referat1,
            unterbereich = None
        )

    def test_Referat_toString(self):
        self.assertEqual(
            self.referat1.__str__(),
            "myreferat")

    def test_Unterbereich_toString(self):
        self.assertEqual(
            self.unterbereich1.__str__(),
            "myunterbereich (myreferat)")

    def test_Funktion1_toString(self):
        self.assertEqual(
            self.funktion1.__str__(),
            "myfunktion1 myunterbereich (myreferat)")

    def test_Funktion2_toString(self):
        self.assertEqual(
            self.funktion2.__str__(),
            "myfunktion2 (myreferat)")
