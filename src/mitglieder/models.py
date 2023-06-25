from datetime import date
from django.db import models
from django.db.models import Q
from simple_history.models import HistoricalRecords
from aemter.models import Funktion

class Mitglied(models.Model):
    """
    Datenbankmodell Mitglied

    Felder:

    * name: Nachname des Mitglieds. Darf nicht null sein.
    * vorname: Vorname des Mitglieds. Darf nicht null sein.
    * spitzname: Spitzname des Mitglieds. Kann null sein.
    * tel_mobil: Telefonnummer des Mitglieds. Kann null sein.

    * tel_weitergabe: Stellt dar, ob die Telefonnummer des Mitglieds im Notfall weitergegeben werden darf. Standard ist False.
    * wahl_angenommen: Stellt dar, ob das Mitglied die Wahl bereits angenommen hat. Standard ist False.
    * kenntnis_ordn: Stellt dar, ob das Mitglied die Kenntnis der Ordnungen bereits eingereicht hat. Standard ist False.
    * verpfl_datengeheimnis: Stellt dar, ob das Mitglied die Verpflichtung zum Datengeheimnis bereits akzeptiert hat. Standard ist False.
    * stammdatenblatt: Stellt dar, ob das Mitglied das Stammdatenblatt bereits eingereicht hat. Standard ist False.
    * history
    """
    name = models.CharField(max_length=50, null=False)
    vorname = models.CharField(max_length=50, null=False)
    spitzname = models.CharField(max_length=50, null=True)
    tel_mobil = models.CharField(max_length=15, null=True)
    tel_weitergabe = models.BooleanField(default=False, null=False)

    auto_checkliste = models.BooleanField(default=True, null=False)
    wahl_angenommen = models.BooleanField(default=False, null=False)
    kenntnis_ordn = models.BooleanField(default=False, null=False)
    verpfl_datengeheimnis = models.BooleanField(default=False, null=False)
    stammdatenblatt = models.BooleanField(default=False, null=False)

    history = HistoricalRecords()

    def __str__(self):
        return self.vorname + " " + self.name

    def curr_funktion_count(self):
        """
        Funktion, die die Anzahl der derzeitigen Funktionen des Mitglieds zurückgibt.
        """
        return self.mitgliedamt_set\
            .filter(Q(amtszeit_ende__isnull=True) | Q(amtszeit_ende__gte=date.today()))\
            .count()

    def curr_funktion_first(self):
        """
        Funktion, die die erste Funktion des Mitglieds zurückgibt
        oder None wenn das Mitglied keine Funktion innehat.
        """
        if self.mitgliedamt_set\
                .filter(Q(amtszeit_ende__isnull=True) | Q(amtszeit_ende__gte=date.today())):
            return self.mitgliedamt_set\
                .filter(Q(amtszeit_ende__isnull=True) | Q(amtszeit_ende__gte=date.today()))\
                .first()\
                .funktion
        else:
            return None

    def admission_data_complete(self):
        """
        Funktion, die prüft, ob alle Daten für die Aufnahme als Mitglied vorhanden sind.
        """
        if self.wahl_angenommen and self.kenntnis_ordn and self.verpfl_datengeheimnis and self.stammdatenblatt:
            return True
        else:
            return False

    class Meta:
        verbose_name = "Mitglied"
        verbose_name_plural = "Mitglieder"


class MitgliedAmt(models.Model):
    """
    Datenbankmodell Zuordnung Mitglied-Amt

    Felder:

    * mitglied: Referenziert eine Mitglied. Darf nicht null sein.
    * funktion: Referenziert eine Funktion. Darf nicht null sein.
    * amtszeit_beginn: Datum des Beginns der Amtszeit. Kann null sein.
    * amtszeit_ende: Datum des Endes der Amtszeit. Kann null sein.
    * history

    Es ist zu beachten, dass diese Zuordnung gelöscht wird, wenn das Mitglied oder die Funktion gelöscht wird. (Cascade)
    """
    mitglied = models.ForeignKey(Mitglied, on_delete=models.CASCADE, null=False)
    funktion = models.ForeignKey(Funktion, on_delete=models.CASCADE, null=False)
    amtszeit_beginn = models.DateField(null=True)
    amtszeit_ende = models.DateField(null=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.mitglied.__str__() + ", " + self.funktion.__str__()
    class Meta:
        verbose_name = "Zuordnung Mitglied-Amt"
        verbose_name_plural = "Zuordnungen Mitglied-Amt"

class MitgliedMail(models.Model):
    """
    Datenbankmodell Zuordnung Mitglied-Mail

    Felder:

    * mitglied: Referenziert ein Mitglied. Darf nicht null sein.
    * email: Eine E-Mail-Adresse des Mitglieds. Darf nicht null sein.
    * history

    Es ist zu beachten, dass diese Zuordnung gelöscht wird, wenn das Mitglied gelöscht wird. (Cascade)
    """
    mitglied = models.ForeignKey(Mitglied, on_delete=models.CASCADE, null=False)
    email = models.CharField(max_length=50, null=False)
    history = HistoricalRecords()

    def __str__(self):
        return self.email + " " + self.mitglied.__str__()
    class Meta:
        verbose_name = "Zuordnung Mitglied-Mail"
        verbose_name_plural = "Zuordnungen Mitglied-Mail"
