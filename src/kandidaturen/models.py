from django.db import models
from django.db.models import Q
from simple_history.models import HistoricalRecords
from aemter.models import Funktion

class Kandidatur(models.Model):
    """
    Datenbankmodell Kandidatur

    Felder:

    * name: Nachname der Kandidatur. Darf nicht null sein.
    * vorname: Vorname der Kandidatur. Darf nicht null sein.
    * spitzname: Spitzname der Kandidatur. Kann null sein.
    * wahldatum: Datum der Wahl der Kandidatur. Darf nicht null sein.
    * beschlussnummer: Beschlussnummer für die Wahl. Kann null sein.
    * history
    """
    name = models.CharField(max_length=50, null=False)
    vorname = models.CharField(max_length=50, null=False)
    spitzname = models.CharField(max_length=50, null=True)
    wahldatum = models.DateField(null=True)
    beschlussnummer = models.CharField(max_length=50, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.vorname + " " + self.name

    def curr_funktion_count(self):
        """
        Funktion, die die Anzahl der derzeitigen angestrebten Funktionen der Kandidatur zurückgibt.
        """
        return self.kandidaturamt_set\
            .count()

    def curr_funktion_first(self):
        """
        Funktion, die die erste der angestrebten Funktionen der Kandidatur zurückgibt
        oder None wenn die Kandidatur keine Funktion anstrebt.
        """
        if self.kandidaturamt_set.first():
            return self.kandidaturamt_set.first().funktion
        else:
            return None

    class Meta:
        verbose_name = "Kandidatur"
        verbose_name_plural = "Kandidaturen"


class KandidaturAmt(models.Model):
    """
    Datenbankmodell Zuordnung Kandidatur-Amt

    Felder:

    * kandidatur: Referenziert eine Kandidatur. Darf nicht null sein.
    * funktion: Referenziert eine Funktion. Darf nicht null sein.
    * history

    Es ist zu beachten, dass diese Zuordnung gelöscht wird, wenn die Kandidatur oder die Funktion gelöscht wird. (Cascade)
    """
    kandidatur = models.ForeignKey(Kandidatur, on_delete=models.CASCADE, null=False)
    funktion = models.ForeignKey(Funktion, on_delete=models.CASCADE, null=False)
    history = HistoricalRecords()
    def __str__(self):
        return self.kandidatur.__str__() + ", " + self.funktion.__str__()
    class Meta:
        verbose_name = "Zuordnung Kandidatur-Amt"
        verbose_name_plural = "Zuordnungen Kandidatur-Amt"


class KandidaturMail(models.Model):
    """
    Datenbankmodell Zuordnung Kandidatur-Mail

    Felder:

    * kandidatur: Referenziert eine Kandidatur. Darf nicht null sein.
    * email: Eine E-Mail-Adresse der Kandidatur. Darf nicht null sein.
    * history

    Es ist zu beachten, dass diese Zuordnung gelöscht wird, wenn die Kandidatur gelöscht wird. (Cascade)
    """
    kandidatur = models.ForeignKey(Kandidatur, on_delete=models.CASCADE, null=False)
    email = models.CharField(max_length=50, null=False)
    history = HistoricalRecords()
    def __str__(self):
        return self.email + " " + self.kandidatur.__str__()
    class Meta:
        verbose_name = "Zuordnung Kandidatur-Mail"
        verbose_name_plural = "Zuordnungen Kandidatur-Mail"
